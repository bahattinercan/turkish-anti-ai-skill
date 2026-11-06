#!/usr/bin/env python3
"""
run_tests.py - turkish-anti-ai-skill Kapsamlı Doğrulama ve Regresyon Test Koşucusu
Çalıştırma: python3 scripts/run_tests.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from detect_tr_ai import analyze_text  # noqa: E402


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
    drift_ok = dist_file.exists() and pkg_skill.exists() and pkg_skill.read_text(encoding="utf-8") == skill_text
    results.append({
        "check": "Single-Source-of-Truth Senkronizasyonu (dist/ ve skills/ Zero-Drift)",
        "passed": drift_ok,
        "detail": f"dist boyutu: {dist_file.stat().st_size if dist_file.exists() else 0} byte | skills/ senkron: {drift_ok}",
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
            passed = (flags_caught and after_clean and mektedir_ok and cov_ok and fidelity_ok
                      and register_dose_ok and no_repeated_endings)

        missing_tokens = [tok for tok in case["must_preserve_tokens"] if tok not in case["output_human"]]
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
            "passed": passed,
            "caught_examples": [f["match"] for f in before_stats["findings"][:6]],
        })

    return scenario_results


def main():
    print("=" * 78)
    print("TURKISH-ANTI-AI-SKILL KAPSAMLI TEST VE DOĞRULAMA PAKETİ")
    print("=" * 78)

    pkg_results = test_package_integrity()
    print("\n[BÖLÜM 1] PAKET VE MİMARİ BÜTÜNLÜK TESTLERİ")
    all_passed = True
    for item in pkg_results:
        status = "[GEÇTİ]" if item["passed"] else "[KALDI]"
        if not item["passed"]:
            all_passed = False
        print(f"  {status} | {item['check']}\n           -> {item['detail']}")

    eval_results = test_eval_scenarios()
    print("\n[BÖLÜM 2] 5 REGISTER + YANLIŞ POZİTİF & OLGUSAL SADAKAT TESTLERİ")
    for res in eval_results:
        status = "[GEÇTİ]" if res["passed"] else "[KALDI]"
        if not res["passed"]:
            all_passed = False
        print(f"  {status} | [{res['id']}] {res['title']}")
        print(f"           -> AI Bayrakları (Önce -> Sonra): {res['before_flags']} -> {res['after_flags']}")
        lo, hi = res["target_range"]
        print(f"           -> '-mAktAdIr' Yoğunluğu (Önce -> Sonra): {res['before_mektedir']} -> {res['after_mektedir']} / 100 kelime (register hedefi: {lo}-{hi})")
        print(f"           -> Art Arda Aynı Cümle Sonu (Önce -> Sonra): {res['before_run']} -> {res['after_run']} (sınır: 3 altı)")
        print(f"           -> Cümle Ritmi / Burstiness CoV (Önce -> Sonra): {res['before_cov']} -> {res['after_cov']}")
        print(f"           -> Olgusal Sadakat (Sayı/Terim Korunumu): {'%100 Korundu' if res['fidelity_preserved'] else res['missing_tokens']}")
        if res["caught_examples"]:
            print(f"           -> Yakalanan Örnek Sinyaller: {', '.join(repr(x) for x in res['caught_examples'])}")

    total_checks = len(pkg_results) + len(eval_results)
    passed_checks = sum(1 for x in pkg_results if x["passed"]) + sum(1 for x in eval_results if x["passed"])
    print("\n" + "=" * 78)
    print(f"GENEL SONUÇ: {passed_checks}/{total_checks} TEST BAŞARIYLA GEÇTİ ({'SORUNSUZ' if all_passed else 'HATALI'})")
    print("=" * 78)

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
