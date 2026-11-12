#!/usr/bin/env python3
"""
denetle_post.py - Sosyal medya postlarını yayına almadan önce denetleyen kapı.

Post dosyasını (marketing takvim formatı) okur, yayınlanacak metni yeniden kurar
(gövde + CTA + hashtag ya da caption + hashtag) ve hem yayın biçimini hem yazılım
projesine özgü iddiaları ölçer.

  python3 scripts/denetle_post.py <post.md> [<post.md> ...]
  python3 scripts/denetle_post.py <takvim-dizini>
  python3 scripts/denetle_post.py --takvim <takvim-dizini>     # postlar arası denetim
  python3 scripts/denetle_post.py --metin "post metni" --platform linkedin
  python3 scripts/denetle_post.py <post.md> --json --katı
  python3 scripts/denetle_post.py <post.md> --canli            # kaynak/demo URL'lerini yoklar
  python3 scripts/denetle_post.py <post.md> --kural-kapat K12,K14
  python3 scripts/denetle_post.py <post.md> --config post-kapisi.json

Çıkış kodu: 0 temiz, 1 hata var (yayınlanmaz), 2 kullanım/dosya hatası.
Uyarılar normalde kapıyı kapatmaz; --katı verilirse kapatır.

Bu betik metnin yazarını tespit etmez. Yalnızca yayından önce düzeltilebilecek
kalıpları, platform sınırlarını ve proje iddialarını raporlar. Kurallar ve
gerekçeler: references/sosyal-medya.md · plan: docs/DENETLE_POST_GELISTIRME_PLANI.md
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detect_tr_ai import analyze_text  # noqa: E402

SURUM = 2

HATASI = "hata"
UYARI = "uyarı"
BILGI = "bilgi"

# --- Kural kataloğu ---------------------------------------------------------
# Rapor ve JSON bu kimlikleri kullanır; post-kapisi.json seviye ezmeleri de bunlarla yapılır.

KURALLAR = {
    "K0": "Yayın biçimi (platform bütçesi, hook, hashtag, paragraf, emoji, CTA, tekrar)",
    "K1": "Zorunlu bölümler",
    "K2": "Carousel bütünlüğü (slayt sayısı, TR/EN eşliği)",
    "K3": "Slayt uzunluğu",
    "K4": "Slayt dili (EN satırda Türkçe harf, çeviri eksikliği)",
    "K5": "A tipi repo linki metinde var mı",
    "K6": "Fork beyanı",
    "K7": "Proje iddiası doğruluk notunda var mı",
    "K8": "Private sızıntısı (kurulum komutu, link)",
    "K9": "Sır ve kişisel veri taraması",
    "K10": "Teknoloji adı yazımı",
    "K11": "Özellik yığını",
    "K12": "İç jargon",
    "K13": "Bozuk kodlama (mojibake)",
    "K14": "Sürüm/durum iddiası",
    "K15": "Postlar arası tekrar",
    "K16": "İçerik sütunu dengesi",
    "K17": "Canlı link sağlığı",
}

# --- Platform bütçeleri (references/sosyal-medya.md ile aynı) ---------------

PLATFORMS = {
    "linkedin": {
        "label": "LinkedIn",
        "max_chars": 3000,
        "hook_chars": 200,
        "hashtag_min": 2,
        "hashtag_max": 5,
        "body_words": (110, 260),
    },
    "instagram": {
        "label": "Instagram (caption)",
        "max_chars": 2200,
        "hook_chars": 150,
        "hashtag_min": 3,
        "hashtag_max": 10,
        "body_words": (70, 180),
    },
    "x": {
        "label": "X",
        "max_chars": 280,
        "hook_chars": 120,
        "hashtag_min": 0,
        "hashtag_max": 2,
        "body_words": (5, 45),
    },
}

PLATFORM_ALIASES = {
    "li": "linkedin", "linkedin": "linkedin", "in": "linkedin",
    "ig": "instagram", "instagram": "instagram", "insta": "instagram",
    "x": "x", "twitter": "x",
}

# Post türüne göre kelime bütçesi (proje-tanitim-postu skill'indeki aralıklarla aynı).
TUR_BUTCE = {
    "ipucu": (110, 170),
    "tanitim": None,
    "teknik": (150, 250),
    "carousel": None,
}
TUR_ALIASES = {"ipucu": "ipucu", "ipuç": "ipucu", "tip": "ipucu", "tanitim": "tanitim",
               "tanıtım": "tanitim", "teknik": "teknik", "carousel": "carousel", "karusel": "carousel"}

# --- Markdown ayrıştırma ---------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SLIDE_RE = re.compile(r"^(?:kapak|slayt)\b[^\d]*(\d+)|^(\d+)\s*[-:.]")
TR_PREFIX_RE = re.compile(r"^\s*(TR|EN)\s*:\s*(.*)$", re.IGNORECASE)


def split_frontmatter(raw: str) -> tuple:
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    fm = {}
    for line in m.group(1).splitlines():
        idx = line.find(":")
        if idx > 0:
            fm[line[:idx].strip()] = line[idx + 1:].strip()
    return fm, raw[m.end():]


def split_sections(body: str) -> dict:
    """'# Gövde' gibi birinci düzey başlıkları anahtar yapar."""
    sections = {}
    current = None
    buf = []
    for line in body.splitlines():
        m = HEADING_RE.match(line.strip())
        if m and len(m.group(1)) == 1:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(2).strip().lower()
            buf = []
            continue
        if current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def section(sections: dict, *names: str) -> str:
    for name in names:
        key = name.lower()
        for k, v in sections.items():
            if k == key or k.startswith(key + " "):
                return v
    return ""


def sanitize(text: str) -> str:
    """Yayın hattındaki (zamanla.mjs / postis-yonet.mjs) temizlikle aynı kurallar."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"(?m)^\s*[-*]\s+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def resolve_platform(value: str) -> str:
    key = (value or "").strip().lower()
    key = PLATFORM_ALIASES.get(key, key)
    if key not in PLATFORMS:
        raise ValueError(f"Bilinmeyen platform: {value}. Seçenekler: {', '.join(PLATFORMS)}")
    return key


def resolve_tur(value: str) -> str:
    key = (value or "").strip().lower()
    key = TUR_ALIASES.get(key, key)
    if key not in TUR_BUTCE:
        raise ValueError(f"Bilinmeyen post türü: {value}. Seçenekler: {', '.join(TUR_BUTCE)}")
    return key


def platform_from_name(path: Path) -> str:
    name = path.name.lower()
    if name.endswith("-linkedin.md"):
        return "linkedin"
    if name.endswith("-ig.md"):
        return "instagram"
    return "linkedin"


def tur_from_post(fm: dict, platform: str, path_name: str = "", explicit: str = None) -> str:
    if explicit:
        return resolve_tur(explicit)
    if platform == "instagram":
        return "carousel"
    if "-ipucu-" in path_name.lower():
        return "ipucu"
    if "teknik" in (fm.get("tur") or "").lower():
        return "teknik"
    return "tanitim"


# --- Ölçüm yardımcıları ----------------------------------------------------

URL_RE = re.compile(r"https?://\S+|www\.\S+")
HASHTAG_RE = re.compile(r"(?<![\w/])#([^\s#.,;:!?)]+)")
LOCAL_PATH_RE = re.compile(r"(?:\b[A-Za-z]:\\|~/|/home/[\w.-]+|/Users/[\w.-]+)")
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]"
)
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\[(?:somut|veri|link|ekle|doldur)[^\]]*\]|<[a-zçğıöşü]{3,}(?:\s[a-zçğıöşü]+)*>")
BOLD_LABEL_RE = re.compile(r"(?m)^\s*(?:[-*]\s+)?\*\*[^*\n]{1,60}\*\*\s*:?")
BULLET_RE = re.compile(r"(?m)^\s*[-*]\s+\S")
YEAR_RE = re.compile(r"(?:19|20)\d{2}")

HOOK_CLICHE = [
    (r"^\s*bu\s+(?:yazıda|postta|içerikte)\b", "P0 Açılış: 'Bu yazıda/postta' sahneleme girişi"),
    (r"^\s*bugün\s+sizlere\b", "P0 Açılış: 'Bugün sizlere' sunucu sesi"),
    (r"\b(?:gururla|heyecanla)\s+(?:duyur|paylaş|sun)", "P0 Duyuru: 'Gururla duyuruyoruz' kalıbı"),
    (r"\b(?:devrim\s+niteliğinde|oyunun\s+kurallarını\s+değiştir|çığır\s+açan)\b", "P0 Şişirme: 'devrim niteliğinde / çığır açan'"),
    (r"\b(?:günümüzün\s+hızla\s+değişen|dijitalleşen\s+(?:dünyada|çağımızda)|yapay\s+zeka\s+çağında)\b", "P0 Sahneleme: boş çağ girişi"),
    (r"\b(?:unutmayın|şunu\s+belirtmeliyim\s+ki)\b", "Tier-2 Dolgu: 'unutmayın / şunu belirtmeliyim ki'"),
    (r"\b(?:yorumlarda\s+buluşalım|düşüncelerinizi\s+(?:yorumlarda\s+)?paylaşın)\b", "P0 CTA: 'yorumlarda buluşalım' kalıbı"),
]

EMOJI_BULLET_RE = re.compile(r"(?m)^\s*(?:" + EMOJI_RE.pattern + r"|[\u2022\u25AA\u25CF])\s+")

TECH_CASING = {
    r"\bGithub\b": "GitHub",
    r"\bGitlab\b": "GitLab",
    r"\bJavascript\b": "JavaScript",
    r"\bTypescript\b": "TypeScript",
    r"\bNodejs\b": "Node.js",
    r"\bNodeJS\b": "Node.js",
    r"\bPostgres\b": "PostgreSQL",
    r"\bPostgre\b": "PostgreSQL",
    r"\bReactjs\b": "React",
    r"\bVuejs\b": "Vue",
    r"\bNextjs\b": "Next.js",
    r"\bDotnet\b|\.net\b": ".NET",
    r"\bFlutter\b(?= )": "Flutter",
    r"\bMySql\b": "MySQL",
    r"\bMongoDb\b": "MongoDB",
    r"\bSqlLite\b": "SQLite",
}

# Gövdede geçen iddia, doğruluk notunda karşılığını bulmalı (K7).
IDDIA_SOZLUGU = [
    "flutter", "react", "next.js", "vue", "svelte", "electron", "node.js", "express",
    "sqlite", "postgresql", "mysql", "supabase", "firebase", "docker", "redis",
    "typescript", "javascript", "python", "rust", "golang", "swift", "kotlin", "dart",
    "graphql", "websocket", "rest", "apache-2.0", "mit lisans", "gpl", "agpl",
    "açık kaynak", "ücretsiz", "sunucu yok", "offline", "çevrimdışı",
]

PRIVATE_INSTALL_RE = re.compile(
    r"\b(?:git\s+clone|npm\s+(?:i|install)|pnpm\s+(?:i|add)|yarn\s+add|cargo\s+install|"
    r"pip\s+install|docker\s+run|composer\s+require|go\s+get)\b",
    re.IGNORECASE,
)

SECRET_PATTERNS = [
    (re.compile(r"https?://[^\s/@]+:[^\s/@]+@"), "URL içinde kullanıcı adı ve şifre"),
    (re.compile(r"\b(?:sk-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|xox[abp]-[A-Za-z0-9-]{10,})\b"), "API anahtarı / token"),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._-]{12,}"), "Bearer token"),
    (re.compile(r"\bTR\d{24}\b"), "IBAN"),
    (re.compile(r"\b(?:\+90|0)\s?\(?5\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{2}[\s.-]?\d{2}\b"), "telefon numarası"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}"), "e-posta adresi"),
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "IP adresi"),
]

FORK_RE = re.compile(r"\bfork\b|\bçatal\b", re.IGNORECASE)
FORK_AUTHORSHIP_RE = re.compile(
    r"\b(?:ben\s+)?(?:yazdım|geliştirdim|kurdum|tasarladım|oluşturdum|kodladım)\b", re.IGNORECASE
)

JARGON_RE = re.compile(r"\bFaz\s*\d|\bW\d{2}\b|\bsprint\b|\bepic\b|\bticket\b|\bPR\s*#|\bissue\s*#", re.IGNORECASE)
VERSION_RE = re.compile(r"\b(?:MVP|beta|alfa|v\d+\.\d+(?:\.\d+)?)\b", re.IGNORECASE)
MOJIBAKE_RE = re.compile(r"[ÃÂÄÅ][\u0080-\u00BF]|\uFFFD")

QUOTE_SPAN_RE = re.compile(r'"[^"\n]{1,160}"|\u201c[^\u201d\n]{1,160}\u201d|\u2018[^\u2019\n]{1,160}\u2019')
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def norm_words(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\wçğıöşüÇĞİÖŞÜ ]", " ", text.lower())).strip()


def sentence_count(paragraph: str) -> int:
    return len([p for p in SENTENCE_SPLIT_RE.split(paragraph) if len(p.split()) > 1])


def numeric_tokens(text: str) -> set:
    return {tok for tok, _ in numeric_occurrences(text)}


def numeric_occurrences(text: str) -> list:
    """(sayı, konum) çiftleri. Yıl, ondalık ve versiyon numaraları sayılmaz."""
    out = []
    for m in re.finditer(r"(?<![\d.,])(\d+(?:[.,]\d+)?)(?![\d])(?!\.\d)", text):
        raw = m.group(1)
        if "," in raw or "." in raw:
            continue
        if YEAR_RE.fullmatch(raw):
            continue
        out.append((raw.lstrip("0") or "0", m.start()))
    return out


def in_quotes(text: str, position: int) -> bool:
    """Alıntı içindeki sayı örnek gösterimdir, metrik iddiası değil."""
    return any(m.start() <= position < m.end() for m in QUOTE_SPAN_RE.finditer(text))


def words_of(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


# --- Rapor -----------------------------------------------------------------


class Report:
    def __init__(self, path, platform, tur):
        self.path = path
        self.platform = platform
        self.tur = tur
        self.findings = []

    def add(self, level, code, message, evidence=None, where=None, kural="K0"):
        self.findings.append({
            "seviye": level,
            "kod": code,
            "kural": kural,
            "mesaj": message,
            "kanit": (evidence or "").strip()[:160],
            "yer": where or "",
        })

    def apply_overrides(self, overrides: dict):
        for f in self.findings:
            if f["kural"] in overrides:
                f["seviye"] = overrides[f["kural"]]
                f["ezildi"] = True

    def count(self, level):
        return sum(1 for f in self.findings if f["seviye"] == level)


# --- Denetim ---------------------------------------------------------------


def parse_slides(sections: dict) -> dict:
    """Slayt numarası -> (başlık, TR metni, EN metni). Kapak 1 sayılır."""
    slides = {}
    for key, text in sections.items():
        if key.startswith("görsel") or key.startswith("caption") or key.startswith("hashtag"):
            continue
        m = SLIDE_RE.match(key)
        if not m:
            continue
        number = int(m.group(1) or m.group(2))
        tr, en = [], []
        target = None
        for line in text.splitlines():
            pm = TR_PREFIX_RE.match(line)
            if pm:
                target = tr if pm.group(1).upper() == "TR" else en
                if pm.group(2).strip():
                    target.append(pm.group(2).strip())
                continue
            if target is not None and line.strip():
                target.append(line.strip())
        slides[number] = (key, "\n".join(tr).strip(), "\n".join(en).strip())
    return slides


def audit_post(raw: str, platform: str, name: str = "metin", tur: str = None,
               overrides: dict = None, katı: bool = False) -> dict:
    fm, body = split_frontmatter(raw)
    sections = split_sections(body)
    profile = PLATFORMS[platform]
    tur = tur_from_post(fm, platform, name, tur)
    report = Report(name, platform, tur)

    govde = section(sections, "Gövde")
    caption = section(sections, "Caption")
    cta = section(sections, "CTA")
    hashtag = section(sections, "Hashtag", "Hashtag (8-10)")
    hook_alternatives = section(sections, "Hook alternatifleri")
    chosen_hook = section(sections, "Seçilen hook")
    truth_note = section(sections, "Teknik doğruluk notu")
    slides = parse_slides(sections) if platform == "instagram" else {}
    slide_text = "\n\n".join(t[1] for t in slides.values() if t[1])

    main = caption if platform == "instagram" else govde
    if not main:
        beklenen = "Caption" if platform == "instagram" else "Gövde"
        report.add(HATASI, "P-YAPI", f"'{beklenen}' bölümü boş ya da yok", kural="K1")

    parts = [main, cta, hashtag]
    raw_content = "\n\n".join(p for p in parts if p).strip()
    content = sanitize(raw_content)

    # --- K0: yayın biçimi ---------------------------------------------------
    chars = len(content)
    if chars > profile["max_chars"]:
        report.add(HATASI, "P-UZUNLUK",
                   f"{chars} karakter, {profile['label']} sınırı {profile['max_chars']}",
                   f"...{content[-40:]}")

    first_line = next((ln.strip() for ln in content.splitlines() if ln.strip()), "")
    if first_line:
        if len(first_line) > profile["hook_chars"]:
            report.add(UYARI, "P-HOOK-UZUNLUK",
                       f"İlk satır {len(first_line)} karakter; {profile['label']} önizlemesi "
                       f"{profile['hook_chars']} karakterde kesiliyor", first_line)
        if len(first_line.split()) > 32:
            report.add(UYARI, "P-HOOK-KELIME",
                       f"İlk satır {len(first_line.split())} kelime; hook 12 kelimeyi geçmemeli", first_line)
    for pattern, label in HOOK_CLICHE:
        for m in re.finditer(pattern, content, flags=re.IGNORECASE):
            report.add(HATASI, "P-HOOK-KLISE", label, m.group(0))

    tags = HASHTAG_RE.findall(content)
    if hashtag.strip():
        if len(tags) < profile["hashtag_min"]:
            report.add(UYARI, "P-HASHTAG-AZ",
                       f"{len(tags)} hashtag; {profile['label']} için en az {profile['hashtag_min']} önerilir")
        if len(tags) > profile["hashtag_max"]:
            report.add(HATASI, "P-HASHTAG-COK",
                       f"{len(tags)} hashtag; {profile['label']} üst sınırı {profile['hashtag_max']}")
    else:
        report.add(UYARI, "P-HASHTAG-YOK", "Hashtag bölümü yok", kural="K1")
    body_tags = HASHTAG_RE.findall(sanitize(main))
    if body_tags:
        report.add(UYARI, "P-HASHTAG-GOVDE",
                   "Hashtag gövde içinde: " + ", ".join("#" + t for t in body_tags[:4]))

    for para in [p.strip() for p in content.split("\n\n") if p.strip()]:
        if HASHTAG_RE.search(para) and len(para) < 200:
            continue
        if sentence_count(para) > 5 or len(para) > 520:
            report.add(UYARI, "P-PARAGRAF",
                       f"Paragraf {sentence_count(para)} cümle / {len(para)} karakter; 3 cümlede böl",
                       para[:120])

    emojis = EMOJI_RE.findall(content)
    if len(emojis) > 3:
        report.add(UYARI, "P-EMOJI", f"{len(emojis)} emoji; post başına 3'ü geçmesin")
    if EMOJI_BULLET_RE.search(raw_content):
        report.add(UYARI, "P-EMOJI-BULLET", "Satır başında emoji madde imi olarak kullanılmış")
    bold = BOLD_LABEL_RE.search(raw_content)
    if bold:
        report.add(UYARI, "P-KALIN-ETIKET", "Kalın etiket + iki nokta listesi; düz cümleye çevir",
                   bold.group(0))

    if platform != "x":
        if not cta.strip():
            if platform == "instagram" and slides:
                report.add(BILGI, "P-CTA-GOMULU", "Ayrı CTA bölümü yok; istem slayt 6 ve caption içinde",
                           kural="K1")
            else:
                report.add(UYARI, "P-CTA-YOK", "CTA bölümü yok; postun tek istemi belirsiz", kural="K1")
        elif cta.count("?") > 1:
            report.add(UYARI, "P-CTA-COK", "CTA içinde birden fazla soru; tek istem bırak", cta[:120])
        elif len(cta) > 220:
            report.add(UYARI, "P-CTA-UZUN", f"CTA {len(cta)} karakter; tek cümleye indir", cta[:120])

    for m in PLACEHOLDER_RE.finditer(content):
        report.add(HATASI, "P-YERTUTUCU", "Metinde doldurulmamış yer tutucu", m.group(0))

    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(content) if len(s.split()) > 3]
    seen, dupes = {}, []
    for s in sentences:
        key = norm_words(s)
        if len(key.split()) < 5:
            continue
        if key in seen:
            dupes.append(s[:90])
        seen[key] = True
    if dupes:
        report.add(UYARI, "P-TEKRAR-CUMLE", f"{len(dupes)} cümle birebir tekrar ediyor", dupes[0])

    if platform != "instagram" and hook_alternatives.strip():
        count = len(re.findall(r"(?m)^\s*\d+[.)]\s+", hook_alternatives))
        digit = re.search(r"\d+", chosen_hook)
        if count and digit and not (1 <= int(digit.group(0)) <= count):
            report.add(UYARI, "P-HOOK-SECIM",
                       f"Seçilen hook {digit.group(0)} numaralı; alternatif sayısı {count}")

    # --- K1 / K2-K4: carousel ----------------------------------------------
    if platform == "instagram":
        if not slides:
            report.add(UYARI, "P-SLAYT-YOK", "Carousel slayt bölümü yok (Kapak + 5 slayt beklenir)",
                       kural="K2")
        else:
            for n in range(1, 7):
                if n not in slides:
                    report.add(HATASI, "P-SLAYT-EKSIK", f"Slayt {n} yok; carousel 6 slayttan oluşur",
                               kural="K2")
            for n in sorted(slides):
                if n > 6:
                    report.add(UYARI, "P-SLAYT-FAZLA", f"Slayt {n}: carousel 6 slaytta biter", kural="K2")
            wants_en = "en" in (fm.get("dil") or "").lower()
            for n in sorted(slides):
                baslik, tr, en = slides[n]
                if not tr:
                    report.add(HATASI, "P-SLAYT-TR-YOK", f"Slayt {n}: TR satırı yok", kural="K2")
                if wants_en and not en:
                    report.add(HATASI, "P-SLAYT-EN-YOK", f"Slayt {n}: EN satırı yok (dil: {fm.get('dil')})",
                               kural="K2")
                tr_words, en_words = words_of(tr), words_of(en)
                limit = 10 if n == 1 else 14
                if tr_words > limit:
                    report.add(UYARI, "P-SLAYT-UZUN",
                               f"Slayt {n}: {tr_words} kelime; {'kapak' if n == 1 else 'slayt'} "
                               f"sınırı {limit}", tr[:90], kural="K3")
                if en and re.search(r"[çğıöşüÇĞİÖŞÜ]", en):
                    report.add(UYARI, "P-SLAYT-EN-TR",
                               f"Slayt {n}: EN satırında Türkçe harf var", en[:90], kural="K4")
                if en and tr_words >= 4 and en_words < tr_words * 0.5:
                    report.add(UYARI, "P-SLAYT-EN-KISA",
                               f"Slayt {n}: EN {en_words} kelime, TR {tr_words}; çeviri eksik olabilir",
                               en[:90], kural="K4")
            kapak = slides.get(1, ("", "", ""))[1]
            for pattern, label in HOOK_CLICHE:
                for m in re.finditer(pattern, kapak, flags=re.IGNORECASE):
                    report.add(HATASI, "P-SLAYT-KLISE", f"Kapak: {label}", m.group(0), "slayt 1")
            if slide_text:
                slide_analysis = analyze_text(slide_text, "blog-deneme")
                for f in slide_analysis["findings"]:
                    if f["severity"] != "sinyal":
                        continue
                    level = HATASI if f["rule"].startswith(("Tier-1", "P0")) else UYARI
                    report.add(level, "D-SLAYT", f"{f['rule']} (slayt metni)", f["match"], "slayt")

    # --- K5: A tipi repo linki ---------------------------------------------
    kaynak = (fm.get("kaynak") or "").strip()
    tip = (fm.get("tip") or "").strip()
    kaynak_url = kaynak if kaynak.lower().startswith("http") else ""
    if kaynak_url:
        in_content = link_present(kaynak_url, content)
        in_slides = bool(slide_text) and link_present(kaynak_url, slide_text)
        if platform == "instagram":
            if not (in_content or in_slides):
                report.add(UYARI, "P-LINK-YOK",
                           f"A tipi post; kaynak URL ne caption'da ne slaytta: {kaynak_url}",
                           kaynak_url, kural="K5")
            elif not in_content:
                report.add(BILGI, "P-LINK-BIO",
                           "Repo linki yalnızca slaytta; Instagram caption'da link tıklanmaz, bio'ya ekle",
                           kaynak_url, kural="K5")
        elif not in_content:
            report.add(HATASI, "P-LINK-YOK",
                       f"A tipi post; kaynak URL metinde yok: {kaynak_url}", kaynak_url, kural="K5")

    # --- K6: fork beyanı ----------------------------------------------------
    if FORK_RE.search(tip):
        if not FORK_RE.search(truth_note):
            report.add(UYARI, "P-FORK-NOT",
                       "Fork postunda doğruluk notu upstream/fork bilgisini anmıyor",
                       truth_note[:100], kural="K6")
        if FORK_AUTHORSHIP_RE.search(content) and not upstream_named(kaynak, truth_note):
            report.add(UYARI, "P-FORK-SAHIPLIK",
                       "Fork postunda 'yazdım/geliştirdim' var, upstream proje adı geçmiyor",
                       FORK_AUTHORSHIP_RE.search(content).group(0), kural="K6")

    # --- K7: iddia izi ve sayı ---------------------------------------------
    if truth_note.strip():
        allowed = numeric_tokens(truth_note) | numeric_tokens(" ".join(fm.values()))
        added = [(tok, pos) for tok, pos in numeric_occurrences(content) if tok not in allowed]
        metric = sorted({tok for tok, pos in added if not in_quotes(content, pos)}, key=lambda x: (len(x), x))
        quoted = sorted({tok for tok, pos in added if in_quotes(content, pos)}, key=lambda x: (len(x), x))
        if metric:
            report.add(HATASI, "P-SAYI-UYDURMA", "Doğruluk notunda olmayan sayı: " + ", ".join(metric),
                       kural="K7")
        if quoted:
            report.add(UYARI, "P-SAYI-ALINTI",
                       "Alıntı içindeki sayı doğruluk notunda yok: " + ", ".join(quoted), kural="K7")
        note_lower = truth_note.lower()
        missing = [t for t in IDDIA_SOZLUGU if re.search(rf"\b{re.escape(t)}\b", content, re.IGNORECASE)
                   and t not in note_lower]
        if missing:
            report.add(UYARI, "P-IDDIA-IZI",
                       "Gövdedeki iddia doğruluk notunda yok: " + ", ".join(missing[:6]), kural="K7")
    else:
        report.add(UYARI, "P-DOGRULUK-NOTU-YOK",
                   "Teknik doğruluk notu yok; sayı ve iddialar denetlenmedi", kural="K7")

    if VERSION_RE.search(content) and truth_note.strip():
        versions = {v.lower() for v in VERSION_RE.findall(content)}
        not_covered = [v for v in versions if v not in truth_note.lower()]
        if not_covered:
            report.add(UYARI, "P-SURUM",
                       "Sürüm/durum iddiası doğruluk notunda yok: " + ", ".join(sorted(not_covered)),
                       kural="K14")

    # --- K8: private sızıntısı ---------------------------------------------
    if "private" in kaynak.lower():
        urls = URL_RE.findall(content)
        if urls:
            report.add(HATASI, "P-LINK-SIZINTI", "kaynak 'private' ama metinde URL var", urls[0],
                       kural="K8")
        install = PRIVATE_INSTALL_RE.search(content)
        if install:
            report.add(HATASI, "P-KURULUM-SIZINTI",
                       "kaynak 'private' ama metinde kurulum komutu var", install.group(0), kural="K8")
    if re.match(r"^B(\s|$|\()", tip, flags=re.IGNORECASE):
        if "kontrol edildi" not in (fm.get("gizlilik") or "").lower():
            report.add(HATASI, "P-GIZLILIK", "tip B ama 'gizlilik: kontrol edildi' satırı yok", kural="K8")

    # --- K9: sır ve kişisel veri -------------------------------------------
    for pattern, label in SECRET_PATTERNS:
        m = pattern.search(content)
        if m:
            report.add(HATASI, "P-SIR", f"Metinde {label} var", m.group(0), kural="K9")
    local = LOCAL_PATH_RE.search(content)
    if local:
        report.add(HATASI, "P-YOL-SIZINTI", "Metinde yerel dosya yolu var", local.group(0), kural="K9")

    # --- K10: teknoloji adı yazımı -----------------------------------------
    for pattern, dogru in TECH_CASING.items():
        for m in re.finditer(pattern, content):
            if m.group(0) == dogru:
                continue
            report.add(UYARI, "P-TEKNOLOJI-ADI", f"'{m.group(0)}' -> '{dogru}'", kural="K10")

    # --- K11: özellik yığını -----------------------------------------------
    run = 0
    for line in main.splitlines():
        if BULLET_RE.match(line):
            run += 1
            if run == 4:
                report.add(UYARI, "P-MADDE-YIGINI",
                           "4+ ardışık madde; özellik listesi yerine 2-3 madde ya da düz cümle",
                           line.strip()[:90], kural="K11")
        else:
            run = 0
    for sent in SENTENCE_SPLIT_RE.split(main):
        if sent.count(",") >= 5 and re.search(r"\bve\b", sent):
            report.add(UYARI, "P-OZELLIK-ZINCIRI",
                       "Tek cümlede 6+ öge; özellik yığını gibi okunuyor", sent.strip()[:110], kural="K11")

    # --- K12 / K13 ----------------------------------------------------------
    for m in JARGON_RE.finditer(content):
        report.add(UYARI, "P-JARGON", f"İç jargon: '{m.group(0)}' (dışarıdaki okur bilmez)",
                   kural="K12")
    m = MOJIBAKE_RE.search(content)
    if m:
        report.add(HATASI, "P-KODLAMA", "Bozuk kodlama (mojibake)", m.group(0), kural="K13")

    # --- AI kalıp motoru ----------------------------------------------------
    analysis = analyze_text(content, "blog-deneme")
    for f in analysis["findings"]:
        if f["severity"] != "sinyal":
            continue
        if f["rule"].startswith(("Tier-1", "P0", "P2 Noktalama")):
            level = HATASI
        else:
            level = UYARI
        report.add(level, "D-" + f["rule"].split(":")[0].strip().replace(" ", "-"), f["rule"], f["match"])
    if analysis["repeated_ending_warning"]:
        report.add(UYARI, "D-EK-TEKRARI",
                   f"Art arda {analysis['repeated_ending_max_run']} cümle aynı ekle bitiyor "
                   f"({analysis['repeated_ending_class']})")
    if analysis["total_flags"] and analysis["word_count"] >= 60:
        per_100 = round(analysis["total_flags"] / analysis["word_count"] * 100, 1)
        if per_100 > 3.0:
            report.add(HATASI, "D-YOGUNLUK", f"100 kelimede {per_100} kalıp sinyali; yoğunluk sınırı 3.0")

    words = words_of(re.sub(r"#\S+", " ", content))
    lo, hi = TUR_BUTCE.get(tur) or profile["body_words"]
    if lo and words < lo:
        report.add(UYARI, "P-KELIME-AZ", f"{words} kelime; {tur} için beklenen {lo}-{hi}")
    if words > hi:
        report.add(UYARI, "P-KELIME-COK", f"{words} kelime; {tur} için beklenen {lo}-{hi}")

    if overrides:
        report.apply_overrides(overrides)
    hatasi = report.count(HATASI)
    uyari = report.count(UYARI)
    engelli = hatasi > 0 or (katı and uyari > 0)
    return {
        "dosya": name,
        "platform": platform,
        "platform_label": profile["label"],
        "profil": f"{platform}/{tur}",
        "sonuc": "KALDI" if engelli else "GECTI",
        "hata": hatasi,
        "uyari": uyari,
        "bilgi": report.count(BILGI),
        "olcumler": {
            "karakter": chars,
            "kelime": words,
            "hashtag": len(tags),
            "slayt": len(slides),
            "ilk_satir_karakter": len(first_line),
            "cumle_cov": analysis["sentence_length_cov"],
            "kalip_sinyali": analysis["total_flags"],
        },
        "bulgular": report.findings,
    }


def link_present(kaynak_url: str, content: str) -> bool:
    norm = re.sub(r"^https?://", "", kaynak_url.strip()).rstrip("/").lower()
    norm = norm.replace("www.", "")
    content_lower = content.lower()
    if norm in content_lower:
        return True
    return norm.split("/")[0] in content_lower


def upstream_named(kaynak: str, truth_note: str) -> bool:
    """Fork postunda upstream proje adı geçiyor mu: doğruluk notu ya da kaynak URL'si farklı sahip."""
    if re.search(r"fork|çatal|upstream|orijinal|kaynak proje", truth_note, re.IGNORECASE):
        return True
    m = re.match(r"https?://github\.com/([^/]+)/", kaynak or "", re.IGNORECASE)
    return bool(m and m.group(1).lower() == "bahattinercan")


# --- Takvim modu (K15/K16) -------------------------------------------------


def audit_calendar(paths: list, platform_of, overrides: dict) -> list:
    posts = []
    for path in paths:
        raw = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(raw)
        sections = split_sections(body)
        platform = resolve_platform(platform_of(path, fm))
        content = sanitize((section(sections, "Caption") if platform == "instagram"
                            else section(sections, "Gövde")) or "")
        posts.append({
            "name": path.name, "path": path, "fm": fm, "platform": platform,
            "content": content, "tur": tur_from_post(fm, platform, path.name),
        })

    def opening(text):
        return " ".join(norm_words(text).split()[:6])

    def shingles(text, n=5):
        w = norm_words(text).split()[:200]
        return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}

    extra = []
    for i, a in enumerate(posts):
        for b in posts[i + 1:]:
            where = f"{a['name']} <-> {b['name']}"
            if opening(a["content"]) and opening(a["content"]) == opening(b["content"]):
                extra.append({"seviye": UYARI, "kod": "P-TAKVIM-ACILIS", "kural": "K15",
                              "mesaj": "İki post aynı 6 kelimeyle açılıyor: " + opening(a["content"]),
                              "kanit": b["name"], "yer": where})
                continue
            sa, sb = shingles(a["content"]), shingles(b["content"])
            if sa and sb:
                jaccard = len(sa & sb) / len(sa | sb)
                if jaccard >= 0.6:
                    extra.append({"seviye": UYARI, "kod": "P-TAKVIM-TEKRAR", "kural": "K15",
                                  "mesaj": f"İki post %{round(jaccard * 100)} örtüşüyor",
                                  "kanit": b["name"], "yer": where})

    by_week = {}
    for p in posts:
        week = (p["fm"].get("hafta") or "").strip()
        by_week.setdefault(p["fm"].get("proje") or p["name"], []).append((week, p))
    for proje, items in by_week.items():
        weeks = sorted({w for w, _ in items if w})
        for x, y in zip(weeks, weeks[1:]):
            if _week_distance(x, y) == 1 and any(t["tur"] == "tanitim" for _, t in items):
                extra.append({"seviye": HATASI, "kod": "P-TAKVIM-USTUSTE", "kural": "K15",
                              "mesaj": f"Aynı proje iki hafta üst üste tanıtılıyor: {proje} ({x} -> {y})",
                              "kanit": "", "yer": proje})

    if extra:
        for e in extra:
            if e["kural"] in overrides:
                e["seviye"] = overrides[e["kural"]]

    return posts, extra


def _week_distance(a: str, b: str) -> int:
    def parse(w):
        m = re.fullmatch(r"(\d{4})-W(\d{2})", w or "")
        return (int(m.group(1)), int(m.group(2))) if m else None
    pa, pb = parse(a), parse(b)
    if not pa or not pb:
        return -1
    return (pb[0] - pa[0]) * 52 + (pb[1] - pa[1])


def balance_findings(posts: list) -> list:
    counts = {"ipucu": 0, "tanitim": 0, "teknik": 0, "carousel": 0}
    for p in posts:
        counts[p["tur"]] = counts.get(p["tur"], 0) + 1
    total = max(len(posts), 1)
    return [{
        "seviye": BILGI, "kod": "P-DENGE", "kural": "K16",
        "mesaj": "İçerik sütunu dağılımı: " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
                 + f" (toplam {total}) · hedef: eğitici %40, tanıtım %10",
        "kanit": "", "yer": "takvim",
    }]


# --- Canlı link (K17) ------------------------------------------------------


def check_links(urls: list) -> list:
    findings = []
    for url in urls:
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "denetle-post/2"})
            with urllib.request.urlopen(req, timeout=6) as res:
                code = res.status
        except urllib.error.HTTPError as exc:
            code = exc.code
            if code in (403, 405, 501):
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "denetle-post/2"})
                    with urllib.request.urlopen(req, timeout=6) as res:
                        code = res.status
                except urllib.error.HTTPError as exc2:
                    code = exc2.code
                except (urllib.error.URLError, TimeoutError) as exc2:
                    findings.append((UYARI, f"Link yoklanamadı: {url} ({exc2})"))
                    continue
        except (urllib.error.URLError, TimeoutError) as exc:
            findings.append((HATASI, f"Link yoklanamadı, ağ hatası: {url} ({exc})"))
            continue
        if code in (404, 410):
            findings.append((HATASI, f"Link ölü ({code}): {url}"))
        elif code >= 500:
            findings.append((UYARI, f"Link sunucu hatası veriyor ({code}): {url}"))
    return findings


# --- Girdi toplama ---------------------------------------------------------


def collect_paths(targets: list) -> list:
    paths = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            paths.extend(sorted(x for x in p.rglob("*.md") if x.is_file()))
        elif p.is_file():
            paths.append(p)
    return paths


def print_human(result: dict) -> None:
    o = result["olcumler"]
    if result["profil"] == "takvim":
        print("=== Takvim Denetimi (K15/K16) ===")
        durum = "GEÇTİ" if result["sonuc"] == "GECTI" else "KALDI"
        print(f"Sonuç: {durum} ({result['hata']} hata, {result['uyari']} uyarı)\n")
    else:
        print(f"=== Post Kapısı: {result['dosya']} ===")
        print(f"Profil: {result['profil']} · {o['kelime']} kelime · {o['karakter']} karakter"
              f" · {o['hashtag']} hashtag" + (f" · {o['slayt']} slayt" if o.get("slayt") else "")
              + f" · ilk satır {o['ilk_satir_karakter']} karakter · CoV {o['cumle_cov']}")
        durum = "GEÇTİ" if result["sonuc"] == "GECTI" else "KALDI"
        print(f"Sonuç: {durum} ({result['hata']} hata, {result['uyari']} uyarı)\n")
    for level, title in ((HATASI, "HATA"), (UYARI, "UYARI"), (BILGI, "BİLGİ")):
        items = [f for f in result["bulgular"] if f["seviye"] == level]
        if not items:
            continue
        print(title)
        for f in items:
            yer = f" [{f['yer']}]" if f["yer"] else ""
            ezildi = " (ezildi)" if f.get("ezildi") else ""
            kanit = f" -> \"{f['kanit']}\"" if f["kanit"] else ""
            print(f"  [{f['kural']}/{f['kod']}]{yer}{ezildi} {f['mesaj']}{kanit}")
        print()


def load_config(path: str) -> dict:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Ayar dosyası kural kimliği -> seviye eşlemesi olmalı: {\"K12\": \"bilgi\"}")
    for k, v in data.items():
        if k not in KURALLAR:
            raise ValueError(f"Bilinmeyen kural: {k}. Geçerli: {', '.join(KURALLAR)}")
        if v not in (HATASI, UYARI, BILGI):
            raise ValueError(f"{k} için geçersiz seviye: {v}")
    return data


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Sosyal medya postu yayın kapısı (metnin yazarını tespit etmez)")
    parser.add_argument("paths", nargs="*", help="Post dosyaları ya da takvim dizini")
    parser.add_argument("--metin", help="Dosya yerine doğrudan post metni")
    parser.add_argument("--platform", help="linkedin | instagram | x (verilmezse frontmatter/dosya adından)")
    parser.add_argument("--tur", help="tanitim | teknik | ipucu | carousel (verilmezse dosya adı/kanaldan)")
    parser.add_argument("--takvim", help="Takvim dizini: postlar arası tekrar ve denge denetimi (K15/K16)")
    parser.add_argument("--config", help="Kural seviyesi ezen JSON dosyası: {\"K12\": \"bilgi\"}")
    parser.add_argument("--kural-kapat", help="Virgülle ayrılmış kural kimlikleri (bilgi seviyesine iner)")
    parser.add_argument("--canli", action="store_true", help="Kaynak/demo URL'lerini HTTP ile yokla (K17)")
    parser.add_argument("--json", action="store_true", help="Çıktıyı JSON ver")
    parser.add_argument("--katı", action="store_true", help="Uyarılar da kapıyı kapatır")
    args = parser.parse_args()

    if not args.paths and not args.metin and not args.takvim:
        parser.print_help()
        return 2

    try:
        overrides = load_config(args.config)
        for kural in (args.kural_kapat or "").split(","):
            kural = kural.strip().upper()
            if not kural:
                continue
            if kural not in KURALLAR:
                raise ValueError(f"Bilinmeyen kural: {kural}")
            overrides[kural] = BILGI
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 2

    results = []
    try:
        if args.metin:
            platform = resolve_platform(args.platform or "linkedin")
            results.append(audit_post(args.metin, platform, "metin", args.tur, overrides, args.katı))
        else:
            paths = collect_paths(args.paths)
            if args.takvim:
                paths = collect_paths([args.takvim])
            if not paths:
                print("Hata: denetlenecek post dosyası bulunamadı", file=sys.stderr)
                return 2
            for path in paths:
                raw = path.read_text(encoding="utf-8")
                fm, _ = split_frontmatter(raw)
                platform = resolve_platform(args.platform or fm.get("kanal") or platform_from_name(path))
                result = audit_post(raw, platform, path.name, args.tur, overrides, args.katı)
                if args.canli:
                    urls = set(URL_RE.findall(raw))
                    urls |= set(re.findall(r"https?://\S+", fm.get("kaynak") or ""))
                    result["bulgular"].extend(
                        {"seviye": level, "kod": "P-LINK-SAGLIK", "kural": "K17",
                         "mesaj": msg, "kanit": "", "yer": "canlı"} for level, msg in check_links(sorted(urls)))
                    result["hata"] = sum(1 for f in result["bulgular"] if f["seviye"] == HATASI)
                    result["uyari"] = sum(1 for f in result["bulgular"] if f["seviye"] == UYARI)
                    result["sonuc"] = "KALDI" if result["hata"] else "GECTI"
                results.append(result)
    except (ValueError, OSError) as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 2

    takvim_posts = []
    if args.takvim:
        try:
            takvim_posts, extra = audit_calendar(
                collect_paths([args.takvim]),
                lambda p, fm: args.platform or fm.get("kanal") or platform_from_name(p),
                overrides)
        except (ValueError, OSError) as exc:
            print(f"Hata: {exc}", file=sys.stderr)
            return 2
        if extra or takvim_posts:
            results.append({
                "dosya": "TAKVİM",
                "platform": "-",
                "platform_label": "Takvim",
                "profil": "takvim",
                "sonuc": "KALDI" if any(f["seviye"] == HATASI for f in extra) else "GECTI",
                "hata": sum(1 for f in extra if f["seviye"] == HATASI),
                "uyari": sum(1 for f in extra if f["seviye"] == UYARI),
                "bilgi": sum(1 for f in extra if f["seviye"] == BILGI) + 1,
                "olcumler": {"karakter": 0, "kelime": 0, "hashtag": 0, "slayt": 0,
                             "ilk_satir_karakter": 0, "cumle_cov": 0, "kalip_sinyali": 0},
                "bulgular": extra + balance_findings(takvim_posts),
            })

    if args.json:
        print(json.dumps({"surum": SURUM, "kurallar": KURALLAR, "dosyalar": results},
                         ensure_ascii=False, indent=2))
    else:
        for r in results:
            print_human(r)

    blocked = any(r["hata"] for r in results) or (args.katı and any(r["uyari"] for r in results))
    if len(results) > 1 and not args.json:
        postlar = [r for r in results if r["profil"] != "takvim"]
        temiz = sum(1 for r in postlar if r["sonuc"] == "GECTI")
        ek = " + takvim denetimi" if len(postlar) != len(results) else ""
        print(f"Özet: {len(postlar)} post{ek}, {temiz} geçti, {len(postlar) - temiz} kaldı")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
