#!/usr/bin/env python3
"""
run_tests.py - turkish-anti-ai-skill Kapsamlı Doğrulama ve Regresyon Test Koşucusu
Çalıştırma: python3 scripts/run_tests.py
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from detect_tr_ai import analyze_text  # noqa: E402

DIGIT_RE = re.compile(r"\d+")
# Kaynakta olmayan miktar/abartı bildiren kelimeler: "birçok" -> "yüzlerce" dönüşümü uydurmadır.
MAGNITUDE_RE = re.compile(
    r"\b(?:yüzlerce|binlerce|milyonlarca|milyarlarca|onlarca|düzinelerce|bütün|tüm|herkes|hiçbiri)\w*",
    re.IGNORECASE,
)


def fabrication_findings(case: dict) -> list:
    """Olgusal sadakat kilidinin testi: çıktı, kaynakta olmayan bilgi eklememeli.

    Kontrol edilenler: yeni sayı, yeni miktar/abartı kelimesi, senaryoda açıkça yasaklanan
    ifadeler ve kaybolmaması gereken ihtiyat kipleri.
    """
    source = case["input_ai"]
    output = case["output_human"]
    problems = []

    added_numbers = sorted(set(DIGIT_RE.findall(output)) - set(DIGIT_RE.findall(source)))
    if added_numbers:
        problems.append(f"kaynakta olmayan sayı: {', '.join(added_numbers)}")

    src_magnitudes = {m.lower() for m in MAGNITUDE_RE.findall(source)}
    added_magnitudes = sorted({m.lower() for m in MAGNITUDE_RE.findall(output)} - src_magnitudes)
    if added_magnitudes:
        problems.append(f"kaynakta olmayan miktar/abartı sözü: {', '.join(added_magnitudes)}")

    forbidden = [token for token in case.get("must_not_add", []) if token.lower() in output.lower()]
    if forbidden:
        problems.append(f"yasaklı ekleme: {', '.join(forbidden)}")

    missing_hedges = [token for token in case.get("must_preserve_hedges", []) if token.lower() not in output.lower()]
    if missing_hedges:
        problems.append(f"kaybolan ihtiyat kipl: {', '.join(missing_hedges)}")

    return problems


def test_package_integrity() -> list:
    results = []

    # 1. SKILL.md varlığı, YAML frontmatter ve <500 satır kontrolü
    skill_path = ROOT / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    lines = skill_text.splitlines()
    has_frontmatter = skill_text.startswith("---\n") and "\n---\n" in skill_text[4:]
    has_name = "name: turkish-anti-ai-skill" in skill_text
    has_desc = "description:" in skill_text
    under_500_lines = len(lines) < 500
    no_em_dash_in_skill = "—" not in skill_text and "–" not in skill_text

    results.append({
        "check": "SKILL.md Agent Skills v1.0 Spesifikasyon Uyumu (<500 satır, YAML, tire yasağı)",
        "passed": has_frontmatter and has_name and has_desc and under_500_lines and no_em_dash_in_skill,
        "detail": f"{len(lines)} satır | Frontmatter: {has_frontmatter} | Em/En-Dash: {'Yok' if no_em_dash_in_skill else 'Var'}",
    })

    # 2. Referans dosyalarının varlığı ve SKILL.md içinden bağlantı kontrolü
    expected_refs = [
        "sentaks-ve-morfoloji.md",
        "ai-turkcesi-sozlugu.md",
        "tdk-ve-noktalama.md",
        "register-ve-ornekler.md",
        "sosyal-medya.md",
    ]
    missing_refs = [r for r in expected_refs if not (ROOT / "references" / r).exists() or r not in skill_text]
    results.append({
        "check": "Progressive Disclosure Referans Dosyaları (references/*.md) Bütünlüğü",
        "passed": len(missing_refs) == 0,
        "detail": f"{len(expected_refs) - len(missing_refs)}/{len(expected_refs)} referans dosyası mevcut ve SKILL.md içinden bağlı"
                  if not missing_refs else f"Eksik: {missing_refs}",
    })

    # 3. dist/ ve skills/turkish-anti-ai-skill/ senkronizasyon (Zero Drift) kontrolü
    dist_file = ROOT / "dist" / "turkish-anti-ai-skill.full.md"
    pkg_skill = ROOT / "skills" / "turkish-anti-ai-skill" / "SKILL.md"
    src_refs = {p.name: p.read_bytes() for p in (ROOT / "references").glob("*.md")}
    pkg_refs_dir = ROOT / "skills" / "turkish-anti-ai-skill" / "references"
    pkg_refs = {p.name: p.read_bytes() for p in pkg_refs_dir.glob("*")} if pkg_refs_dir.exists() else {}
    refs_synced = src_refs == pkg_refs
    drift_ok = (dist_file.exists() and pkg_skill.exists()
                and pkg_skill.read_text(encoding="utf-8") == skill_text and refs_synced)
    results.append({
        "check": "Single-Source-of-Truth Senkronizasyonu (dist/ ve skills/ Zero-Drift)",
        "passed": drift_ok,
        "detail": f"dist boyutu: {dist_file.stat().st_size if dist_file.exists() else 0} byte | SKILL.md + references/ ({len(src_refs)} dosya) skills/ ile birebir: {drift_ok}",
    })

    # 4. Çoklu ajan adaptörleri (.cursor/rules/*.mdc, plugin.json, AGENTS.md, CLAUDE.md)
    mdc_file = ROOT / ".cursor" / "rules" / "turkish-anti-ai-skill.mdc"
    plugin_file = ROOT / ".claude-plugin" / "plugin.json"
    plugin_valid = False
    if plugin_file.exists():
        try:
            data = json.loads(plugin_file.read_text(encoding="utf-8"))
            plugin_valid = data.get("name") == "turkish-anti-ai-skill"
        except Exception:
            plugin_valid = False

    adapters_ok = mdc_file.exists() and plugin_valid and (ROOT / "AGENTS.md").exists() and (ROOT / "CLAUDE.md").exists()
    results.append({
        "check": "Çoklu Ajan Adaptörleri (Cursor .mdc, Claude plugin.json, AGENTS.md, CLAUDE.md)",
        "passed": adapters_ok,
        "detail": f"Cursor .mdc: {mdc_file.exists()} | Claude plugin.json: {plugin_valid} | AGENTS.md: True",
    })

    return results


def test_detector_rules() -> list:
    """Dedektörün kural davranışı: düzeltilen yanlış pozitifler geri dönerse burada kırmızı olur."""
    from detect_tr_ai import COV_MECHANICAL, COV_TARGET, analyze_text, expected_time_suffix, sentence_ending_class

    results = []

    def check(label, passed, detail):
        results.append({"check": label, "passed": bool(passed), "detail": detail})

    fenced = analyze_text("Örnek kod:\n\n```python\nx = a — b  # , ve\n```\n")
    check("Dedektör: kod bloğu içeriği taranmaz (em-dash / virgül)", fenced["total_flags"] == 0,
          f"kod bloğu bayrakları: {fenced['total_flags']} (beklenen: 0)")

    inline = analyze_text("Şu `a — b` komutunu çalıştır.")
    check("Dedektör: satır içi kod taranmaz", inline["total_flags"] == 0,
          f"satır içi kod bayrakları: {inline['total_flags']} (beklenen: 0)")

    prose = analyze_text("Bu bir deneme — ve devamı var.")
    check("Dedektör: düz metindeki em-dash hâlâ yakalanır", prose["total_flags"] == 1,
          f"düz metin bayrakları: {prose['total_flags']} (beklenen: 1)")

    lookalike = [w for w in ("yıllardır", "aylardır", "sabahtır", "bugündür")
                 if sentence_ending_class(w) != "diger"]
    check("Dedektör: '-DIr' görünümlü süre belirteçleri bildirme eki sayılmaz", not lookalike,
          f"yanlış sınıflananlar: {lookalike or 'yok'}")

    real_dir = analyze_text("Kitap masadadır. Hava soğuktur. Kural açıktır. Sonra her şey değişti.")
    check("Dedektör: gerçek '-DIr' zinciri uyarıyı üretmeye devam eder", real_dir["repeated_ending_warning"],
          f"seri: {real_dir['repeated_ending_max_run']} ({real_dir['repeated_ending_class']})")

    legal = analyze_text("Söz konusu taşınmaz üzerinde ipotek bulunmamaktadır. Bu bağlamda tapu kaydı esas alınır. "
                         "Sonuç olarak işlem tamamdır.", "akademik-resmi")
    check("Dedektör: akademik/hukuki register'da yerleşik kalıplar puanlanmaz",
          legal["total_flags"] == 0 and legal["informational_count"] >= 3,
          f"sinyal: {legal['total_flags']} | bilgi: {legal['informational_count']} (beklenen: 0 sinyal, >=3 bilgi)")

    blog = analyze_text("Söz konusu taşınmaz üzerinde ipotek bulunmamaktadır.", "blog-deneme")
    check("Dedektör: aynı kalıp blog register'ında sinyal kalır", blog["total_flags"] == 1,
          f"blog sinyali: {blog['total_flags']} (beklenen: 1)")

    small = analyze_text("Söz konusu taşınmaz üzerinde ipotek bulunmamaktadır.")
    check("Dedektör: küçük örneklemde '-mAktAdIr' yoğunluk uyarısı verilmez",
          small["high_mektedir_warning"] is False and small["mektedir_sample_sufficient"] is False,
          f"örneklem yeterli: {small['mektedir_sample_sufficient']} | uyarı: {small['high_mektedir_warning']}")

    check("Dedektör: saat eki okunuşa göre hesaplanır",
          expected_time_suffix(14, 30, False) == "da" and expected_time_suffix(11, 0, False) == "de"
          and expected_time_suffix(9, 15, False) == "te",
          f"14.30 -> {expected_time_suffix(14, 30, False)}, 11.00 -> {expected_time_suffix(11, 0, False)}, "
          f"09.15 -> {expected_time_suffix(9, 15, False)}")

    check("Dedektör: CoV eşikleri tek kaynaktan ve SKILL.md ile aynı",
          COV_MECHANICAL < COV_TARGET and COV_TARGET == 0.40 and COV_MECHANICAL == 0.35,
          f"mekanik: {COV_MECHANICAL} < hedef: {COV_TARGET}")

    dirty = fabrication_findings({
        "input_ai": "Birçok ekip bunu yapıyor.",
        "output_human": "Yüzlerce ekip 2027'de bunu yaptı ve kesinti yaşanmadı.",
    })
    clean = fabrication_findings({"input_ai": "Birçok ekip bunu yapıyor.", "output_human": "Birçok ekip bunu yapıyor."})
    check("Sadakat kilidi: eklenen sayı, miktar sözü ve yasaklı ifade yakalanır",
          len(dirty) >= 2 and not clean,
          f"kirli metinde: {len(dirty)} problem | temiz metinde: {len(clean)} problem")

    return results


def test_eval_scenarios() -> list:
    evals_data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
    scenario_results = []

    for case in evals_data["test_cases"]:
        before_stats = analyze_text(case["input_ai"], case["register"])
        after_stats = analyze_text(case["output_human"], case["register"])

        if case["mode"] == "control":
            # False-positive kontrolü: Doğal metinde 0 bayrak çıkmalı
            passed = before_stats["total_flags"] == 0 and after_stats["total_flags"] == 0
        else:
            flags_caught = before_stats["total_flags"] >= case["expected_min_before_flags"]
            after_clean = after_stats["total_flags"] == 0
            mektedir_ok = after_stats["mektedir_per_100_words"] <= case["max_after_mektedir"]
            cov_ok = after_stats["sentence_length_cov"] >= case["min_after_cov"]
            missing_tokens = [tok for tok in case["must_preserve_tokens"] if tok not in case["output_human"]]
            fidelity_ok = len(missing_tokens) == 0
            register_dose_ok = after_stats["mektedir_in_range"]
            no_repeated_endings = not after_stats["repeated_ending_warning"]
            # Bu satır eskiden yalnızca "token var mı" bakıyordu; eklenen bilgiyi yakalamıyordu.
            fabrication_problems = fabrication_findings(case)
            passed = (flags_caught and after_clean and mektedir_ok and cov_ok and fidelity_ok
                      and register_dose_ok and no_repeated_endings and not fabrication_problems)

        missing_tokens = [tok for tok in case["must_preserve_tokens"] if tok not in case["output_human"]]
        fabrication_problems = fabrication_findings(case)
        scenario_results.append({
            "id": case["id"],
            "title": case["title"],
            "register": case["register"],
            "mode": case["mode"],
            "before_flags": before_stats["total_flags"],
            "after_flags": after_stats["total_flags"],
            "before_mektedir": before_stats["mektedir_per_100_words"],
            "after_mektedir": after_stats["mektedir_per_100_words"],
            "before_cov": before_stats["sentence_length_cov"],
            "before_run": before_stats["repeated_ending_max_run"],
            "after_run": after_stats["repeated_ending_max_run"],
            "target_range": after_stats["mektedir_target_range"],
            "after_cov": after_stats["sentence_length_cov"],
            "fidelity_preserved": len(missing_tokens) == 0,
            "missing_tokens": missing_tokens,
            "fabrication_problems": fabrication_problems,
            "passed": passed,
            "caught_examples": [f["match"] for f in before_stats["findings"][:6]],
        })

    return scenario_results


def test_post_gate() -> list:
    """Sosyal medya kapısı (scripts/denetle_post.py): yayın öncesi kuralların regresyon testi."""
    from denetle_post import audit_post, PLATFORMS, resolve_platform

    results = []

    def check(label, passed, detail):
        results.append({"check": label, "passed": bool(passed), "detail": detail})

    good = """---
proje: bakkal
tip: B
hafta: 2026-W50
kanal: linkedin
kaynak: private link yok
gizlilik: kontrol edildi
---

# Gövde

Mahalle bakkalı için çevrimdışı bir kasa yazdım: satış, stok, alış ve veresiye. Sunucu yok.

Veresiye ayrı bir ekran değil. Müşteri kartı, borç ve ödeme geçmişi aynı yerde duruyor.

Gün sonu tek düğme. Kasa kapanışı nakit, kart ve veresiyeyi tek ekranda topluyor, fiş PDF olarak çıkıyor.

On sekiz tablo, 233 test ve stok mutabakatı tek komutla doğrulanıyor.

# CTA

Bakkal işleten birini tanıyorsan yorumda etiketle; kasa kapanışı ekranını DM'den göstereyim.

# Hashtag

#bakkal #perakende #yerliyazılım

# Teknik doğruluk notu

- 18 tablo, 233 test
"""
    good_result = audit_post(good, "linkedin", "iyi-post.md")
    check("Post kapısı: temiz post hata üretmez", good_result["hata"] == 0,
          f"hata: {good_result['hata']} | uyarı: {good_result['uyari']}"
          f" | kodlar: {[f['kod'] for f in good_result['bulgular'] if f['seviye'] == 'hata']}")

    bad = """---
proje: ornek
tip: B
hafta: 2026-W50
kanal: linkedin
kaynak: private link yok
gizlilik: gerekmiyor
---

# Gövde

Günümüzün hızla değişen dünyasında inovasyon kaçınılmaz hale gelmiştir.
🚀 Gururla duyuruyoruz ki yeni ürünümüz yayında!
🔥 Sadece hız değil, aynı zamanda güvenilirlik sunuyoruz.
💡 Kritik bir rol oynayan bu çözüm, 450 müşteri tarafından tercih edilmektedir.

# CTA

Düşüncelerinizi yorumlarda paylaşın, beğenin, kaydedin, paylaşın!

# Hashtag

#inovasyon #teknoloji #gelecek #girişimcilik #yazılım #başarı

# Teknik doğruluk notu

- 12 tablo, 233 test
"""
    bad_result = audit_post(bad, "linkedin", "kotu-post.md")
    codes = {f["kod"] for f in bad_result["bulgular"] if f["seviye"] == "hata"}
    expected_codes = {"P-HOOK-KLISE", "P-HASHTAG-COK", "P-GIZLILIK", "P-SAYI-UYDURMA", "D-P0-Yapısal"}
    check("Post kapısı: AI kalıbı, hashtag, gizlilik ve uydurma sayı kapıyı kapatır",
          bad_result["sonuc"] == "KALDI" and expected_codes <= codes,
          f"sonuç: {bad_result['sonuc']} | eksik kodlar: {sorted(expected_codes - codes)}")

    long_post = "# Gövde\n\n" + ("Kasa kapanışı tek ekranda toplanıyor. " * 100) + "\n\n# Hashtag\n\n#kasa #bakkal\n"
    long_result = audit_post(long_post, "linkedin", "uzun-post.md")
    check("Post kapısı: platform karakter sınırı uygulanır",
          any(f["kod"] == "P-UZUNLUK" for f in long_result["bulgular"]),
          f"{long_result['olcumler']['karakter']} karakter / sınır {PLATFORMS['linkedin']['max_chars']}")

    quoted = audit_post(good.replace("fiş PDF olarak çıkıyor.",
                                     "defterdeki \"Ahmet 250 lira\" satırı hareket listesine dönüşüyor."),
                        "linkedin", "alintili-post.md")
    check("Post kapısı: alıntı içindeki sayı hata değil uyarı olur",
          quoted["hata"] == 0 and any(f["kod"] == "P-SAYI-ALINTI" for f in quoted["bulgular"]),
          f"hata: {quoted['hata']} | kodlar: {[f['kod'] for f in quoted['bulgular']]}")

    check("Post kapısı: platform takma adları çözülür (ig -> instagram)",
          resolve_platform("ig") == "instagram" and resolve_platform("li") == "linkedin",
          f"ig -> {resolve_platform('ig')}")

    # --- Faz 1: carousel ---------------------------------------------------
    def ig(slides, dil="tr+en", ekstra=""):
        bloklar = []
        for n, (tr, en) in slides.items():
            baslik = "# Kapak (slayt 1)" if n == 1 else f"# Slayt {n} - Konu"
            bloklar.append(f"{baslik}\n\nTR: {tr}\nEN: {en}")
        return ("---\nproje: test\ntip: B\nhafta: 2026-W50\nkanal: ig\ndil: " + dil +
                "\nkaynak: private link yok\ngizlilik: kontrol edildi\n---\n\n" +
                "\n\n".join(bloklar) +
                "\n\n# Caption\n\nAtölyede sipariş takibi tek ekranda.\n\n"
                "# Hashtag (8-10)\n\n#a #b #c\n" + ekstra)

    temel_slayt = {1: ("Sipariş defterde, üretim panoda.", "Order in a notebook."),
                   2: ("Üç ayrı cevap var.", "Three answers."),
                   3: ("Cevap kişiye göre değişiyor.", "Depends who you ask."),
                   4: ("Tek kural: teslim ve bakiye.", "One rule: delivered and paid."),
                   5: ("Aşamaları atölye tanımlar.", "The workshop defines stages."),
                   6: ("Demo için DM.", "DM for a demo.")}

    saglam_ig = audit_post(ig(temel_slayt), "instagram", "saglam-ig.md")
    check("Carousel: sağlam post hata üretmez (6 slayt, TR+EN)",
          saglam_ig["hata"] == 0, f"hata: {saglam_ig['hata']} | kodlar: {[f['kod'] for f in saglam_ig['bulgular'] if f['seviye'] == 'hata']}")

    eksik_slayt = dict(temel_slayt)
    del eksik_slayt[4]
    k2 = audit_post(ig(eksik_slayt), "instagram", "eksik-slayt.md")
    check("Carousel: eksik slayt hata verir (K2)",
          any(f["kod"] == "P-SLAYT-EKSIK" for f in k2["bulgular"] if f["seviye"] == "hata"),
          f"kodlar: {[f['kod'] for f in k2['bulgular']]}")

    en_bos = dict(temel_slayt)
    en_bos[3] = ("Cevap kişiye göre değişiyor.", "")
    k2b = audit_post(ig(en_bos), "instagram", "en-bos.md")
    check("Carousel: eksik EN satırı hata verir (K2)",
          any(f["kod"] == "P-SLAYT-EN-YOK" for f in k2b["bulgular"]), f"kodlar: {[f['kod'] for f in k2b['bulgular']]}")

    uzun_kapak = dict(temel_slayt)
    uzun_kapak[1] = ("Sipariş defterde, üretim panoda, para cepte, kimse bilmiyor, her gün soruluyor.",
                    "Order in a notebook, production on a board.")
    k3 = audit_post(ig(uzun_kapak), "instagram", "uzun-kapak.md")
    check("Carousel: kapak uzunluğu uyarı verir (K3)",
          any(f["kod"] == "P-SLAYT-UZUN" for f in k3["bulgular"]), f"kodlar: {[f['kod'] for f in k3['bulgular']]}")

    tr_en = dict(temel_slayt)
    tr_en[2] = ("Üç ayrı cevap var.", "Atölye için demo")
    k4 = audit_post(ig(tr_en), "instagram", "en-tr.md")
    check("Carousel: EN satırda Türkçe harf uyarı verir (K4)",
          any(f["kod"] == "P-SLAYT-EN-TR" for f in k4["bulgular"]), f"kodlar: {[f['kod'] for f in k4['bulgular']]}")

    # --- Faz 2: proje iddiaları ve sızıntı ---------------------------------
    def li(govde, cta="Demo: local-ai-news.vercel.app", hashtag="#a #b #c", tip="A",
          kaynak="https://local-ai-news.vercel.app", note="- 12 tablo, 233 test",
          gizlilik="gerekmiyor"):
        return ("---\nproje: test\ntip: " + tip + "\nhafta: 2026-W50\nkanal: linkedin\n"
                "kaynak: " + kaynak + "\ngizlilik: " + gizlilik + "\n---\n\n"
                "# Gövde\n\n" + govde + "\n\n# CTA\n\n" + cta +
                "\n\n# Hashtag\n\n" + hashtag + "\n\n# Teknik doğruluk notu\n\n" + note + "\n")

    temel_li = li("Yerel model haberlerini kategorilere ayıran bir panel yazdım. Sunucu yok.")
    check("Proje iddiaları: temiz A tipi post hata üretmez",
          audit_post(temel_li, "linkedin", "temel-li.md")["hata"] == 0,
          f"kodlar: {[f['kod'] for f in audit_post(temel_li, 'linkedin', 'temel-li.md')['bulgular']]}")

    k5 = audit_post(li("Panel tarayıcıda çalışıyor, kayıt gerekmiyor.",
                       kaynak="https://github.com/bahattinercan/local-ai-news"),
                    "linkedin", "link-yok.md")
    check("Proje iddiaları: A tipi postta kaynak linki yoksa hata (K5)",
          any(f["kod"] == "P-LINK-YOK" and f["seviye"] == "hata" for f in k5["bulgular"]),
          f"kodlar: {[f['kod'] for f in k5['bulgular']]}")

    fork_link = audit_post(li("Tek dosyalık bir araç, kullanımı basit.", tip="A (fork + uyarlama)",
                              kaynak="https://github.com/bahattinercan/GoodbyeDPI-Turkey"),
                           "linkedin", "fork-link.md")
    check("Proje iddiaları: fork postunda da repo linki aranır (K5)",
          any(f["kod"] == "P-LINK-YOK" for f in fork_link["bulgular"]),
          f"kodlar: {[f['kod'] for f in fork_link['bulgular']]}")

    fork_post = li("GoodbyeDPI'i ben yazdım, tek dosyalık bir araç.", tip="A (fork + uyarlama)",
                   kaynak="https://github.com/bahattinercan/GoodbyeDPI-Turkey", note="- 12 tablo")
    k6 = audit_post(fork_post, "linkedin", "fork.md")
    check("Proje iddiaları: fork postunda beyan yoksa uyarı (K6)",
          any(f["kural"] == "K6" for f in k6["bulgular"]), f"kodlar: {[f['kod'] for f in k6['bulgular']]}")

    k8 = audit_post(li("Arayüz hazır. Repoyu klonla: git clone sonra çalıştır.", tip="B",
                       kaynak="private link yok"), "linkedin", "private-kurulum.md")
    check("Proje iddiaları: private postta kurulum komutu hata (K8)",
          any(f["kod"] == "P-KURULUM-SIZINTI" for f in k8["bulgular"] if f["seviye"] == "hata"),
          f"kodlar: {[f['kod'] for f in k8['bulgular']]}")

    k9 = audit_post(li("Ayarlarda token duruyor: ghp_abcdefghijklmnopqrstuvwx"),
                    "linkedin", "sir.md")
    check("Proje iddiaları: token sızıntısı hata (K9)",
          any(f["kod"] == "P-SIR" for f in k9["bulgular"] if f["seviye"] == "hata"),
          f"kodlar: {[f['kod'] for f in k9['bulgular']]}")

    k7 = audit_post(li("Panel Flutter ile yazıldı, sunucu yok.", note="- 12 tablo"),
                    "linkedin", "iddia.md")
    check("Proje iddiaları: notta olmayan teknoloji iddiası uyarı (K7)",
          any(f["kod"] == "P-IDDIA-IZI" for f in k7["bulgular"]), f"kodlar: {[f['kod'] for f in k7['bulgular']]}")

    # --- Faz 3: yazım ve tutarlılık ---------------------------------------
    def var_kod(post, kod):
        return any(f["kod"] == kod for f in audit_post(post, "linkedin", "x.md")["bulgular"])

    check("Yazım: teknoloji adı yazımı uyarı verir (K10)",
          var_kod(li("Kodu Github üzerinde tutuyorum."), "P-TEKNOLOJI-ADI"),
          "Github -> GitHub")
    check("Yazım: 4+ ardışık madde özellik yığını uyarısı (K11)",
          var_kod(li("- kasa\n- stok\n- veresiye\n- rapor"), "P-MADDE-YIGINI"),
          "4 madde")
    check("Yazım: iç jargon uyarısı (K12)",
          var_kod(li("Faz 3 tamam, sırada paketleme var.", note="- Faz 3 tamam"), "P-JARGON"),
          "Faz 3")
    check("Yazım: bozuk kodlama hata verir (K13)",
          any(f["kod"] == "P-KODLAMA" for f in audit_post(li("TÃ¼rkÃ§e metin"), "linkedin", "x.md")["bulgular"]),
          "mojibake")
    check("Yazım: sürüm iddiası notta yoksa uyarı (K14)",
          var_kod(li("v2.1 yayında, herkes kullanabilir."), "P-SURUM"), "v2.1")

    # --- Faz 0: kural ezme ------------------------------------------------
    ezilen = audit_post(li("Faz 3 tamam.", note="- Faz 3 tamam"), "linkedin", "ezme.md",
                        overrides={"K12": "bilgi"})
    check("Kural ezme: K12 bilgi seviyesine iner, kapı kapanmaz",
          not any(f["kod"] == "P-JARGON" and f["seviye"] == "uyarı" for f in ezilen["bulgular"]),
          f"K12 seviyeleri: {[f['seviye'] for f in ezilen['bulgular'] if f['kural'] == 'K12']}")

    # --- Faz 4/5: takvim ve canlı link ------------------------------------
    from denetle_post import audit_calendar, balance_findings, check_links, HATASI
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        ortak = li("Aynı açılış cümlesiyle başlayan bir post.")
        Path(tmp, "a-linkedin.md").write_text(ortak, encoding="utf-8")
        Path(tmp, "b-linkedin.md").write_text(ortak.replace("proje: test", "proje: test2"), encoding="utf-8")
        postlar, extra = audit_calendar([Path(tmp, "a-linkedin.md"), Path(tmp, "b-linkedin.md")],
                                        lambda p, fm: "linkedin", {})
        check("Takvim: aynı açılış iki postta uyarı (K15)",
              any(e["kod"] == "P-TAKVIM-ACILIS" for e in extra), f"bulgu: {len(extra)}")
        check("Takvim: içerik sütunu dengesi raporlanır (K16)",
              any(f["kural"] == "K16" for f in balance_findings(postlar)),
              balance_findings(postlar)[0]["mesaj"][:60])

    kapali_link = check_links(["http://127.0.0.1:9/"])
    check("Canlı link: ulaşılamayan adres sessizce geçilmez (K17)",
          bool(kapali_link) and kapali_link[0][0] == HATASI, f"{kapali_link}")

    return results


def main():
    parser = argparse.ArgumentParser(description="turkish-anti-ai-skill doğrulama ve regresyon testleri")
    parser.add_argument("--report", default=str(ROOT / "docs" / "TEST_VE_DOGRULAMA_RAPORU.txt"),
                        help="Rapor dosyası yolu (varsayılan: docs/TEST_VE_DOGRULAMA_RAPORU.txt)")
    parser.add_argument("--no-report", action="store_true", help="Rapor dosyasını yazma")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    lines = []

    def emit(line=""):
        print(line)
        lines.append(line)

    emit("=" * 78)
    emit("TURKISH-ANTI-AI-SKILL KAPSAMLI TEST VE DOĞRULAMA PAKETİ")
    emit("=" * 78)

    all_passed = True

    def emit_section(title, items, detail_fn):
        nonlocal all_passed
        emit(f"\n{title}")
        for item in items:
            status = "[GEÇTİ]" if item["passed"] else "[KALDI]"
            if not item["passed"]:
                all_passed = False
            emit(f"  {status} | {item['check']}")
            for detail in detail_fn(item):
                emit(f"           -> {detail}")

    pkg_results = test_package_integrity()
    emit_section("[BÖLÜM 1] PAKET VE MİMARİ BÜTÜNLÜK TESTLERİ", pkg_results, lambda item: [item["detail"]])

    detector_results = test_detector_rules()
    emit_section("[BÖLÜM 2] DEDEKTÖR KURAL TESTLERİ (yanlış pozitif ve register davranışı)",
                 detector_results, lambda item: [item["detail"]])

    post_results = test_post_gate()
    emit_section("[BÖLÜM 3] POST KAPISI TESTLERİ (sosyal medya yayın denetimi)",
                 post_results, lambda item: [item["detail"]])

    eval_results = test_eval_scenarios()
    emit("\n[BÖLÜM 4] 5 REGISTER + YANLIŞ POZİTİF & OLGUSAL SADAKAT TESTLERİ")
    for res in eval_results:
        status = "[GEÇTİ]" if res["passed"] else "[KALDI]"
        if not res["passed"]:
            all_passed = False
        lo, hi = res["target_range"]
        emit(f"  {status} | [{res['id']}] {res['title']}")
        emit(f"           -> Kalıp Sinyali (Önce -> Sonra): {res['before_flags']} -> {res['after_flags']}")
        emit(f"           -> '-mAktAdIr' Yoğunluğu (Önce -> Sonra): {res['before_mektedir']} -> {res['after_mektedir']} / 100 kelime (register hedefi: {lo}-{hi})")
        emit(f"           -> Art Arda Aynı Cümle Sonu (Önce -> Sonra): {res['before_run']} -> {res['after_run']} (sınır: 3 altı)")
        emit(f"           -> Cümle Ritmi / Burstiness CoV (Önce -> Sonra): {res['before_cov']} -> {res['after_cov']}")
        emit(f"           -> Olgusal Sadakat (token korunumu): {'%100 Korundu' if res['fidelity_preserved'] else res['missing_tokens']}")
        emit(f"           -> Olgusal Sadakat (ekleme yok): {'Uygun' if not res['fabrication_problems'] else res['fabrication_problems']}")
        if res["caught_examples"]:
            emit(f"           -> Yakalanan Örnek Sinyaller: {', '.join(repr(x) for x in res['caught_examples'])}")

    total_checks = len(pkg_results) + len(detector_results) + len(post_results) + len(eval_results)
    passed_checks = sum(1 for group in (pkg_results, detector_results, post_results, eval_results) for x in group if x["passed"])
    emit("\n" + "=" * 78)
    emit(f"GENEL SONUÇ: {passed_checks}/{total_checks} TEST BAŞARIYLA GEÇTİ ({'SORUNSUZ' if all_passed else 'HATALI'})")
    emit("=" * 78)

    # Rapor her koşuda yeniden yazılır: elle alınan anlık görüntü bayatlıyordu.
    if not args.no_report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Rapor yazıldı: {report_path}")

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
