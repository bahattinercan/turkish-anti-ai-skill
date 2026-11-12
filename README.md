# turkish-anti-ai-skill

**Türkçe metni, ilk okumada anlaşılan insan Türkçesine çevirir.**

Modellerin "kelimeleri Türkçe, cümle iskeleti İngilizce" çıktısını temizler. Yapay zekâ Türkçesi denen mekanik metni alır, cümle mimarisini, TDK yazımını ve nefes ritmini yeniden kurar.

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-v1.0-blue)](https://agentskills.io/specification)
[![Version](https://img.shields.io/badge/version-1.1.0-informational)](SKILL.md)
[![Tests](https://img.shields.io/badge/tests-51%2F51-success)](docs/TEST_VE_DOGRULAMA_RAPORU.txt)
[![TDK](https://img.shields.io/badge/TDK-Yaz%C4%B1m_K%C4%B1lavuzu-red)](https://sozluk.gov.tr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Türkçe** · [English](README.en.md)

|  |  |
| :--- | :--- |
| **Ne yapar** | Türkçe metni onarır, sıfırdan yazar, denetler, sosyal medya postu üretir |
| **Nasıl çalışır** | Bir talimat dosyası (`SKILL.md`), beş referans dosyası, üç yerel Python betiği |
| **Nereye kurulur** | Claude Code, Cursor, Codex, Gemini CLI, Windsurf, OpenCode, Custom GPT |
| **Bağımlılık** | Yok. Python 3 dışında bir şey kurmaz, ağa çıkmaz |

**İçindekiler:** [Sorun](#sorun) · [Öncesi ve Sonrası](#öncesi-ve-sonrası) · [Kurulum](#kurulum) · [Kullanım](#kullanım) · [Mimari](#mimari) · [Register](#register-kalibrasyonu) · [CLI Araçları](#komut-satırı-araçları) · [Güvenlik](#güvenlik) · [Depo Yapısı](#depo-yapısı) · [Katkı](#katkı)

## Sorun

Büyük dil modelleri ağırlıklı olarak İngilizce veriyle eğitiliyor ve İngilizce retorik kalıplarıyla ödüllendiriliyor. Türkçe yazarken de o iskeleti taşıyorlar. Cümle sağa dallanıyor, sıralı eylemler `ve` ile bağlanıyor, her yüklem `-DIr` ya da `-mAktAdIr` ile kapanıyor, bütün cümleler 18-22 kelimelik tek bir banda sıkışıyor.

İngilizce humanizer araçları yüzeydeki kelimeleri değiştirir: *"yadsınamaz"*, *"âdeta"*, *"kritik bir rol oynamaktadır"*. Oysa sorun sözlükte değil, cümlenin kuruluşunda. `turkish-anti-ai-skill` kelime listesiyle yetinmez; Türkçenin sondan eklemeli ve sola dallanan yapısını geri getirir, TDK Yazım Kılavuzu'na uyar, insan ritmini kurar.

## Öncesi ve Sonrası

**Girdi: tipik yapay zekâ Türkçesi**

> Günümüzün hızla değişen iş dünyasında, uzaktan çalışma modeli sadece geçici bir trend değil, aynı zamanda kurumsal kültürün temel bir yapı taşı haline gelmiştir — ve bu durumun önemi yadsınamaz. Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki, çalışanlara esneklik sağlamak verimlilik üzerinde kritik bir rol oynamaktadır. Bununla birlikte, iletişim kopukluklarını önlemek adına bütüncül bir yaklaşım benimsenmelidir. Sonuç olarak, geleceğin çalışma dünyasında başarılı olmak isteyen kurumlar bu dönüşüme ayak uydurmak zorundadır.

**Çıktı: onarım modu, blog/deneme register'ı**

> Uzaktan çalışma artık şirket kültürünün kalıcı bir parçası. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik artıyor. İşin zor kısmı, ekip aynı ofisi paylaşmazken iletişimi koparmamak. Kalıcı çözüm ise çalışma düzenini baştan sona bu yeni ritme göre kurmak.

<details>
<summary><b>Neler onarıldı? (7 kalem)</b></summary>

1. **Sahneleme girişi (P0):** *"Günümüzün hızla değişen iş dünyasında"* silindi, konuya doğrudan girildi.
2. **Negatif paralellik (P0):** *"sadece X değil, aynı zamanda Y"* kalıbı tek bir olumlu yargıya döndü.
3. **Uzun çizgi ve Tier-1 klişe (P0/P2):** TDK'da diyalog dışında yeri olmayan `—` ile *"önemi yadsınamaz"* kaldırıldı.
4. **Edilgen çatı ve `ki` bağlacı (P1):** *"Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki"* etken ve doğrudan cümleye çevrildi.
5. **Kof fiil ve `-mAktAdIr` (P1):** *"esneklik sağlamak... kritik bir rol oynamaktadır"* yerine *"esneklik tanıdığınızda verimlilik artıyor"* kuruldu.
6. **Vaaz veren kapanış (P0):** *"Sonuç olarak... ayak uydurmak zorundadır"* cümlesi kesildi.
7. **Olgusal sadakat:** Kaynakta olmayan hiçbir sayı, tarih veya anekdot eklenmedi.

</details>

Bu metinler `evals/evals.json` içindeki regresyon senaryolarından geliyor; her push'ta otomatik doğrulanıyor.

## Kurulum

| Ortam | Yol |
| :--- | :--- |
| Evrensel (`npx skills`, `gh skill`) | `~/.agents/skills/` altına tek komut |
| Claude Code, Cowork | Plugin marketplace ya da `~/.claude/skills/` |
| Cursor | `.cursor/rules/turkish-anti-ai-skill.mdc` |
| Codex, Gemini CLI, Windsurf, OpenCode | `~/.agents/skills/` ya da `~/.gemini/skills/` |
| Custom GPT, Claude Projects, AI Studio | `dist/turkish-anti-ai-skill.full.md` tek dosya |

### 1. Evrensel Agent Skills CLI

```bash
npx skills add yucezerey/turkish-anti-ai-skill
```

GitHub CLI kullanıyorsan (v2.90+):

```bash
gh skill install yucezerey/turkish-anti-ai-skill
```

### 2. Claude Code ve Claude Cowork

Plugin olarak (önerilen):

```text
/plugin marketplace add yucezerey/turkish-anti-ai-skill
/plugin install turkish-anti-ai-skill@yucezerey
```

Ya da doğrudan klonla:

```bash
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.claude/skills/turkish-anti-ai-skill
```

### 3. Cursor

```bash
mkdir -p .cursor/rules
curl -sL https://raw.githubusercontent.com/yucezerey/turkish-anti-ai-skill/main/.cursor/rules/turkish-anti-ai-skill.mdc \
  -o .cursor/rules/turkish-anti-ai-skill.mdc
```

### 4. Codex, Gemini CLI, Windsurf

```bash
# Ortak .agents/skills/ dizini
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.agents/skills/turkish-anti-ai-skill

# Yalnızca Gemini CLI için:
git clone https://github.com/yucezerey/turkish-anti-ai-skill.git ~/.gemini/skills/turkish-anti-ai-skill
```

### 5. Web arayüzleri (klasör yüklenemeyenler)

`dist/turkish-anti-ai-skill.full.md` bütün referans tablolarını tek dosyada birleştirir. İçeriği Custom GPT'nin **Instructions** alanına, Claude Projects'in **Project knowledge** alanına ya da AI Studio'nun system prompt'una yapıştır.

> `npx skills` ve `gh skill` yalnızca `skills/turkish-anti-ai-skill/` klasörünü indirir: `SKILL.md` ve `references/`. Betikler bu pakette yok.

## Kullanım

Kurulumdan sonra ayrı bir komut ezberlemek gerekmiyor. Skill, kendi `description` alanıyla tetiklenir:

| Mod | Ne zaman | Örnek istem |
| :--- | :--- | :--- |
| `rewrite` (varsayılan) | Elde bir metin var, onarılacak | *"Şu blog yazısını insanileştir ve AI hissiyatını sil: `<metin>`"* |
| `write` | Sıfırdan Türkçe yazılacak | *"Dağıtık sistemlerde cache invalidation konusunu teknik register'da yaz."* |
| `audit` | Metne dokunmadan rapor isteniyor | *"Bu kurumsal metni değiştirme, sadece AI Türkçesi ve TDK hatalarını raporla."* |
| `post` | LinkedIn, Instagram, X postu | *"Bu projeyi LinkedIn'de tanıtan bir post yaz; hook, hashtag ve CTA dahil."* |

Mod adını söylemek zorunda değilsin. İstemden çıkarılır. `audit` modunda metin değişmez, yalnızca P0/P1/P2 sinyalleri alıntılanır.

## Mimari

Her kural üç katmandan birine düşer. Katman, müdahalenin sertliğini belirler.

| Katman | Neye bakar | Yakaladığı iz | Yaptığı dönüşüm |
| :--- | :--- | :--- | :--- |
| **1. Kompozisyon (P0)** | Giriş, kapanış, retorik | *"Günümüzün hızla değişen..."*, *"X değil, Y"*, *"Sonuç olarak..."*, üçlü sıfat listeleri | Sahne ya da doğrudan tez ile açılış, negatif paralelliğin kaldırılması, ders veren kapanışın kesilmesi |
| **2. Cümle mimarisi (P1)** | Sentaks ve morfoloji | Sağa dallanan yan cümleler, Hint-Avrupa `ki`, refleks `ve`, `-DIr / -mAktAdIr` şişmesi, gereksiz `bir` ve `tarafından` | Sıfat-fiille sola dallanma, ulaç sistemi (`-Ip, -IncA, -dIkçA`), yüklem önü vurgu yuvası, zamir düşürme, kanıtsallık kipi (`-mIş`) |
| **3. TDK ve yüzey (P2)** | Noktalama, imla, terim | Uzun çizgi, orta çizgi, `ve/veya` çevresinde virgül, noktalı virgül köprüsü, zorlama çeviri (*"uç nokta"*), ek hatası (*"cache'ı", "SQL'ı"*) | `[TDK]` ve `[Üslup]` etiketlerinin ayrılması, birleşik/ayrı kelime kuralları, terimlerin Türkçe okunuşa göre çekimlenmesi (`cache'i, SQL'i`) |

Kuralların ayrıntısı `references/` altında; `SKILL.md` yalnızca iş akışını ve karar noktalarını taşır (136 satır). Model dosyaları ihtiyaç anında okur.

| Dosya | İçerik |
| :--- | :--- |
| [`references/sentaks-ve-morfoloji.md`](references/sentaks-ve-morfoloji.md) | Cümlenin geometrisi, sola dallanma, ulaçlar, vurgu yuvası, `-DIr`/`-mAktAdIr`, pro-drop, kof fiiller |
| [`references/ai-turkcesi-sozlugu.md`](references/ai-turkcesi-sozlugu.md) | 60+ kalıplık üç kademeli sözlük: Tier-1, Tier-2, Tier-3 ve sohbet artıkları |
| [`references/tdk-ve-noktalama.md`](references/tdk-ve-noktalama.md) | Beş mutlak noktalama yasağı, TDK birleşik/ayrı kelimeler, fonetik ek tablosu |
| [`references/register-ve-ornekler.md`](references/register-ve-ornekler.md) | 5 register × 9 boyut matrisi ve uçtan uca Before/After çiftleri |
| [`references/sosyal-medya.md`](references/sosyal-medya.md) | LinkedIn, Instagram, X register'ı: hook geometrisi, bütçeler, emoji, CTA, yayın kapısı |

## Register Kalibrasyonu

Doğal Türkçe tek bir tondan oluşmaz. Sözleşmedeki devrik cümle özensizlik, blog yazısındaki `-mAktAdIr` ise robotluk üretir. Skill işe başlamadan önce metni beş profilden birine oturtur.

| Register | `-mAktAdIr` (100 kelimede) | Devrik cümle | Kompozisyon müdahalesi |
| :--- | :--- | :--- | :--- |
| Blog / Deneme / Sosyal Medya | 0,0 - 0,5 | 400 kelimede 2-3 | Tam |
| Teknik / Mühendislik | 0,0 - 1,0 | Yok | Orta |
| Kurumsal / SaaS / İş İletişimi | 0,0 - 1,0 | Yok | Orta |
| Akademik / Resmî / Hukuki | 0,5 - 2,5 | Yasak | Kapalı (belge iskeleti korunur) |
| Edebî / Anlatı | 0,0 - 0,5 | Ritme göre | Tam |

Aralıklar korpus ölçümüyle kalibre edilmedi; `scripts/detect_tr_ai.py` içindeki başlangıç değerleridir. Kullanıcı kendi yazısından örnek verdiyse (few-shot), o örnek en üst kural sayılır.

## Komut Satırı Araçları

Üç betik var, hiçbiri harici kütüphane kullanmaz.

### `detect_tr_ai.py`: deterministik tarayıcı

Metnin yazarını tespit etmez. İnsan eliyle yazılmış resmî Türkçe de aynı kalıplara takılabilir, iyi yönlendirilmiş bir model hiçbirine takılmayabilir. Verdiği şey, düzenlemeye nereden başlanacağını gösteren bir puan ve kalem kalem döküm.

```bash
python3 scripts/detect_tr_ai.py metin.md                 # okunur rapor
python3 scripts/detect_tr_ai.py metin.md --json          # makine okunur çıktı
python3 scripts/detect_tr_ai.py makale.md --register akademik-resmi
```

`--register` değerleri: `blog-deneme`, `teknik`, `kurumsal`, `akademik-resmi`, `edebi-anlati`. Register verilince `-mAktAdIr` yoğunluğu o metin türünün hedef aralığıyla karşılaştırılır.

Ölçtükleri:

- AI klişeleri (Tier-1/2/3) ve TDK tabanlı yüzey hataları
- `-mAktAdIr` yoğunluğu, art arda üç cümlede aynı ekle bitiş
- Cümle uzunluğu varyasyonu (Burstiness CoV): 0,40 ve üzeri hedef, 0,35 altı mekanik

Bilinçli davranışlar: kod bloğu, satır içi kod, HTML yorumu ve çıplak URL taranmaz. Akademik/resmî register'da `söz konusu`, `bu bağlamda` gibi kalıplar uyarı değil bilgi olarak listelenir. 50 kelimenin altında `-mAktAdIr` için "hedef dışı" uyarısı verilmez. `yıllardır`, `bugündür` gibi süre belirteçleri bildirme eki sayılmaz.

Sınırı: regex ve basit istatistikle yalnızca yüzeydeki izleri yakalar. Sola dallanma, ulaç seçimi, register uyumu gibi cümle mimarisi kararlarını ölçmez; onlar modelin ve gözün işi.

### `denetle_post.py`: yayın kapısı

Sosyal medya postu blog denetiminden geçmez: ilk 210 karakter için ayrı bir bütçe, hashtag sınırı, tek CTA ve uydurulmuş sayı yasağı vardır. Bu betik postu yayına çıkmadan önce ölçer ve `hata` varsa kapıyı kapatır.

```bash
python3 scripts/denetle_post.py post.md                    # tek post
python3 scripts/denetle_post.py takvim/                    # bütün postlar
python3 scripts/denetle_post.py --takvim takvim/           # postlar arası tekrar ve denge
python3 scripts/denetle_post.py post.md --canli            # link sağlığı (K17)
python3 scripts/denetle_post.py post.md --json             # makine okunur çıktı
python3 scripts/denetle_post.py post.md --katı             # uyarılar da kapıyı kapatır
python3 scripts/denetle_post.py post.md --kural-kapat K12,K14
python3 scripts/denetle_post.py post.md --config post-kapisi.json
```

`--platform linkedin|instagram|x`, `--tur tanitim|teknik|ipucu|carousel` ve `--metin` (dosya yerine doğrudan metin) seçenekleri de var.

<details>
<summary><b>Kural kataloğu (K0-K17)</b></summary>

| Kural | Ne ölçer | Varsayılan |
| :--- | :--- | :--- |
| K0 | Platform bütçesi, hook, hashtag, paragraf, emoji, CTA, tekrar | hata / uyarı |
| K1 | Zorunlu bölümler | hata / uyarı |
| K2 | Carousel: 6 slayt, TR + EN eşliği | hata |
| K3 | Slayt uzunluğu (kapak 10, slayt 14 kelime) | uyarı |
| K4 | EN satırda Türkçe harf, eksik çeviri | uyarı |
| K5 | A tipi repo linki metinde | hata (LinkedIn) |
| K6 | Fork beyanı | uyarı |
| K7 | Teknoloji ve lisans iddiası | hata / uyarı |
| K8 | Private sızıntısı (kurulum komutu, link, gizlilik beyanı) | hata |
| K9 | E-posta, telefon, IBAN, token, IP, yerel yol | hata |
| K10 | Teknoloji adı yazımı (`Github` → `GitHub`) | uyarı |
| K11 | Özellik yığını (4+ madde, 6+ ögeli cümle) | uyarı |
| K12 | İç jargon (`Faz 3`, `W46`, `sprint`) | uyarı |
| K13 | Bozuk kodlama (mojibake) | hata |
| K14 | Sürüm ve durum iddiası notu | uyarı |
| K15 | Postlar arası tekrar | uyarı / hata |
| K16 | İçerik sütunu dengesi | bilgi |
| K17 | Canlı link sağlığı (`--canli`) | hata / uyarı |

`hata` yayını engeller (çıkış kodu 1), `uyarı` engellemez, `bilgi` yalnızca kayıt düşer. `post-kapisi.json` kural bazında seviye ezer: `{"K12": "bilgi"}`. `--kural-kapat` tek seferlik istisna bırakır ve raporda görünür.

</details>

### `run_tests.py` ve `build_dist.py`

```bash
python3 scripts/run_tests.py      # 51 test: paket bütünlüğü, dedektör, post kapısı, evaller
python3 scripts/build_dist.py     # dist/ dosyasını derle, skills/ ile eşle
```

`run_tests.py` raporu `docs/TEST_VE_DOGRULAMA_RAPORU.txt` dosyasına kendisi yazar (`--no-report` ile kapatılır). Rapor elle düzenlenmez; bayatlamasın diye üretimi otomatikleştirildi. Aynı komut GitHub Actions üzerinde her push ve pull request'te koşar, ardından `build_dist.py` sonrası `git diff --exit-code` ile `dist/` senkronu denetlenir.

## Güvenlik

Paket, modele verilen Markdown talimatlarından ve üç yerel Python betiğinden oluşur. Betikler ağa çıkmaz, komut çalıştırmaz, harici kütüphane kullanmaz.

| Betik | Ne yapar | Dosya yazar mı |
| :--- | :--- | :--- |
| `scripts/detect_tr_ai.py` | Metni okur, raporu ekrana basar | Hayır |
| `scripts/denetle_post.py` | Postu ve takvimi denetler; `--canli` verilirse URL'lere HTTP isteği atar | Hayır |
| `scripts/run_tests.py` | Paket, dedektör ve eval senaryolarını denetler | Yalnızca `docs/TEST_VE_DOGRULAMA_RAPORU.txt` |
| `scripts/build_dist.py` | `dist/` üretir, `skills/turkish-anti-ai-skill/` klasörünü eşler | Yalnızca depo içinde |

`build_dist.py` eşleme sırasında `skills/turkish-anti-ai-skill/references/` klasörünü silip yeniden kopyalar. Güvenlik tarayıcıları (Socket, Snyk) bu satırı dosya silme olarak işaretleyebilir. Silme kilitle korunuyor: hedef bu tek klasör değilse ya da symlink ise betik hiçbir şey silmeden durur. `--canli` dışında hiçbir betik dışarıya istek atmaz.

## Depo Yapısı

```text
turkish-anti-ai-skill/
├── SKILL.md                           # Ana orkestratör: YAML frontmatter + 4 adımlı iş akışı
├── skills/turkish-anti-ai-skill/      # npx skills ve plugin paketleyici için uyum dizini
├── references/                        # İhtiyaç anında okunan dilbilimi veritabanı
│   ├── sentaks-ve-morfoloji.md        # Sola dallanma, ulaçlar, vurgu, -DIr/-mAktAdIr, pro-drop
│   ├── ai-turkcesi-sozlugu.md         # Tier-1/2/3 sözlük (60+ kalıp) ve sohbet artıkları
│   ├── tdk-ve-noktalama.md            # [TDK]/[Üslup] kuralları, imla, fonetik ek tablosu
│   ├── register-ve-ornekler.md        # 5 register × 9 boyut matrisi, Before/After örnekleri
│   └── sosyal-medya.md                # Post register'ı, hook, bütçe, CTA, kapı kuralları
├── scripts/
│   ├── detect_tr_ai.py                # Deterministik AI-slop, TDK ve CoV tarayıcısı
│   ├── denetle_post.py                # Sosyal medya postu yayın kapısı (K0-K17)
│   ├── run_tests.py                   # Paket + dedektör + post kapısı + eval testleri
│   └── build_dist.py                  # dist/ ve skills/ derlemesi
├── evals/evals.json                   # Olgusal sadakat ve anti-slop regresyon senaryoları
├── dist/turkish-anti-ai-skill.full.md # Web arayüzleri için tek dosya
├── docs/
│   ├── ARASTIRMA_VE_MIMARI_RAPORU.md  # Dilbilimi ve anti-AI mimari araştırması
│   ├── DENETLE_POST_GELISTIRME_PLANI.md
│   └── TEST_VE_DOGRULAMA_RAPORU.txt   # run_tests.py üretir, elle düzenlenmez
├── .cursor/rules/turkish-anti-ai-skill.mdc
├── .claude-plugin/plugin.json         # Claude Code / Cowork manifestosu
├── .github/workflows/tests.yml        # CI: testler + dist senkronu
├── AGENTS.md · CLAUDE.md · GEMINI.md  # Ajan adaptörleri
├── CONTRIBUTING.md
└── LICENSE                            # MIT
```

## Katkı

Yeni bir yapay zekâ Türkçesi kalıbı, çeviri kokan bir SaaS ifadesi veya TDK sınır durumu fark ettiysen Issue ya da Pull Request açabilirsin.

Kurala dayanak gerekir. `[TDK]` etiketi için kılavuzdan madde bağlantısı, `[Dil bilgisi]` için kuralın bozulduğunda anlamı kaydıran örnek, `[Üslup]` için register istisnası istenir. Öznel beğeni tek başına yeterli değil. Şablon ve doğrulama adımları [`CONTRIBUTING.md`](CONTRIBUTING.md) dosyasında.

Değişiklikten sonra:

```bash
python3 scripts/build_dist.py && python3 scripts/run_tests.py
```

## Lisans

[MIT](LICENSE). Kullan, değiştir, dağıt.

Yazar: [Yüce Zerey](https://github.com/yucezerey) · Agent Skills Specification v1.0
