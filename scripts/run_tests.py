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
from detect_tr_ai import COV_TARGET, analyze_text  # noqa: E402

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
    ]
    missing_refs = [r for r in expected_refs if not (ROOT / "references" / r).exists() or r not in skill_text]
    results.append({
        "check": "Progressive Disclosure Referans Dosyaları (references/*.md) Bütünlüğü",
        "passed": len(missing_refs) == 0,
        "detail": f"4/4 referans dosyası mevcut ve SKILL.md içinden bağlı" if not missing_refs else f"Eksik: {missing_refs}",
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
    """Dedektörün kural davranışī: düzeltilen yanlış pozitifler geri dönerse burada kırmızı olur."""
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

    skill_body = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    target_s, mech_s = f"{COV_TARGET:.2f}", f"{COV_MECHANICAL:.2f}"
    evals_cov = [c.get("min_after_cov") for c in json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))["test_cases"]
                 if c.get("mode") != "control" and "min_after_cov" in c]
    check("Dedektör: CoV eşikleri tek kaynaktan ve SKILL.md ile aynı",
          COV_MECHANICAL < COV_TARGET and target_s in skill_body and mech_s in skill_body and not evals_cov,
          f"mekanik: {mech_s} < hedef: {target_s} | SKILL.md'de ikisi de var: {target_s in skill_body and mech_s in skill_body}"
          f" | evals'te elle yazılmış eşik: {len(evals_cov)}")
    short = analyze_text("Kısa bir metin. İki cümle.")
    check("Dedektör: 3 cümleden kısa metinde CoV uydurulmaz",
          short["sentence_length_cov"] is None and not short["low_burstiness_warning"] and not short["cov_below_target"],
          f"CoV: {short['sentence_length_cov']}")

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
            # Eşik verilmemişse dedektördeki tek kaynak (COV_TARGET) kullanılır.
            min_cov = case.get("min_after_cov", COV_TARGET)
            after_cov = after_stats["sentence_length_cov"]
            cov_ok = after_cov is not None and after_cov >= min_cov
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


def main():
    parser = argparse.ArgumentParser(description="turkish-anti-ai-skill doğrulama ve regresyon testleri")
    parser.add_argument("--report", default=str(ROOT / "docs" / "TEST_VE_DOGRULAMA_RAPORU.txt"),
                        help="Rapor dosyası yolu (varsayılan: docs/TEST_VE_DOGRULAMA_RAPORU.txt)")
    parser.add_argument("--no-report", action="store_true", help="Rapor dosyasını yazma")
    args = parser.parse_args()

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
    emit_section("[BÖLÜM 2] DEDEKTÖR KURAL TESTLERİ (yanlış pozitif ve register davranışī)",
                 detector_results, lambda item: [item["detail"]])

    eval_results = test_eval_scenarios()
    emit("\n[BÖLÜM 3] 5 REGISTER + YANLIŞ POZİTİF & OLGUSAL SADAKAT TESTLERİ")
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

    total_checks = len(pkg_results) + len(detector_results) + len(eval_results)
    passed_checks = sum(1 for group in (pkg_results, detector_results, eval_results) for x in group if x["passed"])
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
