# denetle_post.py Geliştirme Planı: Yazılım Projesi Postları

Durum: **uygulandı** (faz 0-5) · Tarih: 2026-11-11 · Kapsam: `C:/Orca/turkish-anti-ai-skill` + `C:/Orca/Command Center/is/marketing`

Amaç: kapıyı genel "post yazım denetimi"nden, **yazılım projesi tanıtım postu** denetimine çıkarmak. Bugün kapı dil ve platform kurallarını ölçüyor; projeye özgü olan üç şeyi ölçmüyor: **carousel slayt metni, proje iddiaları ve sızıntı.**

## 1. Bugünkü durum

Kapı şu anda yayınlanacak metni (gövde + CTA + hashtag ya da caption + hashtag) kurup 11 kalemi ölçüyor: karakter sınırı, ilk satır uzunluğu, hook klişesi, hashtag bütçesi, paragraf yığını, emoji/emoji bullet, kalın etiketli liste, CTA sayısı, yer tutucu/yol/link sızıntısı, `tip: B` gizlilik beyanı, sayı uydurma, tekrar eden cümle, dedektör kalıpları.

Yazılım projesi postunda eksik kalanlar (12 postluk takvim üzerinde doğrulandı):

| Boşluk | Neden önemli | Bugünkü davranış |
|---|---|---|
| Instagram carousel slaytları | Slayt metni görsele basılıyor, yayına çıkıyor; kapı yalnızca `Caption` + `Hashtag` bakıyor | Hiç denetlenmiyor |
| EN slayt eşliği | `dil: tr+en` postlarda EN metin eksik/boş kalabiliyor | Hiç denetlenmiyor |
| A tipi repo linki | `kaynak:` dolu ama gövdede link yoksa post tıklanmıyor | Yalnızca "private ise link olmasın" var |
| Fork beyanı | Fork repoyu kendi ürünü gibi anlatmak yanlış beyan (envanter kuralı) | Denetlenmiyor |
| Teknik iddia | "233 test", "Flutter", "Apache-2.0", "sunucu yok" gibi iddialar doğruluk notundan gelmeli | Yalnızca sayılar |
| Sır/kişisel veri | Ekran görüntüsünden kopyalanan e-posta, telefon, IP, token, kullanıcı yolu | Denetlenmiyor |
| Özellik yığını | Yazılım postlarının en sık hatası: 5 maddelik özellik listesi | Yalnızca paragraf ve kalın etiket |
| Teknoloji adı yazımı | `Github`, `Javascript`, `Nodejs`, `Postgres` | Denetlenmiyor |
| İç jargon | "Faz 0-6", "W46", "sprint" dışarıdaki okura bir şey söylemez | Denetlenmiyor |
| Postlar arası tekrar | Aynı açılış kalıbı 12 postta tekrarlarsa hesap şablon gibi okunur | Denetlenmiyor |
| Bozuk kodlama | Windows'ta `Ã¼`, `ÄŸ` gibi mojibake yayına gidebilir | Denetlenmiyor |

## 2. Tasarım kararları

**2.1 Profil = platform × post türü.** `platform` (linkedin | instagram | x) mevcut. Üstüne `tür` eklenir: `tanitim`, `teknik`, `ipucu`, `carousel`. Tür `-ipucu-` dosya adından, `tip: A/B` frontmatter'ından ve `kanal: ig` + slayt bölümlerinden türetilir; `--tur` ile ezilebilir. Her profilin kelime bütçesi, zorunlu bölümleri ve hashtag aralığı olur (`proje-tanitim-postu` skill'indeki 110-170 / 150-250 kuralıyla aynı).

**2.2 Kural kimlikleri.** Bulgular `K` grubu altında toplanır (`K1`...`K17`). Mevcut `kod` adları korunur (entegrasyon ve alışkanlık bozulmasın), yeni bulgular `K` kimliğiyle gelir; `--json` çıktısı `surum: 2` olur ve her bulguya `kural` alanı eklenir.

**2.3 Sıkılık.** Varsayılan: dil/TDK ve platform sınırı **hata**, proje iddiası ve üslup **uyarı**. Üç kaçış yolu var, üçü de denetlenebilir:
1. `--katı` (uyarılar da kapatır, mevcut).
2. `--kural-kapat K12,K14` (bilinçli istisna, raporda "kapatıldı" satırı görünür).
3. `post-kapisi.json` (marketing tarafı): kural bazında seviye ezme, ör. `{"K12": "bilgi"}`.

**2.4 Deterministik kalır.** Ağ yalnızca `--canli` ile, model/puanlama hiç yok. Aynı girdi aynı çıktı.

## 3. Kural kataloğu

| K | Ad | Seviye | Ne ölçer | Örnek tetik |
|---|---|---|---|---|
| K0 | Yayın biçimi | hata / uyarı | Platform bütçesi, hook, hashtag, paragraf, emoji, CTA, tekrar (kapının eski kuralları) | 3200 karakter, 6 hashtag |
| K1 | Zorunlu bölüm | hata | Profil başına gövde/caption, CTA (veya slayt 6), hashtag, doğruluk notu | `# CTA` yok |
| K2 | Carousel bütünlüğü | hata | Kapak + 5 slayt, her slaytta TR ve EN satırı, slayt numarası sürekliliği | `# Slayt 4` yok, `EN:` boş |
| K3 | Slayt uzunluğu | uyarı | Kapak ≤ 10 kelime, gövde slaytı ≤ 14 kelime | Kapak 22 kelime |
| K4 | Slayt dili | uyarı | EN satırda Türkçeye özgü harf, EN kelime sayısı TR'nin %50'sinden az | `EN: Atölye için demo` |
| K5 | A tipi link | hata | `kaynak:` URL'si gövde/caption'da birebir geçmeli | `kaynak: github.com/...` var, metinde yok |
| K6 | Fork beyanı | uyarı | `tip` içinde `fork` var + gövde "yazdım/geliştirdim" diyor + doğruluk notu upstream'i anmıyor | "GoodbyeDPI'ı yazdım" |
| K7 | İddia izi | uyarı | Gövdede geçen teknoloji/ölçüm iddiası doğruluk notunda geçmeli: `Flutter, Node.js, Apache-2.0, test, tablo, offline, sunucu yok, ücretsiz, açık kaynak, MVP, beta, v1.x` | Gövde "Apache-2.0", notta yok |
| K8 | Private sızıntı | hata | `kaynak: private` iken repo linki, `git clone`, `npm i`, `docker run` | B tipi postta kurulum komutu |
| K9 | Sır taraması | hata | E-posta, telefon, IBAN, `sk-`/`ghp_`/`Bearer`, IPv4, `C:\Users\...`, `/home/...` | `C:\Users\bahat\...` |
| K10 | Teknoloji adı | uyarı | `Github, Javascript, Typescript, Nodejs, Postgres, Reactjs, Vuejs, dotnet` yazımları | `Github` |
| K11 | Özellik yığını | uyarı | 4+ ardışık madde, ya da 5+ özelliği tek cümlede `ve` ile dizmek | 6 maddelik özellik listesi |
| K12 | İç jargon | uyarı | `Faz N`, `W46`, `sprint`, `epic`, `ticket`, `PR #` gövdede | "Faz 0-6 bitti" |
| K13 | Bozuk kodlama | hata | `Ã`, `ÄŸ`, `ÅŸ`, `Â` kalıpları | `TÃ¼rkÃ§e` |
| K14 | Sürüm iddiası | uyarı | `beta`, `MVP`, `v1.2` varsa doğruluk notunda sürüm/durum satırı | "v2 yayında", notta yok |
| K15 | Takvim tekrarı | uyarı / hata | Postlar arası: ilk 6 kelime aynı (uyarı), 5-gram örtüşmesi ≥ %60 (uyarı), aynı proje 2 hafta üst üste (hata) | İki post aynı açılışla başlıyor |
| K16 | Haftalık denge | bilgi | Eğitici / kanıt / tanıtım dağılımı (skill: %40 / %15 / %10) | 4 haftada 9 tanıtım |
| K17 | Canlı link | hata/uyarı | `--canli`: `kaynak` ve demo URL'lerine HEAD; 404/410 hata, 5xx/redirect zinciri uyarı | Demo 404 |

K15/K16 yalnızca `--takvim <dizin>` modunda çalışır. K17 yalnızca `--canli` ile; varsayılan kapalı.

## 4. Fazlar

| Faz | İş | Dosya | Kabul | Göreli süre |
|---|---|---|---|---|
| 0 | Profil altyapısı, `K` kimlikleri, `surum: 2`, `--tur`, `--kural-kapat` | `scripts/denetle_post.py` | Mevcut 12 postta bulgu kümesi değişmez; yalnızca kimlik/şema değişir | 0.5 gün |
| 1 | K1-K4: bölüm zorunluluğu + carousel slayt denetimi + EN eşliği | aynı dosya + `references/sosyal-medya.md` | 4 IG postu yeşil; slaytı bozuk fixture hata verir | 1 gün |
| 2 | K5-K9: repo linki, fork beyanı, iddia izi, private sızıntı, sır taraması | aynı dosya | 12 postta hata 0; 6 fixture yakalanır | 1 gün |
| 3 | K10-K14: teknoloji adı, özellik yığını, jargon, kodlama, sürüm | aynı dosya | Fixture yakalanır, mevcut postlarda yeni hata yok | 0.5 gün |
| 4 | K15-K16: `--takvim` modu, tekrar ve denge raporu; marketing `--takvim` passthrough | `denetle_post.py`, `is/marketing/post-kapisi.mjs` | `post-kapisi.mjs --takvim` çalışır, mevcut 12 post raporu çıkar | 1 gün |
| 5 | K17: `--canli` link kontrolü | `denetle_post.py` | Varsayılan kapalı; `--canli` ile 404 fixture hata verir | 0.5 gün |

Her faz kendi başına yayınlanabilir. Faz 1 tek başına en yüksek değeri taşır: carousel metni bugün hiç denetlenmiyor.

## 5. Kalibrasyon kuralı

Yeni her kural, 12 mevcut post üzerinde **hata 0** üretecek şekilde kalibre edilir. Bir kural mevcut postta hata veriyorsa iki seçenek var: kural daraltılır ya da o post gerçekten düzeltilir. Kuralı "yeşil görünsün" diye seyreltmek yasak; hangi seçeneğin neden seçildiği faz raporuna yazılır.

## 6. Doğrulama

```bash
# 1. Kapı testleri (fixture'lar dahil)
python3 scripts/run_tests.py

# 2. Mevcut takvim üzerinde ölçüm: hata 0 beklenir
python3 scripts/denetle_post.py "C:/Orca/Command Center/is/marketing/takvim"

# 3. Takvim modu (faz 4 sonrası)
python3 scripts/denetle_post.py --takvim "C:/Orca/Command Center/is/marketing/takvim"

# 4. Marketing entegrasyonu
node "C:/Orca/Command Center/is/marketing/post-kapisi.mjs"
node "C:/Orca/Command Center/is/marketing/zamanla.mjs" --dry-run

# 5. Dist senkronu
python3 scripts/build_dist.py && python3 scripts/run_tests.py
```

Kabul ölçütleri:

1. `run_tests.py` 28 testten **40+ teste** çıkar, hepsi yeşil; her yeni `K` için en az bir pozitif ve bir negatif fixture.
2. Mevcut 12 postta `hata = 0`; uyarı listesi tek tek gerekçelendirilir.
3. `--json` şeması `surum: 2`, kural kimlikleri sabit; `post-kapisi.mjs` ve `zamanla.mjs` kod değişikliği olmadan çalışır.
4. Tek post < 0.3 sn, 12 post < 3 sn.
5. Yeni bağımlılık yok (yalnızca standart kütüphane).
6. `--canli` ağ erişimi olmayan ortamda sessizce atlanmaz, açık hata verir.

## 7. Geri dönüş

- Kurallar eklemeli; davranış değişikliği `post-kapisi.json` ile kural bazında geri alınabilir (`"K12": "bilgi"`).
- `--kural-kapat` tek seferlik istisna bırakır, raporda görünür.
- Tek faz geri alınacaksa `git revert <commit>`; kural kataloğu dosya başında tablo olarak durur, kimlik çakışması olmaz.

## 8. Yapılmayacaklar

- Model tabanlı "AI mı insan mı" puanı veya yazar tespiti.
- Postu kendiliğinden yeniden yazma (kapı raporlar, yazmaz).
- README/repoyu uzaktan okuyup iddia doğrulama (faz 5 yalnızca HTTP durum kodu bakar).
- Platform API'sine yazma; zamanlama davranışını değiştirme.

## 9. Riskler

| Risk | Etki | Azaltma |
|---|---|---|
| K7 iddia izi çok gürültülü olur | Ekip kapıyı kapatır | Yalnızca kapalı sözlükten (Flutter, Node.js, test, lisans...) bakar; uyarı seviyesinde başlar |
| K15 takvim modu yavaşlar | 12 post < 3 sn hedefi | Tek geçişte okuma, 5-gram karşılaştırması yalnızca ilk 40 cümlede |
| K2 slayt ayrıştırması başlık biçimine bağlı | Yanlış "slayt yok" hatası | Başlık biçimi esnek (`Slayt 2`, `Slayt 2: Problem`, `2 - Problem`), fixture'da üçü de denenir |
| K9 sır taraması yanlış pozitif | Gerçek sayı/telefon metni | Telefon yalnızca `+90`/`0 5xx` deseniyle, IBAN `TR\d{24}` ile |
| Yeni kurallar mevcut postları kırar | Zamanlama durur | Bölüm 5 kalibrasyon kuralı + `--kural-kapat` |


## 10. Uygulama sonucu (2026-11-11)

| Faz | Durum | Kanıt |
|---|---|---|
| 0 | ✅ | `--tur`, `--config`, `--kural-kapat`, `surum: 2`, her bulguda `kural` alanı |
| 1 | ✅ | K2/K3/K4 + slayt klişe taraması; 4 IG postu 6 slayt, TR+EN |
| 2 | ✅ | K5-K9; private postta `git clone`, token ve e-posta yakalanıyor |
| 3 | ✅ | K10-K14; `Github`, 4 madde, `Faz 3`, `TÃ¼rkÃ§e`, `v2.1` fixture'ları |
| 4 | ✅ | `--takvim` + K15/K16; marketing `post-kapisi.mjs --takvim` |
| 5 | ✅ | `--canli` + K17; ulaşılamayan adres hata, sessiz geçmez |

Plan dışı iki karar:

1. **K5 Instagram'da uyarı.** Instagram caption'ında link tıklanmaz; `barber_shops-ig` linki slayt 6'da taşıyor. LinkedIn'de eksik link hata, Instagram'da "link yalnızca slaytta, bio'ya ekle" bilgisi verilir. Fork postları da A tipi sayılır: kendi çatalının linki metinde olmalı.
2. **Doğruluk notu eksikliği uyarı, hata değil.** 4 IG postunda not yok; hata yapılsaydı mevcut takvim kırmızı olurdu. Not eksikse K7 "denetlenmedi" uyarısı verir.

Doğrulama:

```text
python3 scripts/run_tests.py        -> 49/49 (post kapısı 27 test)
python3 scripts/denetle_post.py takvim  -> 12 post, hata 0
node is/marketing/post-kapisi.mjs --takvim -> 0 hata, 0 uyarı (K16 bilgi)
node is/marketing/zamanla.mjs --dry-run -> çıkış 0
süre: 12 post tek çağrıda ~0.2 sn
```
