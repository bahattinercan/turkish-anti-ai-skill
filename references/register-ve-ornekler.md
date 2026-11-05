# Register (Bağlam) Profilleri ve Uçtan Uca Dönüşüm Örnekleri

Doğal Türkçe tek bir kalıptan oluşmaz. Bir sözleşmedeki devrik cümle özensizlik, bir blog yazısındaki `-mAktAdIr` eki ise robotluk üretir. Bu dosya, metin türlerine göre 9 üslup boyutunun nasıl kalibre edileceğini ve uçtan uca (Before / After) dönüşüm örneklerini içerir.

## 1. Dokuz Boyutlu Register ve Üslup Matrisi

Kullanıcı özel bir yazar örneği (few-shot) vermediğinde aşağıdaki 5 profilden uygun olanı seç:

| Boyut | 1. Blog / Deneme / Sosyal Medya | 2. Teknik / Mühendislik | 3. Kurumsal / SaaS / İş İletişimi | 4. Akademik / Resmi / Hukuki | 5. Edebi / Anlatı |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Anlatıcı Kimliği** | Masanın karşısından anlatan deneyimli dost | Gece 2'de o hatayı çözmüş kıdemli mühendis | Müşteriye bizzat yazan net ve dürüst kurucu | Konuya hakim, soğukkanlı araştırmacı/uzman | Düşüncesini yazarken inşa eden usta yazar |
| **Hitap** | Sen veya Siz (tutarlı) | Sen veya nötr 2. çoğul | Siz | 3. şahıs / nötr | Bağlama göre 1. veya 3. şahıs |
| **Cümle Uzunluğu & Burstiness** | Yüksek dalgalanma (4 kelime ile 28 kelime bir arada) | Orta-Yüksek (Kısa net yargılar + ulaçlı açıklamalar) | Orta (10-20 kelime, net ve taranabilir) | Orta-Uzun (15-30 kelime, sola dallanan yan cümleler) | Çok yüksek dalgalanma (nefes ritmine odaklı) |
| **Cümlecik Bağlama** | Ulaçlar (`-Ip, -IncA`) + nokta/virgül | Ulaçlar (`-Ip, -dIkçA, -ArAk`) + iki nokta | Ulaçlar + net sebep-sonuç bağlaçları | Sıfat-fiiller (`-An, -DIk`) + ulaçlar | Ulaçlar + ritmik tekrarlar ve virgül |
| **Kip Dağılımı** | `-yor`, `-DI`, `-mIş` (delil), geniş zaman | Geniş zaman (`-Ir/-Ar` kurallar için), `-DI`, `-mIş` | Geniş zaman, `-yor`, `-DI` | Geniş zaman, `-mAktAdIr` (100 kelimede 0.4-2.3), `-DIr` | Tüm kipler serbest |
| **Söylem Parçacıkları** | `işte, zaten, ise, hani, tabii, daha doğrusu` | `ise, aslında, daha doğrusu, örneğin` | `ise, özellikle, doğrudan` | Yalnızca `ise, nitekim, dolayısıyla` | Doğal akışa göre serbest |
| **Devrik Cümle Oranı** | 400 kelimede 2-3 adet | Sıfır (0) | Sıfır (0) | Sıfır (0) | Anlatı ritmine göre doğal |
| **Terim Tercihi** | Günlük karşılıklar veya okunuşa göre çekimli terim | Yerleşik İngilizce terim olduğu gibi (`endpoint'e`) | Sektör standardı, jargonsuz sade Türkçe | TDK ve alan terimleri (`veri tabanı, alanyazın`) | Türkçe duygu ve imge değeri yüksek sözcükler |
| **Açılış Hamlesi** | Sahne, somut gözlem veya doğrudan soru | Doğrudan problem veya mimari karar | Temel değer önermesi veya ana mesaj | Araştırma problemi veya olgusal çerçeve | Atmosfer, detay veya iç ses |

## 2. Aynı İddianın 4 Farklı Register'daki Doğal Yazımı

- **Ham AI Çıktısı (Makine Türkçesi):**
  > *"Cache stratejisinin doğru bir şekilde belirlenmesi, sistem performansı açısından kritik bir öneme sahiptir ve gecikme sürelerinin azaltılmasında yadsınamaz bir rol oynamaktadır."*
- **Akademik / Resmi Register:**
  > *"Önbellekleme stratejisinin doğru kurgulanması, sistem performansını ve yanıt sürelerini doğrudan belirlemektedir."*
- **Teknik / Mühendislik Register:**
  > *"Cache stratejisini doğru kurgulamak performansı doğrudan belirler ve gecikmeyi düşürür."*
- **Kurumsal / Ürün Register:**
  > *"Doğru önbellek kurgusu, sisteminizi hızlandırırken yanıt sürelerini kısaltır."*
- **Blog / Deneme Register:**
  > *"Performansı belirleyen asıl şey cache stratejisi işte; doğru kurduğunuzda gecikme yarı yarıya düşüyor."*

## 3. Uçtan Uca (Before / After) Dönüşüm Örnekleri

### Örnek 1: Kurumsal / LinkedIn / Blog Yazısı

**Önce (Tipik AI Türkçesi):**
> Günümüzün hızla değişen iş dünyasında, uzaktan çalışma modeli sadece geçici bir trend değil, aynı zamanda kurumsal kültürün temel bir yapı taşı haline gelmiştir ve bu durumun önemi yadsınamaz. Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki, çalışanlara esneklik sağlamak verimlilik üzerinde kritik bir rol oynamaktadır. Bununla birlikte, iletişim kopukluklarını önlemek adına bütüncül bir yaklaşım benimsenmelidir. Sonuç olarak, geleceğin çalışma dünyasında başarılı olmak isteyen kurumlar bu dönüşüme ayak uydurmak zorundadır.

**Yakalanan AI Sinyalleri:**
1. *"Günümüzün hızla değişen iş dünyasında"* (Sahneleme / Boş giriş - P0)
2. *"sadece X değil, aynı zamanda Y"* (Negatif paralellik - P0)
3. *"önemi yadsınamaz"* (Tier-1 klişe - P0)
4. *"Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki"* (Edilgen çatı + kof fiil + belirsiz otorite + Hint-Avrupa `ki` - P1)
5. *"esneklik sağlamak ... kritik bir rol oynamaktadır"* (Kof fiil + Tier-1 klişe + `-mAktAdIr` şişmesi - P1)
6. *"Bununla birlikte ... bütüncül bir yaklaşım"* (Mekanik bağlaç + kurumsal jargon - P2)
7. *"Sonuç olarak ... ayak uydurmak zorundadır"* (Vaaz veren özet kapanış - P0)

**Sonra (Doğal İnsan Türkçesi - Blog/Deneme Register):**
> Uzaktan çalışma artık geçici bir heves olmaktan çıkıp şirket kültürünün kalıcı bir parçasına dönüştü. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik doğrudan artıyor. İşin zor kısmı, ekip aynı ofiste değilken iletişimi koparmamak. Bunu da tek tek araçlarla değil, çalışma düzenini baştan sona buna göre kurgulayarak çözebiliyorsunuz.

### Örnek 2: Teknik / Yazılım Mühendisliği Dokümanı

**Önce (Tipik AI Türkçesi):**
> ## Cache Stampede Problemi Ve Çözüm Yöntemleri
> Bir önbellek (cache) anahtarının süresi dolduğunda, aynı anda gelen birçok istek veritabanına yönlendirilir ve bu durum sistemde adeta bir darboğaz yaratmaktadır. Bu sorun özellikle yüksek bir trafiğe sahip olan uç noktalarda (endpoints) kritik bir öneme sahiptir. Bu problemi çözmek için dağıtık kilit (distributed lock) mekanizması kullanılabilir, ama bu yöntem gecikme süresini artırabilir.

**Yakalanan AI Sinyalleri:**
1. Başlıkta `Ve` bağlacının büyük yazılması ve klasik *"X Nedir ve Çözüm Yöntemleri"* şablonu (P2)
2. *"yönlendirilir ve bu durum ... yaratmaktadır"* (Ulaç yerine `ve bu durum` + `-mAktAdIr` - P1)
3. *"adeta bir darboğaz"*, *"yüksek bir trafiğe sahip olan"*, *"uç noktalarda"*, *"kritik bir öneme sahiptir"* (Tier-1 klişeler + gereksiz `"bir"` + zorlama teknik çeviri `"uç nokta"` - P0/P1)
4. `..., ama` (Karşıtlık bağlacı öncesi virgül - P2)

**Sonra (Doğal İnsan Türkçesi - Teknik Register):**
> ## Popüler bir cache key'in süresi dolduğunda ne olur?
> Çok okunan bir `cache` anahtarının süresi dolduğu anda gelen yüzlerce istek aynı anda veritabanına yüklenir ve sistemi kilitler. Özellikle yüksek trafikli `endpoint`'lerde bu durum doğrudan kesintiye yol açar. Dağıtık kilit (`distributed lock`) kullanarak veritabanına yalnızca tek bir isteğin gitmesini sağlayabilirsiniz ama bu yöntem diğer isteklerin bekleme süresini uzatır.

### Örnek 3: Akademik / Analitik Metin (Olgusal Sadakat ve Dozaj Korunarak)

**Önce (Tipik AI Türkçesi):**
> Türkiye'de 2020-2024 yılları arasında yenilenebilir enerji yatırımları sadece artış göstermekle kalmamış, aynı zamanda enerji arz güvenliğinde de çığır açan bir dönüm noktası olmuştur. Enerji Bakanlığı tarafından paylaşılan verilere göre, güneş enerjisi kurulu gücü %112 oranında bir büyüme gerçekleştirmiştir ki bu durum sektörün dinamik yapısının en büyük kanıtıdır.

**Sonra (Doğal İnsan Türkçesi - Akademik Register):**
> Türkiye'de 2020-2024 döneminde hız kazanan yenilenebilir enerji yatırımları, enerji arz güvenliğinin yapısını da dönüştürmüştür. Enerji Bakanlığının verilerine göre güneş enerjisi kurulu gücü bu dönemde %112 büyümüştür.
