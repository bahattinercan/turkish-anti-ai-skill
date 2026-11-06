#!/usr/bin/env python3
"""
detect_tr_ai.py - Deterministik Türkçe AI Yazım İzi (AI Slop, Translationese & TDK) Tarayıcısı
Kullanım: python3 scripts/detect_tr_ai.py <dosya_yolu.md> [--json]
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

TIER1_PATTERNS = [
    (r"\byadsınamaz\b|\binkar\s+edilemez\b", "Tier-1 Klişe: 'yadsınamaz / inkar edilemez' (undeniable calque)"),
    (r"\b[aâ]deta\b", "Tier-1 Klişe: 'âdeta / adeta' (aşırı benzetme zarfı)"),
    (r"\bderinlemesine\s+(?:inmek|incelemek|bakmak|ele\s+almak|analiz)\b|\bmercek\s+altına\s+al", "Tier-1 Klişe: 'derinlemesine inmek / mercek altına almak' (delve into calque)"),
    (r"\bkritik\s+(?:bir\s+)?(?:rol\s+oyna|öneme\s+sahip)|\bhayati\s+(?:bir\s+)?öneme\s+sahip", "Tier-1 Klişe: 'kritik bir rol oynamak / öneme sahip olmak'"),
    (r"\bgeniş\s+bir\s+yelpaze|\bzengin\s+bir\s+(?:doku|mozaik)\b", "Tier-1 Klişe: 'geniş bir yelpaze / zengin bir doku-mozaik'"),
    (r"\bsadece\s+[^,.!?]+?\s+değil,\s*aynı\s+zamanda\b|\byalnızca\s+[^,.!?]+?\s+değil,\s*aynı\s+zamanda\b", "P0 Yapısal: 'sadece X değil, aynı zamanda Y' (negatif paralellik)"),
    (r"\byalnızca\s+[^,.!?]+?\s+olmakla\s+kalmayıp\b|\bsadece\s+[^,.!?]+?\s+göstermekle\s+kalma", "P0 Yapısal: 'yalnızca X olmakla kalmayıp' (not only... but also)"),
    (r"\bgünümüzün\s+hızla\s+değişen\b|\bdijitalleşen\s+çağımızda\b", "P0 Sahneleme: 'günümüzün hızla değişen...' (boş giriş klişesi)"),
    (r"\bçığır\s+açan\b|\bdönüm\s+noktası\w*\b|\bkilometre\s+taşı\w*\b", "Tier-1 Şişirme: 'çığır açan / dönüm noktası / kilometre taşı'"),
    (r"\bpotansiyelini\s+ortaya\s+çıkar|\bbir\s+üst\s+seviyeye\s+taşı", "Tier-1 Klişe: 'potansiyelini ortaya çıkarmak / bir üst seviyeye taşımak'"),
    (r"\ben\s+büyük\s+(?:kanıtıdır|göstergesidir)\b", "Tier-1 Şişirme: 'en büyük kanıtıdır / göstergesidir' (testament to calque)"),
    (r"\bkusursuz\s+bir\s+şekilde\b|\bpürüzsüz\s+bir\s+şekilde\b", "Tier-1 Klişe: 'kusursuz / pürüzsüz bir şekilde' (seamlessly calque)"),
]

TIER2_AND_SYNTAX_PATTERNS = [
    (r"\bbununla\s+birlikte\b|\böte\s+yandan\b", "Tier-2 Geçiş: 'bununla birlikte / öte yandan' (moreover/however)"),
    (r"\bbelirtmek\s+gerekir\s+ki\b|\bunutulmamalıdır\s+ki\b|\bvurgulamak\s+(?:gerekir|önemlidir)\s+ki\b", "Tier-2 Dolgu: 'belirtmek / vurgulamak gerekir ki'"),
    (r"\bsöz\s+konusu\b|\bbu\s+bağlamda\b|\bbu\s+doğrultuda\b|\bbahsi\s+geçen\b", "Tier-2 Bürokratik: 'söz konusu / bu bağlamda / bu doğrultuda'"),
    (r"\bbütüncül\s+(?:bir\s+)?yaklaşım\b|\bparadigma\s+değişimi\b|\bsinerji\s+yarat", "Tier-2 Jargon: 'bütüncül yaklaşım / paradigma değişimi / sinerji'"),
    (r"\bsonuç\s+olarak\b|\bözetlemek\s+gerekirse\b|\bson\s+tahlilde\b", "Tier-2 Kapanış: 'sonuç olarak / özetlemek gerekirse'"),
    # 'tarafından' tek başına doğru Türkçedir ("Köprü Mimar Sinan tarafından yapıldı"). Yalnızca kof eylemle
    # ya da yazarın kendi kurumu eyleyen olduğunda bayraklanır.
    (r"\btarafından\s+(?:gerçekleştiril|sağlan|icra\s+edil)|\b(?:ekibimiz|şirketimiz|kurumumuz|tarafımız)\s+tarafından\b", "P1 Sentaks: Edilgen çatı ('tarafından') + kof eylem ya da yazarın kendi kurumu"),
    (r"\b(?:göstermektedir|belirtmektedir|kanıtlamaktadır|ortaya\s+koymaktadır)\s+ki\b", "P1 Sentaks: Hint-Avrupa tipi '...-mektedir ki' yan cümle kopyası"),
    # 'Sıfat + bir + ad' tek başına doğaldır ("derin bir iz bıraktı"). Yalnızca kalıplaşmış birleşik eylemin içindeki 'bir' bayraklanır.
    (r"\b(?:büyük|yüksek|kritik|ciddi|önemli|hayati)\s+bir\s+(?:önem\s+taşı|artış\s+göster|rol\s+oyna|ivme\s+kazan|önem\s+arz)", "P1 Sentaks: Kalıplaşmış birleşik eylemde gereksiz 'bir' (a/an calque)"),
    (r"\b(?:uç\s+nokta(?:lar|larda|lara|ları)?|olay\s+güdümlü|ara\s+katman|çekme\s+isteği)\b", "P2 Terminoloji: Zorlama teknik terim çevirisi ('uç nokta / olay güdümlü / ara katman')"),
    (r"\bev\s+sahipliği\s+yapmakta|\bkatkıda\s+bulunmakta", "P1 Kof Fiil: '-mAktAdIr' ile şişirilmiş 'ev sahipliği yapmak / katkıda bulunmak'"),
]

PUNCTUATION_AND_TDK_PATTERNS = [
    (r"—", "P2 Noktalama: Uzun çizgi (em-dash '—') kullanımı (TDK diyalog dışında yasaklar)"),
    (r"\w+[–]\w+", "P2 Noktalama: Aralıkta orta çizgi (en-dash '–') kullanımı (TDK kısa çizgi '-' şart koşar)"),
    (r",\s*(?:ve|veya|yahut)\b|\b(?:ve|veya|yahut),", "P2 TDK Noktalama: 've / veya / yahut' bağlacından önce veya sonra virgül (TDK: konmaz)"),
    (r",\s*(?:ama|fakat|lakin|ya da)\b", "P2 Üslup: 'ama / fakat / lakin / ya da' öncesi refleks virgül (TDK kuralı değil, İngilizce ', but' alışkanlığı)"),
    (r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", "P2 TDK Saat Hatası: Saat arasında iki nokta (':') kullanımı (TDK tek nokta '.' şart koşar, örn: 14.30)"),
    (r"%\d+\.\d+", "P2 TDK Sayı Hatası: Yüzde ondalık ayracı olarak nokta kullanımı (TDK virgül şart koşar, örn: %112,5)"),
    (r"\b(?:birşey|herşey|hiçbirşey|yada|bir çok|bir kaç|pekçok|ard arda|yanısıra|önsöz|önyargı|işbirliği|farketmek|terketmek|halbu ki|oysa ki)\b", "P2 TDK İmla Hatası: Birleşik/ayrı yazılan kelime hatası"),
]

# Büyük/küçük harf ve Türkçe ı/i ayrımına duyarlı fonetik ek hataları
CASE_SENSITIVE_PATTERNS = [
    (r"\b(?:cache'ı|cache'de|cache'dan|SQL'ı|SQL'da|SQL'dan|JSON'i|JSON'de|queue'ya|React'ı|React'da|Node\.js'ı|Node\.js'da|GitHub'de|Google'de|URL'ı|URL'da)\b", "P2 Fonetik Ek Hatası: Yabancı terime Türkçe okunuşu yerine yazılışına göre ek getirilmesi"),
]


# Saate gelen ek, saatin Türkçe okunuşunun son sözcüğüne uyar (TDK örnekleri: 13.00'te, 11.00'de, 17.30'da, 09.15'te).
_UNITS = {1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "beş", 6: "altı", 7: "yedi", 8: "sekiz", 9: "dokuz"}
_TENS = {1: "on", 2: "yirmi", 3: "otuz", 4: "kırk", 5: "elli"}
_BACK_VOWELS = set("aıou")
_FRONT_VOWELS = set("eiöü")
_HARD_CONSONANTS = set("fstkçşhp")
TIME_SUFFIX_RE = re.compile(r"\b(\d{1,2})\.(\d{2})'(d[ae]n?|t[ae]n?)\b")


def _last_word_of_number(n: int) -> str:
    if n == 0:
        return "sıfır"
    return _UNITS[n % 10] if n % 10 else _TENS[n // 10]


def expected_time_suffix(hour: int, minute: int, ablative: bool) -> str:
    """'14.30' + bulunma -> 'da' (otuzda). Dakika 00 ise saat okunur."""
    word = _last_word_of_number(minute if minute else hour)
    last_vowel = next(ch for ch in reversed(word) if ch in _BACK_VOWELS | _FRONT_VOWELS)
    vowel = "a" if last_vowel in _BACK_VOWELS else "e"
    consonant = "t" if word[-1] in _HARD_CONSONANTS else "d"
    return consonant + vowel + ("n" if ablative else "")


def time_suffix_findings(text: str) -> list:
    findings = []
    for m in TIME_SUFFIX_RE.finditer(text):
        hour, minute, suffix = int(m.group(1)), int(m.group(2)), m.group(3)
        if hour > 24 or minute > 59:
            continue
        expected = expected_time_suffix(hour, minute, suffix.endswith("n"))
        if suffix != expected:
            findings.append({
                "rule": f"P2 TDK Saat Eki Hatası: Ek, saatin okunuşuna uymalı ('{m.group(1)}.{m.group(2)}'{expected}')",
                "match": m.group(0),
                "position": m.start(),
            })
    return findings


# Register'a göre '-mAktAdIr' hedef aralıkları (100 kelimede). Değerler SKILL.md register
# tablosundaki dozajın sayısal karşılığıdır. Korpus ölçümüyle kalibre edilmemiş başlangıç değerleridir.
REGISTER_PROFILES = {
    "blog-deneme": {"label": "Blog / Deneme / Sosyal Medya", "mektedir_min": 0.0, "mektedir_max": 0.5},
    "teknik": {"label": "Teknik / Mühendislik", "mektedir_min": 0.0, "mektedir_max": 1.0},
    "kurumsal": {"label": "Kurumsal / SaaS / İş İletişimi", "mektedir_min": 0.0, "mektedir_max": 1.0},
    "akademik-resmi": {"label": "Akademik / Resmî / Hukuki", "mektedir_min": 0.5, "mektedir_max": 2.5},
    "edebi-anlati": {"label": "Edebî / Anlatı", "mektedir_min": 0.0, "mektedir_max": 0.5},
}
DEFAULT_PROFILE = {"label": "Register belirtilmedi (genel eşik)", "mektedir_min": 0.0, "mektedir_max": 2.5}
REGISTER_ALIASES = {"blog": "blog-deneme", "deneme": "blog-deneme", "akademik": "akademik-resmi",
                    "resmi": "akademik-resmi", "hukuki": "akademik-resmi", "edebi": "edebi-anlati",
                    "anlati": "edebi-anlati", "saas": "kurumsal"}

# Art arda aynı cümle sonu: bu sayıda ve üstünde ardışık cümle aynı ek ailesiyle biterse uyarı ver.
REPEATED_ENDING_LIMIT = 3


def resolve_register(register):
    if not register:
        return None
    key = REGISTER_ALIASES.get(register.lower(), register.lower())
    if key not in REGISTER_PROFILES:
        raise ValueError(f"Bilinmeyen register: {register}. Seçenekler: {', '.join(REGISTER_PROFILES)}")
    return key


def sentence_ending_class(sentence: str) -> str:
    """Cümlenin son kelimesini koşulaç ailesine göre sınıflar."""
    words = re.findall(r"\w+", sentence)
    if not words:
        return "diger"
    last = words[-1].lower()
    if re.search(r"m[ae]kt[ae]d[ıi]r$", last):
        return "-mAktAdIr"
    if re.search(r"m[ıiuü]şt[ıiuü]r$", last):
        return "-mIştIr"
    if re.search(r"[dt][ıiuü]r$", last):
        return "-DIr"
    return "diger"


def max_repeated_ending_run(sentences: list) -> tuple:
    best_run, best_class, run, prev = 0, None, 0, None
    for sent in sentences:
        cls = sentence_ending_class(sent)
        if cls != "diger" and cls == prev:
            run += 1
        elif cls != "diger":
            run = 1
        else:
            run = 0
        prev = cls
        if run > best_run:
            best_run, best_class = run, cls
    return best_run, best_class


def split_turkish_sentences(text: str) -> list:
    """Saat (14.30), ondalık sayı (3.14) ve teknik terim (Node.js) noktalarını bölmeden cümleleri ayırır."""
    protected = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", text)
    protected = re.sub(r"\b(Node|Vue|Next|Nuxt)\.js", r"\1<DOT>js", protected, flags=re.IGNORECASE)
    raw_sentences = re.split(r"[.!?]+(?:\s+|$)", protected)
    return [s.replace("<DOT>", ".").strip() for s in raw_sentences if len(s.strip().split()) > 1]


def analyze_text(text: str, register: str = None) -> dict:
    register_key = resolve_register(register)
    profile = REGISTER_PROFILES[register_key] if register_key else DEFAULT_PROFILE
    findings = []
    for pattern, label in TIER1_PATTERNS + TIER2_AND_SYNTAX_PATTERNS + PUNCTUATION_AND_TDK_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            findings.append({
                "rule": label,
                "match": match.group(0),
                "position": match.start(),
            })

    for pattern, label in CASE_SENSITIVE_PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append({
                "rule": label,
                "match": match.group(0),
                "position": match.start(),
            })

    findings.extend(time_suffix_findings(text))

    words = re.findall(r"\b\w+\b", text)
    word_count = max(len(words), 1)
    mektedir_count = len(re.findall(r"\w+m[ae]kt[ae]d[ıi]r\b", text, flags=re.IGNORECASE))
    mektedir_per_100 = round((mektedir_count / word_count) * 100, 2)

    sentences = split_turkish_sentences(text)
    sent_lengths = [len(s.split()) for s in sentences]
    if len(sent_lengths) >= 3:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((x - mean_len) ** 2 for x in sent_lengths) / len(sent_lengths)
        cov = round(math.sqrt(variance) / mean_len, 2) if mean_len > 0 else 0.0
    else:
        cov = 0.5

    run_len, run_class = max_repeated_ending_run(sentences)
    mektedir_in_range = profile["mektedir_min"] <= mektedir_per_100 <= profile["mektedir_max"]

    return {
        "register": register_key,
        "register_label": profile["label"],
        "mektedir_target_range": [profile["mektedir_min"], profile["mektedir_max"]],
        "mektedir_in_range": mektedir_in_range,
        "repeated_ending_max_run": run_len,
        "repeated_ending_class": run_class,
        "repeated_ending_warning": run_len >= REPEATED_ENDING_LIMIT,
        "word_count": len(words),
        "sentence_count": len(sentences),
        "sentence_lengths": sent_lengths,
        "sentence_length_cov": cov,
        "low_burstiness_warning": cov < 0.35 and len(sentences) >= 3,
        "mektedir_per_100_words": mektedir_per_100,
        "high_mektedir_warning": mektedir_per_100 > profile["mektedir_max"],
        "total_flags": len(findings),
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser(description="Türkçe AI Yazım İzi (AI Slop) Tarayıcısı")
    parser.add_argument("file", help="Taranacak metin veya Markdown dosyası")
    parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında ver")
    parser.add_argument("--register", help=f"Metin türü: {', '.join(REGISTER_PROFILES)}. Verilirse '-mAktAdIr' hedefi buna göre seçilir.")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Hata: {args.file} bulunamadı.", file=sys.stderr)
        sys.exit(2)

    try:
        report = analyze_text(path.read_text(encoding="utf-8"), args.register)
    except ValueError as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"=== Turkish Anti-AI Denetim Raporu: {path.name} ===")
        print(f"Kelime Sayısı: {report['word_count']} | Cümle Sayısı: {report['sentence_count']}")
        print(f"Cümle Uzunluğu Değişim Katsayısı (Burstiness CoV): {report['sentence_length_cov']} (İnsan hedefi: >= 0.40)")
        lo, hi = report["mektedir_target_range"]
        print(f"Register: {report['register_label']}")
        print(f"'-mAktAdIr' Yoğunluğu (100 kelimede): {report['mektedir_per_100_words']} | Hedef: {lo}-{hi} | {'Uygun' if report['mektedir_in_range'] else 'Hedef dışı'}")
        run_note = f" ({report['repeated_ending_class']})" if report["repeated_ending_class"] else ""
        print(f"Art Arda Aynı Cümle Sonu (en uzun seri): {report['repeated_ending_max_run']}{run_note} | Sınır: {REPEATED_ENDING_LIMIT} altı | {'Uyarı' if report['repeated_ending_warning'] else 'Uygun'}")
        print(f"Toplam Yakalanan AI/TDK Sinyali: {report['total_flags']}")
        for item in report["findings"]:
            print(f"  - [{item['rule']}] -> \"{item['match']}\"")


if __name__ == "__main__":
    main()
