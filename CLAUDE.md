# CLAUDE.md — Claude Code Geliştirici ve Kullanım Rehberi

Bu repo, Türkçe metinlerdeki yapay zeka izlerini (*AI slop & Translationese*) temizleyen `turkish-anti-ai-skill` yeteneğini içerir.

- Ana yetenek tanımı: `SKILL.md`
- Dilbilimi, sentaks, sözlük ve TDK referansları: `references/`
- Deterministik denetim aracı: `python3 scripts/detect_tr_ai.py <dosya_yolu>`
- Dağıtım (`dist/` ve `skills/`) derleyicisi: `python3 scripts/build_dist.py`

Kullanıcı Türkçe bir metin yazmanı, düzenlemeni veya "insanlaştırmanı" istediğinde `SKILL.md` içindeki 4 adımlı iş akışını ve **Olgusal Sadakat Kilidini** uygula.
