# turkish-anti-ai-skill

**Türkçeyi çevrilmiş İngilizce gibi değil, insan eliyle yazılmış doğal Türkçe gibi yaz ve onar.**  
*An open-source Agent Skill & Turkish Humanizer that removes AI writing patterns ("Yapay Zeka Türkçesi" / Translationese) and rebuilds authentic Turkish sentence architecture.*

[![Agent Skills Specification](https://img.shields.io/badge/Agent_Skills-v1.0-blue)](https://agentskills.io/specification)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![TDK Uyumlu](https://img.shields.io/badge/TDK-Yaz%C4%B1m_K%C4%B1lavuzu-red)](https://sozluk.gov.tr/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Kurulum** · **Öncesi / Sonrası Demo** · **Neden Sadece Bir Prompt Değil?** · **3 Katmanlı Mimari** · **Register Matrisi** · **CLI Dedektörü**

## Sorun Nedir?

Büyük Dil Modelleri (LLM) ağırlıklı olarak İngilizce veriyle eğitildiği ve RLHF aşamasında İngilizce retorik kalıplarıyla ödüllendirildiği için, Türkçe metin üretirken **"kelimeleri Türkçe ama cümle iskeleti İngilizce"** olan mekanik bir dil (*Translationese / Yapay Zeka Türkçesi*) üretir.

Piyasadaki İngilizce *humanizer* araçları yalnızca yüzeydeki kelimeleri değiştirir. Oysa Türkçede sorun sadece *"yadsınamaz"*, *"adeta"* veya *"kritik bir rol oynamaktadır"* kelimeleri değildir. Asıl sorun **niteleyicilerin baş ismin arkasına takılması (sağa dallanma), ulaç (`-Ip, -IncA, -dIkçA`) gereken yere mekanik `ve` bağlacının girmesi, her cümlenin `-DIr / -mAktAdIr` ile bitmesi ve tüm cümlelerin 18-22 kelimelik tekdüze bir banda sıkışmasıdır.**

`turkish-anti-ai-skill`, kelimelerin altındaki **Türkçe cümle mimarisini**, **TDK Yazım Kılavuzu kurallarını** ve **insan nefes ritmini (burstiness)** yeniden kurar.

## Hızlı Demo (Öncesi / Sonrası)

### Girdi (Tipik Yapay Zeka Türkçesi)
> Günümüzün hızla değişen iş dünyasında, uzaktan çalışma modeli sadece geçici bir trend değil, aynı zamanda kurumsal kültürün temel bir yapı taşı haline gelmiştir — ve bu durumun önemi yadsınamaz. Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki, çalışanlara esneklik sağlamak verimlilik üzerinde kritik bir rol oynamaktadır. Bununla birlikte, iletişim kopukluklarını önlemek adına bütüncül bir yaklaşım benimsenmelidir. Sonuç olarak, geleceğin çalışma dünyasında başarılı olmak isteyen kurumlar bu dönüşüme ayak uydurmak zorundadır.

### Çıktı (`turkish-anti-ai-skill` Onarım Modu · *Blog/Deneme Register*)
> Uzaktan çalışma artık şirket kültürünün kalıcı bir parçası. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik artıyor. İşin zor kısmı, ekip aynı ofisi paylaşmazken iletişimi koparmamak. Kalıcı çözüm ise çalışma düzenini baştan sona bu yeni ritme göre kurgulamaktan geçiyor.

**Neleri Yakaladı ve Onardı?**
1. **Sahneleme Girişi (P0):** *"Günümüzün hızla değişen iş dünyasında"* boş girişi silindi, doğrudan konuya girildi.
2. **Negatif Paralellik (P0):** *"sadece X değil, aynı zamanda Y"* kalıbı tamamen silindi, yerine tek bir olumlu yargı geldi (*"şirket kültürünün kalıcı bir parçası"*).
3. **Noktalama & Tier-1 Klişe (P0/P2):** TDK'da diyalog dışında bulunmayan uzun çizgi (`—`) ve *"önemi yadsınamaz"* klişesi kaldırıldı.
4. **Edilgen Çatı & Hint-Avrupa `ki` Bağlacı (P1):** *"Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki"* yapısı etken ve doğrudan cümleye çevrildi.
5. **Kof Yardımcı Fiil & `-mAktAdIr` Salgını (P1):** *"esneklik sağlamak ... kritik bir rol oynamaktadır"* yerine *"esneklik tanıdığınızda verimlilik artıyor"* kuruldu.
6. **Vaaz Veren Kapanış (P0):** *"Sonuç olarak ... ayak uydurmak zorundadır"* ders verme cümlesi tamamen kesildi.
7. **Olgusal Sadakat Kilidi:** Kaynak metinde olmayan hiçbir istatistik, tarih veya uydurma kişisel anekdot eklenmedi.

## Neden Sadece Bir Prompt Değil de Bir Skill?

Tek satırlık *"Bunu insani ve doğal bir Türkçeyle yaz"* komutu yalnızca en bariz birkaç kelimeyi değiştirir ve çoğu zaman modelin "insan gibi görünmek" adına **kaynakta olmayan veriler/anekdotlar uydurmasına** yol açar. `turkish-anti-ai-skill` ise modele kurallı bir çalışma düzeni verir. Yeniden yazımı model `SKILL.md` ve referans dosyalarındaki kurallara göre yapar. Deterministik olan tek parça ise bu çıktıyı denetleyen CLI dedektörüdür:

- **3 Çalışma Modu (`rewrite`, `write`, `audit`):** Mevcut metni olgusal sadakatle onarır (`rewrite`), sıfırdan Türkçe düşünerek metin kurar (`write`) veya metne dokunmadan AI/TDK kusurlarını raporlar (`audit`).
- **Olgusal Sadakat Kilidi (Anti-Fabrication Lock):** Onarım modunda kaynakta bulunmayan hiçbir sayı, tarih, isim, iddia veya nedensellik bağı eklenemez.
- **5 Register × 9 Üslup Boyutu Kalibrasyonu:** KVKK metnine devrik cümle sokmaz, blog yazısına `-mAktAdIr` eki dayatmaz (*Blog/Deneme, Teknik/Mühendislik, Kurumsal/SaaS, Akademik/Resmi, Edebi/Anlatı*).
- **60+ Kalıplık 3 Katmanlı "Yapay Zeka Türkçesi" Sözlüğü:** Tier-1 (kesin ifşalar), Tier-2 (bürokratik bağlaçlar) ve Tier-3 (SaaS/pazarlama çeviri kokuları) tabloları.
- **TDK Yazım Kılavuzu ve Fonetik Ek Denetimi:** Yabancı teknik terimleri (`endpoint`, `deploy`, `middleware`, `queue`) *"uç nokta, ara katman"* diye zorla çevirmez. Ekleri kelimenin yazılışına göre değil **Türkçe okunuşuna (fonetiğine)** göre getirir (`cache'i`, `queue'yu`, `SQL'i`, `JSON'ı`).
- **Deterministik Python CLI Dedektörü (`scripts/detect_tr_ai.py`):** Harici kütüphane gerektirmeden Türkçe metinlerdeki AI klişelerini, TDK hatalarını, `-mAktAdIr` yoğunluğunu ve cümle uzunluğu varyasyonunu (**Burstiness CoV**) ölçer. Regex ve basit istatistikle çalışır, yalnızca yüzeydeki izleri yakalar. Sola dallanma, ulaç kullanımı veya register uyumu gibi cümle mimarisi kararlarını ölçmez, bunlar modelin işidir.

## Kurulum (Installation)

### 1. Evrensel Agent Skills CLI (`npx skills` & `gh skill`)
Claude Code, Cursor, OpenAI Codex, Gemini CLI, Windsurf ve OpenCode için tek komutla kurulum:

```bash
npx skills add yucezerey/turkish-anti-ai-skill
```

GitHub CLI (v2.90+) kullanıyorsan:

```bash
gh skill install yucezerey/turkish-anti-ai-skill
```

### 2. Claude Code & Claude Cowork
**Seçenek A: Plugin Marketplace olarak kurulum (Önerilen):**
```text
/plugin marketplace add yucezerey/turkish-anti-ai-skill
/plugin install turkish-anti-ai-skill@yucezerey
```

**Seçenek B: Doğrudan `~/.claude/skills/` dizinine klonlama:**
```bash
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.claude/skills/turkish-anti-ai-skill
```

### 3. Cursor (`.cursor/rules/*.mdc` veya Agent Skills)
Projenin kök dizininde Cursor kuralını aktif etmek için:

```bash
mkdir -p .cursor/rules
curl -sL https://raw.githubusercontent.com/yucezerey/turkish-anti-ai-skill/main/.cursor/rules/turkish-anti-ai-skill.mdc \
  -o .cursor/rules/turkish-anti-ai-skill.mdc
```

### 4. OpenAI Codex, Gemini CLI ve Windsurf
```bash
# Evrensel .agents/skills/ dizini (Codex, Gemini CLI, Cursor, Windsurf destekler)
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.agents/skills/turkish-anti-ai-skill

# Veya doğrudan Gemini CLI dizinine:
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.gemini/skills/turkish-anti-ai-skill
```

### 5. ChatGPT (Custom GPT), Claude Projects ve Google AI Studio (Web)
Klasör yüklenemeyen web arayüzleri için tüm referans tablolarının tek dosyada birleştirildiği `dist/turkish-anti-ai-skill.full.md` dosyasını kopyalayıp **Project Instructions / System Prompt** veya **Knowledge** alanına yapıştırabilirsin.

## Kullanım

Kurulumdan sonra ajanına doğal dilde seslenmen yeterlidir. Yetenek kendi açıklamasıyla (`description`) otomatik tetiklenir:

- **Onarım (`rewrite`):** *"Şu blog yazısını insanlaştır ve AI kokusunu sil: `<metin>`"*
- **Üretim (`write`):** *"Dağıtık sistemlerde cache invalidation konusunu teknik register'da, doğal Türkçeyle yaz."*
- **Denetim (`audit`):** *"Bu kurumsal metni değiştirme, sadece içindeki AI-Türkçesi ve TDK hatalarını raporla (audit modu)."*

## Üç Katmanlı Mimari Özeti

| Katman | Odak Noktası | Yakalanan Yapay Zeka İzi (Makine Türkçesi) | Uygulanan Doğal Türkçe Dönüşümü |
| :--- | :--- | :--- | :--- |
| **Katman 1: Kompozisyon (P0)** | Giriş, kapanış, retorik şablonlar | *"Günümüzün hızla değişen..."*, *"Sadece X değil, aynı zamanda Y"*, *"Sonuç olarak..."*, üçlü sıfat listeleri | Sahne veya doğrudan tez ile açılış, negatif paralelliklerin kaldırılması, vaaz veren kapanışların kesilmesi |
| **Katman 2: Cümle Mimarisi (P1)** | Sentaks ve morfoloji (`references/sentaks-ve-morfoloji.md`) | Sağa dallanan yan cümleler, Hint-Avrupa `ki` bağlacı, refleks `ve`, `-DIr / -mAktAdIr` şişmesi, gereksiz `"bir"` ve `"tarafından"` | Sıfat-fiille sola dallanma, ulaç sistemi (`-Ip, -IncA, -dIkçA`), yüklem önü vurgu yuvası, zamir düşürme (pro-drop), delil kipi (`-mIş`) |
| **Katman 3: TDK ve Yüzey (P2)** | Noktalama, imla ve terimler (`references/tdk-ve-noktalama.md`) | Uzun çizgi (`—`), orta çizgi (`–`), `..., ama` virgülü, `"uç nokta"` gibi zorlama çeviriler, `"cache'ı, SQL'ı"` ek hataları | 5 mutlak noktalama yasağı, TDK birleşik/ayrı kelime kuralları, terimlerin Türkçe okunuşa göre çekimlenmesi (`cache'i, SQL'i`) |

## Deterministik CLI Dedektörü (`detect_tr_ai.py`)

Repodaki Python betiği ile herhangi bir Markdown veya metin dosyasını terminalden ya da CI/CD (GitHub Actions) üzerinden tarayabilirsin:

```bash
python3 scripts/detect_tr_ai.py ornek-metin.md
# JSON çıktısı için:
python3 scripts/detect_tr_ai.py ornek-metin.md --json
# Register'a göre '-mAktAdIr' hedefiyle denetim için:
python3 scripts/detect_tr_ai.py makale.md --register akademik-resmi
```

`--register` değerleri: `blog-deneme`, `teknik`, `kurumsal`, `akademik-resmi`, `edebi-anlati`. Register verildiğinde dedektör `-mAktAdIr` yoğunluğunu o metin türünün hedef aralığıyla karşılaştırır. Akademik register'da ek korunur, hedef 100 kelimede yaklaşık 0,5-2,5'tir. Blog ve edebi metinde hedef sıfıra yakındır. Ayrıca art arda üç veya daha fazla cümlenin aynı ekle (`-mektedir`, `-mıştır`, `-dır`) bitip bitmediğini ölçer. Bu aralıklar korpusla kalibre edilmiş değerler değil, `scripts/detect_tr_ai.py` içinden değiştirilebilen başlangıç değerleridir.

Tek parça `dist/turkish-anti-ai-skill.full.md` dosyasını yeniden derlemek için:

```bash
python3 scripts/build_dist.py
```

## Güvenlik

Skill, modele verilen Markdown talimatlarından ve üç yerel Python betiğinden oluşur. Betikler ağa çıkmaz, komut çalıştırmaz, harici kütüphane kullanmaz.

| Betik | Ne yapar | Dosya yazar mı |
| :--- | :--- | :--- |
| `scripts/detect_tr_ai.py` | Verilen metin dosyasını okur, raporu ekrana basar | Hayır |
| `scripts/run_tests.py` | Repo dosyalarını ve `evals/evals.json` senaryolarını dedektörden geçirir | Hayır |
| `scripts/build_dist.py` | `dist/` dosyasını üretir, `skills/turkish-anti-ai-skill/` klasörünü kaynakla eşler | Evet, yalnızca repo içinde |

`build_dist.py`, eşleme sırasında `skills/turkish-anti-ai-skill/references/` klasörünü silip yeniden kopyalar. Güvenlik tarayıcıları (Socket, Snyk) bu satırı dosya silme işlemi olarak işaretleyebilir. Silme bir kilitle korunur: hedef bu tek klasör değilse veya symlink ise betik durur, hiçbir şey silinmez.

`npx skills` veya `gh skill` ile kurulumda yalnızca `skills/turkish-anti-ai-skill/` klasörü iner. Bu klasörde betik yoktur, yalnızca `SKILL.md` ve `references/` vardır.

## Repo Klasör Yapısı

```text
turkish-anti-ai-skill/
├── SKILL.md                           # Ana orkestratör (<500 satır, YAML frontmatter + 4 adımlı iş akışı)
├── skills/turkish-anti-ai-skill/      # npx skills CLI ve plugin paketleyici uyumluluk dizini
├── AGENTS.md                          # Codex, Cursor, Windsurf, Copilot ortak adaptörü
├── CLAUDE.md                          # Claude Code proje rehberi
├── GEMINI.md                          # Gemini CLI adaptörü
├── references/                        # Aşamalı yüklenen (Progressive Disclosure) Türkçe dilbilimi veritabanı
│   ├── tdk-ve-noktalama.md            # 5 mutlak noktalama yasağı, TDK imla ve fonetik ek tablosu
│   ├── sentaks-ve-morfoloji.md        # Sola dallanma, ulaçlar, vurgu yuvası, -DIr/-mAktAdIr, pro-drop
│   ├── ai-turkcesi-sozlugu.md         # Tier-1, Tier-2 ve Tier-3 Yapay Zeka Türkçesi sözlüğü (60+ kalıp)
│   └── register-ve-ornekler.md        # 5 register x 9 boyut matrisi ve uçtan uca Before/After örnekleri
├── scripts/
│   ├── detect_tr_ai.py                # Deterministik Türkçe AI-slop, TDK ve Burstiness (CoV) tarayıcı CLI
│   └── build_dist.py                  # SKILL.md + references/* dosyalarını dist/ içine derler
├── .cursor/rules/
│   └── turkish-anti-ai-skill.mdc      # Cursor yerel kural adaptörü (.mdc)
├── .claude-plugin/
│   └── plugin.json                    # Claude Code / Cowork plugin manifestosu
├── dist/
│   └── turkish-anti-ai-skill.full.md  # Web arayüzleri (Custom GPT / Claude Projects) için tekil dosya
├── evals/
│   └── evals.json                     # Olgusal sadakat ve anti-slop regresyon test senaryoları
├── docs/
│   └── ARASTIRMA_VE_MIMARI_RAPORU.md  # Kapsamlı Türkçe dilbilimi ve anti-AI mimari araştırma raporu
├── CONTRIBUTING.md                    # Kanıta dayalı yeni kalıp ekleme kuralları
└── LICENSE                            # MIT Lisansı
```

## Katkıda Bulunma (Contributing)

Yeni bir "Yapay Zeka Türkçesi" kalıbı, çeviri kokan SaaS ifadesi veya TDK sınır durumu fark ettiysen Issue veya Pull Request açabilirsin. Kurallar ve şablon için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına göz at.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında açık kaynak olarak sunulmaktadır.
