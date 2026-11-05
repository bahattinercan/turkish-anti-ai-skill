#!/usr/bin/env python3
"""
build_dist.py - SKILL.md ve references/*.md dosyalarını tek parça dist/turkish-anti-ai-skill.full.md
dosyasında birleştirir ve skills/turkish-anti-ai-skill/ alt dizini ile senkronize eder.
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF_ORDER = [
    "sentaks-ve-morfoloji.md",
    "ai-turkcesi-sozlugu.md",
    "tdk-ve-noktalama.md",
    "register-ve-ornekler.md",
]


def main():
    dist_dir = ROOT / "dist"
    dist_dir.mkdir(exist_ok=True)

    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    sections = [skill_md.strip()]

    for ref_name in REF_ORDER:
        ref_path = ROOT / "references" / ref_name
        if ref_path.exists():
            sections.append(f"\n\n<!-- KAYNAK: references/{ref_name} -->\n\n" + ref_path.read_text(encoding="utf-8").strip())

    full_path = dist_dir / "turkish-anti-ai-skill.full.md"
    full_path.write_text("\n".join(sections) + "\n", encoding="utf-8")

    # npx skills CLI uyumluluğu için skills/turkish-anti-ai-skill/ dizinini senkronize et
    pkg_dir = ROOT / "skills" / "turkish-anti-ai-skill"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "SKILL.md", pkg_dir / "SKILL.md")
    if (pkg_dir / "references").exists():
        shutil.rmtree(pkg_dir / "references")
    shutil.copytree(ROOT / "references", pkg_dir / "references")

    print(f"Derleme tamamlandı: {full_path} ({full_path.stat().st_size} byte)")
    print(f"Paket dizini senkronize edildi: {pkg_dir}")


if __name__ == "__main__":
    main()
