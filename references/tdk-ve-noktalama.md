# TDK Yazım Kılavuzu, Noktalama ve Yüzey Kuralları Referansı

Bu referans dosyası, Büyük Dil Modellerinin (LLM) Türkçe metin üretirken yaptığı imla, noktalama ve fonetik ek hatalarını Türk Dil Kurumu (TDK) Yazım Kılavuzu ve doğal Türkçe tipografi standartlarına göre düzeltmek için kullanılır.

## 1. Noktalama: İngilizce Tipografi Kopyaları

LLM'ler İngilizce eğitim korpusundaki noktalama alışkanlıklarını Türkçe metinlere doğrudan taşır. Aşağıdaki kurallar iki türdür:

- **`[TDK]`**: TDK Yazım Kılavuzu'nda açıkça yazan kural. Her register'da geçerlidir. Kaynak: [Noktalama İşaretleri](https://yazim.tdk.gov.tr/content/09-noktalama-isaretleri.html), [Büyük Harflerin Kullanıldığı Yerler](https://tdk.gov.tr/icerik/yazim-kurallari/buyuk-harflerin-kullanildigi-yerler/).
- **`[Üslup]`**: Kılavuzda kuralı olmayan, çeviri kokusunu azaltan tercih. Register'a göre esnetilebilir ve "TDK hatası" diye raporlanmaz.

| Kural | Makine Türkçesi (Yapay) | İnsan Türkçesi (Doğal) | Gerekçe ve Kaynak |
| :--- | :--- | :--- | :--- |
| **1. Uzun çizgi (em-dash)** `[TDK]` | Kurulum sihirbazı, ara söz uzun çizgiyle ayrılmış biçimde: *"Kurulum sihirbazı (uzun çizgi) birkaç dakika içinde (uzun çizgi) projelerinizi aktarır."* | Kurulum sihirbazı birkaç dakika içinde projelerinizi aktarır. / Kurulum sihirbazı -birkaç dakika içinde- projelerinizi aktarır. | TDK: uzun çizgi *"Yazıda satır başına alınan konuşmaları göstermek için kullanılır."* Ara söz için virgül ya da başına ve sonuna bitişik yazılan kısa çizgi kullanılır (*"Küçük bir sürü -dört inekle birkaç koyun- köye giren geniş yolun ağzında durmuştu."*). |
| **2. Orta çizgi (en-dash)** `[TDK]` | Toplantı 14.00 ile 15.30 arasında, 2024 ile 2026 yıllarında yapıldı (orta çizgi ile). | Toplantı 14.00-15.30 arasında, 2024-2026 dönemini kapsıyor. | TDK aralıklarda kısa çizgi kullanır: *"Arasında, ve, ile, ila, …-den …-e anlamlarını vermek için kelimeler veya sayılar arasında kullanılır"* (`09.30-10.30`, `1914-1918`). |
| **3a. `ve / veya` çevresinde virgül** `[TDK]` | Elma, armut, ve muz aldık. | Elma, armut ve muz aldık. | TDK: *"Metin içinde ve, veya, yahut, ya … ya bağlaçlarından önce de sonra da virgül konmaz."* Tekrarlı bağlaçlarda da konmaz: *"Hem gider hem ağlar."* |
| **3b. `ama / fakat` öncesi refleks virgül** `[Üslup]` | Sistem hızlı çalışıyor, ama bellek tüketimi yüksek. | Sistem hızlı çalışıyor ama bellek tüketimi yüksek. | İngilizce `..., but` alışkanlığının kopyası. TDK Yazım Kılavuzu'nda `ama, fakat, lakin, ancak` için virgül kuralı **yoktur**. Kısa cümlede virgülsüz yazım daha doğal durur. Uzun ve karmaşık cümlede okumayı kolaylaştıran virgül hata değildir. |
| **4. Noktalı virgül köprüsü** `[Üslup]` | Model veriyi analiz eder; bu süreç yaklaşık iki saniye sürer. | Model veriyi analiz eder. Bu süreç yaklaşık iki saniye sürer. | AI, bağlaç seçmekten kaçınmak için iç virgülü olmayan iki cümleyi `;` ile yapıştırır. **Ancak noktalı virgülün TDK'da tanımlı kullanımları doğrudur** ve özellikle akademik/hukuki metinde korunur: virgülle ayrılmış tür veya takımları ayırmak (*"Erkek çocuklara Doğan, Tuğrul, Aslan, Orhan; kız çocuklara ise İnci, Çiçek, Gönül, Yonca adları verilir."*), *"Ögeleri arasında virgül bulunan sıralı cümleleri birbirinden ayırmak"* (*"Sevinçten, heyecandan içim içime sığmıyor; bağırmak, kahkahalar atmak, ağlamak istiyorum."*). |
| **5. Başlıklarda bağlaçların büyük yazılması** `[TDK]` | `## Yapay Zekâ Ve Doğal Dil İşleme Sistemlerinde Yeni Yaklaşımlar` | `## Yapay Zekâ ve Doğal Dil İşleme Sistemlerinde Yeni Yaklaşımlar` (makale alt başlığı) / `## Yapay zekâ ve doğal dil işlemede yeni yaklaşımlar` (blog, teknik belge) | TDK: *"Kitap, bildiri, makale vb.nde ana başlıktaki kelimelerin tamamı, alt başlıktaki kelimelerin ise yalnızca ilk harfleri büyük olarak yazılır."* Kelimelerin ilk harfi büyük yazıldığında *"ve, ile, ya, veya, yahut, ki, da, de sözleriyle mı, mi, mu, mü soru eki küçük harfle yazılır"* (`Suç ve Ceza`, `Leyla ile Mecnun`). Bu küçük harf kuralı yalnızca kelimelerin ilk harfi büyük yazıldığında geçerlidir. Ana başlık tamamen büyük harfle yazıldığında bağlaç ve soru eki de büyük yazılır (`YAPAY ZEKÂ VE GELECEK`, `DİL VE TARİH-COĞRAFYA FAKÜLTESİ`). Yani alt başlıkta her kelimenin büyük harfle başlaması doğru, bağlacı büyük yazmak yanlış. `[Üslup]` Blog, teknik belge ve kurumsal metinde tümce düzeni (yalnızca ilk harf büyük) daha doğal durur. |

## 2. Saat, Sayı ve Yüzde Yazımı `[TDK]`

Kaynak: [Sayıların Yazılışı](https://yazim.tdk.gov.tr/content/04-sayilarin-yazilisi.html), [Noktalama İşaretleri](https://yazim.tdk.gov.tr/content/09-noktalama-isaretleri.html).

- **Saat ve Dakika Ayracı:** TDK saat ve dakikayı iki nokta (`14:30`) ile değil, **tek nokta (`14.30`)** ile ayırır: *"Tren 09.15'te kalktı. Toplantı 13.00'te başladı."*
- **Saate Gelen Ek:** Ek, saatin **okunuşunun son sesine** uyar. Dakika sıfırsa saat okunur, dakika varsa dakika okunur. TDK örnekleri: `13.00'te` (on üçte), `11.00'de` (on birde), `17.30'da` (otuzda), `09.15'te` (on beşte). Buna göre `10.00'da` (onda), `09.00'da` (dokuzda), `16.00'da` (on altıda) **doğru**, `13.00'da` (on üç sıfır sıfırda okunmaz) ve `15.00'de` (on beşte olmalı) **yanlış** olur.
- **Ondalık Ayraç ve Binlik Basamaklar:** İngilizce sayılardaki ondalık nokta (`3.14` veya `%42.5`) Türkçede **virgül (`3,14` veya `%42,5`)** olarak yazılır: *"Sayılarda kesirler virgülle ayrılır."* Dört veya daha çok basamaklı sayılar sondan üçlü gruplara ayrılır ve aralarına nokta konur (`10.000`, `1.250.000`).
- **Yüzde İşareti:** Yüzde işareti sayıdan önce ve boşluksuz yazılır: *"Yüzde ve binde işaretleri yazılırken sayılarla işaret arasında boşluk bırakılmaz: %25"*.

## 3. Yabancı Teknik Terimler ve Türkçe Fonetiğe (Okunuşa) Göre Ek Uyumu

Teknik metinlerde yapılan en belirgin iki AI hatası şunlardır: (1) mühendislerin Türkçede hiç kullanmadığı zorlama çeviriler üretmek ve (2) İngilizce kalan terimlere yazılışına göre ek getirmektir.

### A. Zorla Çevrilmeyecek ve Çevrilecek Terimler

| Kategori | Terim Örnekleri | Doğru Uygulama |
| :--- | :--- | :--- |
| **Zorla Çevrilmeyecekler (Olduğu Gibi Bırak)** | `endpoint`, `deploy`, `middleware`, `queue`, `webhook`, `idempotent`, `payload`, `migration`, `script`, `commit`, `merge`, `rebase`, `token`, `prompt`, `fine-tuning`, `RAG`, `pipeline` | Asla *"uç nokta"*, *"göç betiği"*, *"olay güdümlü"*, *"ara katman"*, *"yük"*, *"çekme isteği"* diye çevirme, terimi olduğu gibi koru. |
| **Yerleşik Türkçesi Olanlar (Türkçesini Kullan)** | `developer` -> geliştirici, `user` -> kullanıcı, `database` -> veri tabanı (TDK yazımı, teknik metinlerde bitişik `veritabanı` da yaygın, metin boyunca birini seç), `validation` -> doğrulama, `production` -> canlı ortam, `search` -> arama, `folder` -> klasör | Sektörde doğal olarak kullanılan Türkçe karşılığını tercih et. |
| **Her İkisi de Doğal Olanlar (Tutarlılık Kuralı)** | `cache / önbellek`, `server / sunucu`, `request / istek`, `response / yanıt`, `interface / arayüz`, `file / dosya` | Metnin başında birini seç ve metin bitene kadar aynı tercihi koru (bir cümlede `server`, sonrakinde `sunucu` yazma). |

### B. Türkçe Okunuşa Göre Kesme İşareti ve Ek Tablosu

- `[TDK]` Kısaltmalara ve özel adlara gelen ekler kesmeyle ayrılır ve kısaltmanın okunuşuna uyar: *"TBMM'nin, TDK'nin, BM'de, ABD'de, TV'ye"* ([Kesme İşareti](https://tdk.gov.tr/icerik/yazim-kurallari/kesme-isareti/)). Kurum adlarına gelen ekler ise kesmeyle ayrılmaz: *"Türkiye Büyük Millet Meclisine, Türk Dil Kurumundan"*.
- `[Üslup]` `cache`, `queue`, `endpoint` gibi yabancı **cins isimlere** kesmeyle ek getirmek TDK'da düzenlenmemiştir ama teknik Türkçede yerleşik bir yazım geleneğidir. Bu durumda da ek, kelimenin **Türkçe okunuşuna (son sesine)** ve ünlü/ünsüz uyumuna göre gelir.
- Okunuşu iki türlü yaygın olan kısaltmalarda (`API`, `SQL`, `URL`) metin boyunca tek okunuş seç ve ekleri ona göre getir. İki okunuştan birine uyan eki hata sayma.

| Yabancı Terim / Kısaltma | Türkçe Okunuşu | Yanlış (AI Yazılış Tahmini) | Doğru (Okunuşa Göre Çekim) |
| :--- | :--- | :--- | :--- |
| `cache` | keş (ince ünlü, sert ünsüz) | `cache'ı`, `cache'de`, `cache'dan` | `cache'i`, `cache'te`, `cache'ten` |
| `queue` | kü (ince-yuvarlak ünlü) | `queue'ya`, `queue'da`, `queue'yı` | `queue'yu`, `queue'de`, `queue'ye`, `queue'den` |
| `SQL` | es-kü-el (ince ünlü) | `SQL'ı`, `SQL'da`, `SQL'dan` | `SQL'i`, `SQL'de`, `SQL'den` |
| `JSON` | ceyson (kalın ünlü) | `JSON'i`, `JSON'de` | `JSON'ı`, `JSON'da`, `JSON'dan` |
| `API` | api (kelime gibi, ince ünlü) veya ey-pi-ay (kalın ünlü) | `API'ye` + `API'da` gibi iki okunuşu karıştırmak | api okunuşunda `API'yi`, `API'de`, `API'den`. ey-pi-ay okunuşunda `API'ı`, `API'da`, `API'dan`. Seçilen okunuş metin boyunca korunur. |
| `URL` | u-re-le (TDK harf okunuşu) | `URL'ı`, `URL'da` | `URL'yi`, `URL'de` |
| `CPU` | si-pi-yu | `CPU'ı` | `CPU'yu`, `CPU'da` |
| `GitHub` | git-hab | `GitHub'de`, `GitHub'i` | `GitHub'da`, `GitHub'ı`, `GitHub'a` |
| `Google` | gugıl | `Google'de`, `Google'i` | `Google'da`, `Google'ı`, `Google'ın` |
| `Docker` | dakır | `Docker'de`, `Docker'i` | `Docker'da`, `Docker'ı` |
| `React` | ri-ekt | `React'ı`, `React'da` | `React'i`, `React'te` |
| `Node.js` | nod-cey-es | `Node.js'ı`, `Node.js'da` | `Node.js'i`, `Node.js'te` |

## 4. TDK Bağlaç ve Birleşik/Ayrı Kelime Denetim Tablosu

LLM'lerin ve insan yazarların en sık karıştırdığı, TDK Yazım Kılavuzu'na göre kesin kurala bağlanmış yazımlar:

| Doğru Yazım (TDK) | Sık Yapılan Yanlış | Kural / Açıklama |
| :--- | :--- | :--- |
| **birçok, birkaç, biraz** | bir çok, bir kaç, bir az | Belirsizlik sıfat ve zamirleri geleneksel olarak bitişik yazılır. |
| **pek çok, pek az** | pekçok, pekaz | `pek` zarfıyla kurulan öbekler her zaman ayrı yazılır. |
| **hiçbir, herhangi bir** | hiç bir, her hangi bir, herhangibir | `hiçbir` ve `herhangi` bitişik, `herhangi bir`deki `bir` ayrı yazılır. |
| **bir şey, her şey, hiçbir şey** | birşey, herşey, hiçbirşey | `şey` sözcüğü her durumda ayrı yazılır. |
| **art arda, yan yana, baş başa, iç içe** | ard arda, artarda, yanyana, içiçe | İkilemeler ayrı yazılır. Kök `art`tır: Türkçede sözcük sonunda tonlu `d` bulunmaz, bu yüzden yalın biçim `art` olur. Ünlüyle başlayan ek alınca ünsüz yumuşar (`art` + `-a` → `arda`). |
| **yanı sıra, ardı sıra, peşi sıra** | yanısıra, ardısıra | `sıra` ile kurulan sözler her zaman ayrı yazılır. |
| **ön söz, ön yargı, öngörü, önsezi** | önsöz, önyargı, ön görü | TDK'ya göre `ön söz` ve `ön yargı` ayrı, `öngörmek / öngörü` ve `önsezi` bitişik yazılır. |
| **iş birliği, güç birliği, dil birliği** | işbirliği, güçbirliği | `birlik` kelimesiyle kurulan tamlamalar ayrı yazılır. |
| **veri tabanı, ağ geçidi, iş akışı** | işakışı | TDK Güncel Türkçe Sözlük'te `veri tabanı` ayrı yazılır. Resmî/akademik metinlerde TDK yazımı (`veri tabanı`, `iş akışı`) korunur. |
| **fark etmek, ayırt etmek, terk etmek** | farketmek, ayırtetmek, terketmek | Ses düşmesi veya türemesi olmayan yardımcı fiiller ayrı yazılır. |
| **kaydetmek, sabretmek, keşfetmek, reddetmek** | kayıt etmek, keşif etmek, red etmek | Ünlü düşmesi veya ünsüz türemesi olan yardımcı fiiller bitişik yazılır. |
| **hâlbuki, oysaki, çünkü, mademki, belki, sanki, meğerki** | halbu ki, oysa ki, madem ki | TDK: *"Bağlaç olan ki ayrı yazılır"*, ancak *"Birkaç örnekte ki bağlacı kalıplaşmış olduğu için bitişik yazılır: belki, çünkü, hâlbuki, mademki, meğerki, oysaki, sanki."* (`SOMBAHÇEM` kodlaması). Diğer bağlaç `ki`'ler ayrı yazılır (`demek ki`, `kaldı ki`, `öyle ki`, `iyi ki`). |
| **ya da** | yada | Her zaman ayrı yazılır. |
| **hem ... hem (de)** | hem X, hem de Y | Tekrarlı bağlaçların (`hem... hem`, `ne... ne`, `ya... ya`, `gerek... gerek`) arasına virgül konmaz. |
| **zarf-fiil ekinden sonra virgül konmaz** | Veriyi çekip, işledik. / Sistemi kurarak, hızlandırdık. | TDK kuralına göre `-Ip, -ArAk, -IncA, -mAdAn, -dIkçA` gibi zarf-fiil eklerinden sonra (art arda sıralanan zarf-fiiller hariç) virgül konmaz. |
