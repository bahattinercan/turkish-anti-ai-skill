# Sosyal Medya Register'ı (LinkedIn, Instagram, X)

Post, blog yazısının kısaltılmış hâli değildir. Okurun kararı ilk iki satırda verilir, satır kırılması noktalama işlevi görür, metin 3 ile 12 cümle arasında biter. Bu yüzden blog kuralları postta tek başına yetmez: cümle sayısı az olduğu için cümle ritmi (CoV) ölçümü güvenilir değildir ve modelin en yoğun ürettiği kalıplar tam olarak post açılışlarında toplanır.

Bu dosya, `SKILL.md` içindeki üç katmanlı dönüşümün post register'ına uyarlanmış hâlidir. Denetimi `scripts/denetle_post.py` yapar; buradaki eşikler o betiğin eşikleriyle aynıdır.

## 1. Post Cümlesinin Geometrisi

| Bölüm | Kural | Yasak |
| :--- | :--- | :--- |
| Açılış (hook) | Tek somut olgu, 12 kelimeyi geçmez, merak boşluğu bırakır | "Bu yazıda", "Bugün sizlere", "Gururla duyuruyoruz" |
| Gövde | Paragraf başına 1 ile 3 cümle, tek fikir | 5 cümlelik blok, madde imi yığını |
| Kanıt | Sayı, ekran görüntüsü, süre, kısıt | "Yüzlerce ekip", "büyük ilgi" |
| Kapanış | Tek istem (CTA) ya da hiç kapanış cümlesi | Ders veren özet, "Sonuç olarak" |
| Hashtag | Sonda, 2 ile 5 (LinkedIn), 3 ile 10 (Instagram) | Gövde içine serpiştirilmiş etiket |

Postta yeni paragraf, nefes demektir. Arka arkaya beş cümleyi tek blokta vermek, okurun kaydırma kararını hızlandırır. Paragrafı bölmek için cümle ekleme; cümleyi bitir, satır atla.

## 2. Platform Bütçeleri

| Platform | Sert sınır | Görünen kısım | Hashtag | Not |
| :--- | :--- | :--- | :--- | :--- |
| LinkedIn | 3000 karakter | ilk 210 karakter ("devamını gör" öncesi) | 2 ile 5 | Kalın yazı ve madde imi ham görünür, yayın metninde kullanma |
| Instagram (caption) | 2200 karakter | ilk 125 karakter | 3 ile 10 | 30 etiket üstü spam sayılır, işlevsiz etiket taşıma |
| X | 280 karakter | tamamı | 0 ile 2 | Ulaç ve kısa cümle şart, giriş cümlesi lüks |

LinkedIn'in ilk 210 karakteri, postun tamamından daha çok okunur. Bu alanı "Merhaba, bugün..." ile harcama.

## 3. Postta En Sık Görülen On İki Kalıp

| AI kalıbı | Yerine ne yazılır |
| :--- | :--- |
| "Gururla duyuruyoruz ki X yayında" | "X yayında." |
| "Bu yazıda X'i ele alacağız" | Doğrudan X'in kendisi |
| "Sadece X değil, aynı zamanda Y" | "X yapıyor. Y de var." |
| "Heyecan verici haber 🚀" | Haberin kendisi, sayıyla |
| "Büyük bir adım attık" | Atılan adım, ölçülebilir hâliyle |
| "Kritik bir rol oynuyor" | Ne yaptığı, fiille |
| "Unutmayın:" / "Şunu belirtmeliyim ki" | Sil; cümle kendi başına dursun |
| "Katılıyor musunuz? Yorumlarda buluşalım 👇" | Tek somut soru, tek istem |
| Kalın etiketli liste (`**Neden?** ...`) | Düz cümle, gerekiyorsa üç maddelik kısa liste |
| "Hızlı, güvenilir ve ölçeklenebilir" | Gerçek sayı ya da tek sıfat |
| "Yapay zekâ çağında" / "dijitalleşen dünyada" | Tarih, ürün adı, somut bağlam |
| "Sonuç olarak" / "Özetle" | Sil, son cümleyi olduğu gibi bırak |

Liste hâlinde değil de cümle içinde gelen kalıplar için `references/ai-turkcesi-sozlugu.md` geçerlidir. Post burada yalnızca yoğunlaşma noktasıdır: aynı klişe blogda bir kez, postta bir kez geçse bile postun tamamının üçte birini kaplar.

## 4. Ritim, Emoji ve Noktalama

- Emoji bir noktalama değil, ton işaretidir. Post başına 0 ile 3 arası; her satırın başına emoji koymak madde imi yerine geçen süslemedir, sil.
- Satır başına emoji koyup altına tek cümle yazma alışkanlığı (emoji bullet) modelin en belirgin parmak izidir. Madde gerekiyorsa `-` kullan ya da düz paragraf yaz.
- Üç nokta, ünlem ve büyük harf vurgusu: post başına bir tane. "MUHTEŞEM!!!" yerine sayı.
- Uzun çizgi (`—`) yasak. Ara söz gerekiyorsa cümleyi ikiye böl ya da virgül kullan ([TDK], `references/tdk-ve-noktalama.md`).
- Hashtag'ler gövdenin sonunda, tek satırda. `#yapayzeka #inovasyon #gelecek` gibi anlamsız üçlü yerine konuyu arayan üç etiket.

## 5. CTA: Tek İstem, Tek Fiil

| Kötü | Neden | İyi |
| :--- | :--- | :--- |
| "Düşüncelerinizi yorumlarda paylaşın, beğenin, kaydedin, paylaşın" | Dört istem, hiçbiri yapılmaz | "Kasa kapanışı ekranını görmek istersen DM at." |
| "Detaylar için profilimdeki linke göz atabilirsiniz" | Belirsiz, tıklama maliyeti yüksek | "Demo: local-ai-news.vercel.app" |
| "Katılıyor musunuz?" | Cevabı bedava, etkileşim üretmez | "Sizin dükkânda kasa sayımı kaç dakika sürüyor?" |

CTA bir cümledir. İkinci bir istem eklemek, birincisinin yapılma olasılığını düşürür. Ürün postunda (B tipi) istem "DM at / demo iste" olur; açık kaynak postunda (A tipi) doğrudan çalıştırılabilir komut ya da demo linki verilir.

## 6. Olgusal Sadakat Kilidi Postta Nasıl Çalışır

Post, iddianın en yoğun olduğu yerdir: "233 test yeşil", "18 tablo", "3 haftada bitti". Her sayı `# Teknik doğruluk notu` bölümünde karşılığını bulmak zorundadır. Notta olmayan sayı postta görünüyorsa iki seçenek var: sayıyı sil ya da notu gerçek kaynaktan tamamla.

- Yuvarlama da bilgidir: "yaklaşık 230 test" yazmak, 233 sayısını gizlemek için bahane değil.
- Ölçülmemiş şey övülmez: "çok hızlı" yerine ölçülen süre, ölçüm yoksa sıfat da yok.
- Müşteri işi postlarda (`tip: B`) müşteri adı, tutar, telefon, adres maskelenmeden yayına çıkmaz. Post dosyasında `gizlilik: kontrol edildi` satırı bunun beyanıdır.
- `kaynak: private` ise gövdede, CTA'da ve görsel üstünde repo linki olmaz. "Private repo ama link şurada" çelişkisi kapıda hata verir.

## 7. Yazılım Projesi Postu

Proje postu, dil kurallarına ek olarak iddia kurallarına tabidir. Kapı bu bölümü `K1` ile `K17` arasındaki kurallarla ölçer.

**Post tipi ve link.** `tip: A` açık kaynak demektir: `kaynak:` satırındaki URL gövdede birebir geçmeli (`K5`). LinkedIn'de eksik link hatadır. Instagram caption'ında link tıklanmaz; link slayt 6'da ya da bio'da durur, bu yüzden orada uyarı sayılır. `tip: B` ürün demektir: link ve kurulum komutu (`git clone`, `npm i`, `docker run`) yasak (`K8`), `gizlilik: kontrol edildi` satırı zorunlu.

**Fork beyanı.** `tip` içinde `fork` geçiyorsa doğruluk notu upstream projeyi anmalı (`K6`). Fork bir repoyu kendi ürünün gibi anlatan cümle (`yazdım`, `geliştirdim`) denetimde uyarı alır. Doğru çerçeve: "X projesinin Türkiye için düzenlenmiş sürümü".

**İddia izi.** Gövdede geçen teknoloji, lisans ve ölçüm iddiası (`Flutter`, `Node.js`, `Apache-2.0`, `açık kaynak`, `sunucu yok`, `offline`) doğruluk notunda karşılığını bulmalı (`K7`). Sayılar daha sıkı kurala tabidir: notta olmayan sayı hatadır, alıntı içindeki sayı uyarıdır. `MVP`, `beta`, `v1.2` gibi sürüm iddiaları da notta geçmeli (`K14`).

**Carousel.** Instagram postu 6 slayttır: kapak + 5. Her slaytta `TR:` ve `EN:` satırı olmalı (`K2`); kapak 10, diğer slaytlar 14 kelimeyi geçmez (`K3`); EN satırda Türkçe harf olmaz, çeviri TR'nin yarısından kısa kalmaz (`K4`). Slayt metni de kapak klişesi taramasından geçer; görsele basılan cümle caption'dan daha çok okunur.

**Temizlik.** Postta e-posta, telefon, IBAN, API anahtarı, IP adresi ve yerel dosya yolu olmaz (`K9`). Ekran görüntüsünden kopyalanan bir token yayına giderse geri dönüşü yoktur.

**Dil.** `Github`, `Javascript`, `Nodejs`, `Postgres` gibi yazımlar düzeltilir (`K10`). 4+ ardışık madde ya da tek cümlede 6+ öge özellik yığını sayılır (`K11`). `Faz 3`, `W46`, `sprint` gibi iç jargon dışarıdaki okura bir şey söylemez (`K12`).

## 8. Kapı: Ölç, Sonra Yayınla

Post yazıldıktan sonra, zamanlamadan önce tek komut:

```
python3 scripts/denetle_post.py <post-dosyasi>
python3 scripts/denetle_post.py --takvim <takvim-dizini>   # postlar arası tekrar ve denge
python3 scripts/denetle_post.py <post.md> --canli          # kaynak/demo URL'lerini yokla
python3 scripts/denetle_post.py <post.md> --kural-kapat K12,K14
python3 scripts/denetle_post.py <post.md> --config post-kapisi.json
```

Betik yayınlanacak metni (gövde + CTA + hashtag ya da caption + hashtag) yeniden kurar ve platform bütçesini, hook'u, hashtag sayısını, paragraf yığınını, emoji kullanımını, CTA sayısını, carousel slaytlarını, proje iddialarını, sızıntıyı ve AI kalıplarını ölçer.

| Kural | Ne ölçer | Varsayılan |
| :--- | :--- | :--- |
| K0 | Platform bütçesi, hook, hashtag, paragraf, emoji, CTA, tekrar | hata / uyarı |
| K1 | Zorunlu bölümler (gövde, CTA, hashtag) | hata / uyarı |
| K2 | 6 slayt, TR + EN eşliği | hata |
| K3 | Kapak 10, slayt 14 kelime | uyarı |
| K4 | EN satırda Türkçe harf, kısa çeviri | uyarı |
| K5 | A tipi repo linki metinde | hata (LinkedIn) |
| K6 | Fork beyanı | uyarı |
| K7 | İddia ve sayı doğruluk notunda | hata / uyarı |
| K8 | Private sızıntısı, gizlilik beyanı | hata |
| K9 | E-posta, telefon, IBAN, token, IP, yerel yol | hata |
| K10 | Teknoloji adı yazımı | uyarı |
| K11 | Özellik yığını | uyarı |
| K12 | İç jargon | uyarı |
| K13 | Bozuk kodlama | hata |
| K14 | Sürüm/durum iddiası notta | uyarı |
| K15 | Postlar arası tekrar, üst üste tanıtım | uyarı / hata |
| K16 | İçerik sütunu dengesi | bilgi |
| K17 | Canlı link sağlığı (`--canli`) | hata / uyarı |

Çıkış kodları: `0` temiz, `1` en az bir hata var (yayınlanmaz), `2` dosya ya da kullanım hatası. `--katı` verilirse uyarılar da kapıyı kapatır. Rapor `hata` (yayını engeller), `uyarı` (yayınlanabilir ama düzeltilmeli), `bilgi` (kayıt amaçlı) olarak ayrılır. `post-kapisi.json` ile kural bazında seviye ezilir; ezilen bulgu raporda `(ezildi)` görünür.

Kapıyı "çok katı" bulup kapatmak, postu AI yazan kişinin kendi yazısını denetlememesi demektir. Hata varsa metni düzelt; kuralı esnetme. Gerçekten istisna gerekiyorsa `--kural-kapat` kullan ve gerekçesini post dosyasına yaz.

## 9. Before / After

**LinkedIn, ürün postu**

Önce:
> Heyecan verici bir haber! 🚀 Mahalle bakkalları için geliştirdiğimiz yenilikçi kasa çözümüyle, sadece satış süreçlerini değil, aynı zamanda stok yönetimini de bir üst seviyeye taşıyoruz. Bu çözüm, günümüzün hızla değişen perakende dünyasında kritik bir rol oynamaktadır. Sonuç olarak, işletmelerin verimliliğini artırmalarına yardımcı oluyoruz.

Sonra:
> Mahalle bakkalı için çevrimdışı bir kasa yazdım: satış, stok, alış ve veresiye. Sunucu yok, internet gerekmiyor.
>
> Veresiye ayrı bir ekran değil. Müşteri kartı, borç ve ödeme geçmişi aynı yerde duruyor.
>
> Gün sonu tek düğme: nakit, kart ve veresiye tek ekranda toplanıyor, fiş PDF olarak çıkıyor.
>
> Bakkal, market ya da küçük dükkân işleten birini tanıyorsan yorumda etiketle; kasa kapanışı ekranını DM'den göstereyim.

**Instagram, caption**

Önce:
> ✨ Yeni bir dönem başlıyor! ✨
> 💡 Atölyeler için devrim niteliğinde bir çözüm
> 🔥 Sipariş takibi artık çok kolay
> 👉 Detaylar için profildeki linke göz atın!
> #inovasyon #teknoloji #gelecek #girişimcilik #yazılım #üretim #atölye #dijital #başarı #motivasyon

Sonra:
> Atölyede "bu sipariş nerede" sorusunun cevabı üç ayrı yerde duruyordu: defterde, panoda, çek listesinde.
>
> Üçünü tek ekranda birleştirdim. İş emri açılınca kimin, hangi makinede, hangi gün çalıştığı aynı satırda görünüyor.
>
> #siparistakibi #atölyeyazılımı #yerliyazılım

**LinkedIn, ipucu postu**

Önce:
> Verimlilik üzerine düşünürken şunu belirtmek gerekir ki, küçük işletmelerin en büyük sorunu kayıt düzenidir. Bu bağlamda defter tutmak yerine dijital çözümlere yönelmek, işletmenin potansiyelini ortaya çıkarmaktadır.

Sonra:
> Bakkalda gün sonu kasa sayımı uzuyorsa sorun kasa değil, kayıt düzeni.
>
> Defterde "Ahmet 250 lira" yazıyor ama hangi gün, ne için, ne kadarı ödendi belli değil. Aynı satır tarihli hareket listesine dönüşünce sayım beş dakikaya iniyor.

## 10. Post Kontrol Listesi

1. İlk satır 12 kelimeyi geçmiyor ve "Bu yazıda / Gururla duyuruyoruz / Günümüzün" ile başlamıyor.
2. Paragraf başına en fazla üç cümle; beş cümlelik blok yok.
3. Uzun çizgi, `ve` çevresi virgülü, `%12.5` gibi TDK hatası yok.
4. Emoji üçten az ve satır başlarında emoji bullet yok.
5. Hashtag sınırda: LinkedIn 2 ile 5, Instagram 3 ile 10; gövde içinde etiket yok.
6. Tek CTA var; ikinci bir istem eklenmemiş.
7. Doğruluk notundaki sayılarla posttaki sayılar aynı; teknoloji ve lisans iddiaları notta geçiyor; yeni sayı uydurulmamış.
8. A tipi ise repo linki gövdede; B tipi ise link yok ve `gizlilik: kontrol edildi` yazıyor.
9. Fork ise upstream adı doğruluk notunda; "yazdım" çerçevesi kullanılmamış.
10. Postta e-posta, telefon, IBAN, token, IP, yerel yol yok.
11. Carousel ise 6 slayt, her slaytta TR + EN; kapak 10 kelimeyi geçmiyor.
12. Teknoloji adları doğru yazılmış; 4+ maddelik özellik listesi ve `Faz/W46/sprint` jargonu yok.
13. Kapı temiz: `python3 scripts/denetle_post.py <dosya>` çıkış kodu `0`.
14. Metin, `detect_tr_ai.py` raporunda Tier-1 sinyali taşımıyor.
