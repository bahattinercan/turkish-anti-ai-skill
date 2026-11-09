# GEMINI.md: Gemini CLI Adaptörü

Bu repo, Türkçe metinlerdeki yapay zekâ izlerini (*AI slop & Translationese*) temizleyen `turkish-anti-ai-skill` yeteneğini içerir.

- Ana yetenek tanımı: `SKILL.md`
- Dilbilimi, sentaks, sözlük ve TDK referansları: `references/`
- Deterministik denetim aracı: `python3 scripts/detect_tr_ai.py <dosya_yolu> --register <register>`
- Doğrulama kapısı: `python3 scripts/run_tests.py`
- Dağıtım (`dist/` ve `skills/`) derleyicisi: `python3 scripts/build_dist.py`

Gemini CLI, yeteneği `description` alanından tetikler. Türkçe bir metin yazmanı, düzenlemeni veya "insanlaştırmanı" istediğinde `SKILL.md` içindeki 4 adımlı iş akışını ve **Olgusal Sadakat Kilidini** uygula: kaynakta olmayan sayı, tarih, isim, anekdot veya kesinlik derecesi ekleme.
