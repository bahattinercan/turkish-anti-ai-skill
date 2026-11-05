# AGENTS.md — Çoklu Ajan (Codex, Cursor, Claude Code, Gemini CLI, Windsurf) Yönlendiricisi

Bu repo, Türkçe metinlerdeki yapay zeka izlerini (*AI slop / Translationese*) temizlemek ve TDK uyumlu, doğal insan Türkçesi üretmek için tasarlanmış `turkish-anti-ai-skill` paketini barındırır.

## Ajan Talimatları

1. Türkçe bir metni yazarken, düzenlerken, insanlaştırırken veya denetlerken **önce kök dizindeki `SKILL.md` dosyasını oku**.
2. Görevin bağlamına göre aşağıdaki referans dosyalarını (`references/`) incele:
   - `references/sentaks-ve-morfoloji.md`: Sola dallanma, ulaç sistemi (`-Ip, -IncA, -dIkçA`), yüklem önü vurgu yuvası, `-DIr / -mAktAdIr` temizliği, zamir düşürme ve kof fiiller.
   - `references/ai-turkcesi-sozlugu.md`: Tier-1 (`yadsınamaz, adeta, derinlemesine, kritik bir rol oynamaktadır`), Tier-2 (`bununla birlikte, söz konusu, bu bağlamda`) ve Tier-3 SaaS/pazarlama klişeleri.
   - `references/tdk-ve-noktalama.md`: 5 mutlak noktalama yasağı (uzun çizgi `—`, orta çizgi `–`, `ama` öncesi virgül), TDK birleşik/ayrı kelimeler ve teknik terimlerin Türkçe okunuşa göre ek alması (`cache'i, queue'yu, SQL'i, JSON'ı`).
   - `references/register-ve-ornekler.md`: 5 register profili (*Blog/Deneme, Teknik, Kurumsal, Akademik, Edebi*) ve Before/After dönüşüm örnekleri.
3. Deterministik metin taraması için `python3 scripts/detect_tr_ai.py <dosya>` komutunu çalıştırabilirsin.
4. `SKILL.md` veya `references/` altında bir değişiklik yaptığında `python3 scripts/build_dist.py` komutunu çalıştırarak `dist/turkish-anti-ai-skill.full.md` ve `skills/turkish-anti-ai-skill/` dosyalarını senkronize et.
