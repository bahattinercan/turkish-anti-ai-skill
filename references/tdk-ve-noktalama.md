# TDK Yazım Kılavuzu, Noktalama ve Yüzey Kuralları Referansı

Bu referans dosyası, Büyük Dil Modellerinin (LLM) Türkçe metin üretirken yaptığı imla, noktalama ve fonetik ek hatalarını Türk Dil Kurumu (TDK) Yazım Kılavuzu ve doğal Türkçe tipografi standartlarına göre düzeltmek için kullanılır.

## 1. Beş Mutlak Noktalama Yasağı (İngilizce Tipografi Kopyaları)

LLM'ler İngilizce eğitim korpusundaki noktalama alışkanlıklarını Türkçe metinlere doğrudan taşır. Aşağıdaki 5 kullanım her register'da yasaktır:

| Kural | Makine Türkçesi (Yanlış / Yapay) | İnsan Türkçesi (Doğru / TDK Uyumlu) | Gerekçe ve TDK Karşılığı |
| :--- | :--- | :--- | :--- |
| **1. Uzun Çizgi (Em-dash) Yasağı** | Kurulum sihirbazı projelerinizi aktarır `[uzun çizgi]` böylece ilk günden başlarsınız. | Kurulum sihirbazı projelerinizi aktarır, böylece ilk günden başlarsınız. | TDK'da uzun çizgi yalnızca satır başında konuşma (diyalog) çizgisidir. Ara sözlerde virgül veya kısa çizgi kullanılır. |
| **2. Orta Çizgi (En-dash) Yasağı** | Toplantı 14.00 ile 15.30 arasında, 2024 ile 2026 yıllarında yapıldı (orta çizgi ile). | Toplantı 14.00-15.30 arasında, 2024-2026 dönemini kapsıyor. | Türkçede en-dash yoktur. TDK sayı, saat ve tarih aralıklarında boşluksuz **kısa çizgi (`-`)** kullanır. |
| **3. `ama / fakat` Öncesi Virgül** | Sistem hızlı çalışıyor, ama bellek tüketimi yüksek. | Sistem hızlı çalışıyor ama bellek tüketimi yüksek. | İngilizce `..., but` kuralının kopyasıdır. TDK kuralına göre Türkçede bağlaçlardan (`ama, fakat, lakin, ve, veya, ya da`) önce de sonra da virgül konmaz. |
| **4. Zorlama Noktalı Virgül Köprüsü** | Model veriyi analiz eder; bu süreç yaklaşık iki saniye sürer. | Model veriyi analiz eder. Bu süreç yaklaşık iki saniye sürer. | AI bağlaç seçmekten kaçınmak için iki cümleyi `;` ile yapıştırır. Doğal Türkçede cümle noktayla biter veya ulaçla bağlanır. |
| **5. İngilizce Title Case Başlıklar** | `## Yapay Zeka Ve Doğal Dil İşleme Sistemlerinde Yeni Yaklaşımlar` | `## Yapay zeka ve doğal dil işleme sistemlerinde yeni yaklaşımlar` | Türkçede ara başlıklarda tümce düzeni (yalnızca ilk harf büyük) tercih edilir. Her kelimenin ilk harfi büyük yazılırsa bile TDK kuralına göre `ve, ile, ya da, ki, de` bağlaçları her zaman küçük yazılır. |

## 2. Saat, Sayı ve Yüzde Yazımı (TDK Standartları)

- **Saat ve Dakika Ayracı:** TDK kuralına göre saat ve dakikalar iki nokta (`14:30`) ile değil, **tek nokta (`14.30`)** ile ayrılır. Ek gelirken dakika kısmı sıfırsa saat okunur (`14.00'te`), dakika varsa dakika okunur (`14.30'da`). Saat `00` olanlarda `13.00'da` (on üç sıfır sıfırda) değil, **`13.00'te` (on üçte)** yazılır.
- **Ondalık Ayraç ve Binlik Basamaklar:** İngilizce sayılardaki ondalık nokta (`3.14` veya `%42.5`) Türkçede **virgül (`3,14` veya `%42,5`)** olarak yazılır. Binlik basamaklar ise nokta ile ayrılır (`10.000`, `1.250.000`).
- **Yüzde İşareti:** Türkçede yüzde işareti sayıdan önce ve boşluksuz yazılır (`%25`).

## 3. Yabancı Teknik Terimler ve Türkçe Fonetiğe (Okunuşa) Göre Ek Uyumu

Teknik metinlerde yapılan en belirgin iki AI hatası şunlardır: (1) mühendislerin Türkçede hiç kullanmadığı zorlama çeviriler üretmek ve (2) İngilizce kalan terimlere yazılışına göre ek getirmektir.

### A. Zorla Çevrilmeyecek ve Çevrilecek Terimler

| Kategori | Terim Örnekleri | Doğru Uygulama |
| :--- | :--- | :--- |
| **Zorla Çevrilmeyecekler (Olduğu Gibi Bırak)** | `endpoint`, `deploy`, `middleware`, `queue`, `webhook`, `idempotent`, `payload`, `migration`, `script`, `commit`, `merge`, `rebase`, `token`, `prompt`, `fine-tuning`, `RAG`, `pipeline` | Asla *"uç nokta"*, *"göç betiği"*, *"olay güdümlü"*, *"ara katman"*, *"yük"*, *"çekme isteği"* diye çevirme, terimi olduğu gibi koru. |
| **Yerleşik Türkçesi Olanlar (Türkçesini Kullan)** | `developer` -> geliştirici, `user` -> kullanıcı, `database` -> veritabanı, `validation` -> doğrulama, `production` -> canlı ortam, `search` -> arama, `folder` -> klasör | Sektörde doğal olarak kullanılan Türkçe karşılığını tercih et. |
| **Her İkisi de Doğal Olanlar (Tutarlılık Kuralı)** | `cache / önbellek`, `server / sunucu`, `request / istek`, `response / yanıt`, `interface / arayüz`, `file / dosya` | Metnin başında birini seç ve metin bitene kadar aynı tercihi koru (bir cümlede `server`, sonrakinde `sunucu` yazma). |

### B. Türkçe Okunuşa Göre Kesme İşareti ve Ek Tablosu

TDK kuralına göre yabancı kelimelere ve kısaltmalara gelen ekler, kelimenin **Türkçe okunuşuna (son sesine)** ve ünlü/ünsüz uyumuna göre belirlenir:

| Yabancı Terim / Kısaltma | Türkçe Okunuşu | Yanlış (AI Yazılış Tahmini) | Doğru (Okunuşa Göre Çekim) |
| :--- | :--- | :--- | :--- |
| `cache` | keş (ince ünlü, sert ünsüz) | `cache'ı`, `cache'de`, `cache'dan` | `cache'i`, `cache'te`, `cache'ten` |
| `queue` | kü (ince-yuvarlak ünlü) | `queue'ya`, `queue'da` | `queue'yu`, `queue'da` |
| `SQL` | es-kü-el (ince ünlü) | `SQL'ı`, `SQL'da`, `SQL'dan` | `SQL'i`, `SQL'de`, `SQL'den` |
| `JSON` | ceyson (kalın ünlü) | `JSON'i`, `JSON'de` | `JSON'ı`, `JSON'da`, `JSON'dan` |
| `API` | ey-pi-ay veya a-pi | `API'de` | `API'yi` / `API'ı` (tamlamada `API ucu`) |
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
| **art arda, yan yana, baş başa, iç içe** | ard arda, artarda, yanyana, içiçe | İkilemeler her zaman ayrı yazılır (`art` kelimesi ünlüyle başlamadığı için `ard` olmaz). |
| **yanı sıra, ardı sıra, peşi sıra** | yanısıra, ardısıra | `sıra` ile kurulan sözler her zaman ayrı yazılır. |
| **ön söz, ön yargı, öngörü, önsezi** | önsöz, önyargı, ön görü | TDK'ya göre `ön söz` ve `ön yargı` ayrı, `öngörmek / öngörü` ve `önsezi` bitişik yazılır. |
| **iş birliği, güç birliği, dil birliği** | işbirliği, güçbirliği | `birlik` kelimesiyle kurulan tamlamalar ayrı yazılır. |
| **veri tabanı, ağ geçidi, iş akışı** | işakışı | Resmi/akademik metinlerde TDK standardı (`veri tabanı`, `iş akışı`) korunur. |
| **fark etmek, ayırt etmek, terk etmek** | farketmek, ayırtetmek, terketmek | Ses düşmesi veya türemesi olmayan yardımcı fiiller ayrı yazılır. |
| **kaydetmek, sabretmek, keşfetmek, reddetmek** | kayıt etmek, keşif etmek, red etmek | Ünlü düşmesi veya ünsüz türemesi olan yardımcı fiiller bitişik yazılır. |
| **halbuki, oysaki, çünkü, mademki, belki, sanki, meğerki** | halbu ki, oysa ki, madem ki | `SOMBAHÇEM` kodlamasındaki kalıplaşmış bağlaçlar bitişik, diğer tüm bağlaç `ki`'ler ayrı yazılır (`demek ki`, `kaldı ki`, `öyle ki`, `iyi ki`). |
| **ya da** | yada | Her zaman ayrı yazılır. |
| **hem ... hem (de)** | hem X, hem de Y | Tekrarlı bağlaçların (`hem... hem`, `ne... ne`, `ya... ya`, `gerek... gerek`) arasına virgül konmaz. |
| **zarf-fiil ekinden sonra virgül konmaz** | Veriyi çekip, işledik. / Sistemi kurarak, hızlandırdık. | TDK kuralına göre `-Ip, -ArAk, -IncA, -mAdAn, -dIkçA` gibi zarf-fiil eklerinden sonra (art arda sıralanan zarf-fiiller hariç) virgül konmaz. |
