# Türkçe Cümle Mimarisi (Sentaks) ve Morfoloji Kılavuzu

İngilizce eğitimli dil modellerinin Türkçe çıktılarındaki temel sorun kelime dağarcığı değil, **cümle iskeletinin İngilizce (Sağa Dallanan SVO) kalmasıdır**. Bu kılavuz, çeviri kokan mekanik cümleleri Türkçenin doğal morfolojik ve sözdizimsel yapısına dönüştüren 9 temel kuralı içerir.

## 1. Dallanma Yönü: Sağa Dallanmadan Sola Dallanmaya (Left-Branching)

İngilizce niteleyicileri ve yan cümleleri baş ismin (head noun) sağına dizer (`We built a system that scans and reports data every night`). LLM bu iskeleti Türkçeye iki yapay yolla kopyalar: ya cümleyi bölüp zamirle tekrarlar ya da Hint-Avrupa tipi `ki` bağlacı kullanır. Türkçe ise **sola dallanır** ve tüm niteleyiciler sıfat-fiil (`-An`, `-DIk`, `-AcAk`) alarak baş ismin önüne yerleşir.

| Kusur Türü | Makine Türkçesi (Sağa Dallanan / Calque) | İnsan Türkçesi (Sola Dallanan Doğal Yapı) |
| :--- | :--- | :--- |
| **Kuyruk Yan Cümle** | Bir sistem kurduk, bu sistem her gece verileri tarayıp raporluyor. | Her gece verileri tarayıp raporlayan bir sistem kurduk. |
| **Hint-Avrupa `ki` Bağlacı** | Öyle bir mimari tasarladık ki yüksek trafik altında bile gecikme yaşatmıyor. | Yüksek trafik altında bile gecikme yaşatmayan bir mimari tasarladık. |
| **Soru Zamirli Yan Cümle (Relativization)** | Kim açtı, kim düzenledi gör. / Nereye gideceklerini bilmiyorlar. | Kimin açtığını, kimin düzenlediğini gör. |

## 2. Bağlaç (`ve`) Yerine Ulaç (Zarf-Fiil) Sistemi

İngilizce sıralı eylemleri ve nedensellik bağlarını `and`, `and then`, `when`, `as` gibi ayrı kelimelerle bağlar. Türkçe ise zengin **ulaç (converb / zarf-fiil)** ekleriyle (`-Ip`, `-IncA`, `-dIkçA`, `-ArAk`, `-mAdAn`, `-ken`) iki yüklemi tek bir akışta kaynaştırır.

| İlişki Türü | Makine Türkçesi (Mekanik Bağlaçlı) | İnsan Türkçesi (Ulaçlı Doğal Akış) | Kullanılan Ulaç Eki |
| :--- | :--- | :--- | :--- |
| **Ardışık Eylem** | Veriyi çektik ve sonra temizledik. | Veriyi çekip temizledik. | `-Ip` |
| **Zaman / Tetikleme** | Cache doldu ve istekler yavaşlamaya başladı. | Cache dolunca istekler yavaşlamaya başladı. | `-IncA` |
| **Orantı / Süreç** | Trafik arttı ve buna bağlı olarak hata oranı da yükseldi. | Trafik arttıkça hata oranı da yükseldi. | `-dIkçA` |
| **Yöntem / Araç** | Maliyetleri düşürdük ve bu sayede karlılığı artırdık. | Maliyetleri düşürerek karlılığı artırdık. | `-ArAk` |
| **Zıtlık / Eşzamanlılık** | Birinci grup hızlı ilerler ve ikinci grup daha yavaş kalır. | Birinci grup hızlı ilerlerken ikincisi daha yavaş kalıyor. | `-ken` |

- **Sınır Kuralı (Sadakat Uyarıcısı):** Ulaç eklemek iki olay arasında zamansal veya nedensel bir bağ kurar. Kaynak metinde iki cümle arasında böyle bir bağ yoksa ve yalnızca yan yana duruyorlarsa, zorla ulaç ekleyip yeni bir nedensellik uydurma, virgülle veya ayrı cümle olarak bırak.

## 3. Koşulaç (Copula) Şişmesi: `-DIr` ve `-mAktAdIr` Salgını

İngilizcede geniş zamanlı her isim cümlesinde `is / are` zorunludur (`This method is effective`). LLM'ler bu `is/are` yapısını Türkçeye refleks olarak **`-DIr`** ve şimdiki/geniş zamanı **`-mAktAdIr`** olarak çevirir. Oysa doğal Türkçede geniş zaman isim cümlesinde koşulaç sıfırdır (ek almaz). `-DIr` yalnızca resmi/akademik kesinlik veya olasılık (`Eve varmıştır`) bildirir.

- **Akademik / Hukuki Register Dışında `-DIr` ve `-mAktAdIr` Temizliği:**
  - **Makine:** *"Bu yöntem oldukça etkilidir ve geliştiricilere büyük kolaylık sağlamaktadır. Burası sistemin en kritik parçasıdır."*
  - **İnsan (Teknik):** *"Bu yöntem oldukça etkili, geliştiricilerin işini de kolaylaştırıyor. Burası sistemin en kritik parçası."*
  - **İnsan (Akademik - Kalibre Edilmiş Doz):** 2015-2019 arası insan yazımı hakemli Türkçe makalelerde `-mAktAdIr` yoğunluğu 100 kelimede `0,4 - 2,3`, `-DIr` yoğunluğu ise `2,3 - 4,0` aralığındadır. Akademik metinlerde bile her cümleyi `-mektedir` ile bitirme, geniş zaman (`-Ir/-Ar`) ile nöbetleşe kullan.

## 4. Vurgu Yuvası (Pre-Verbal Focus) ve Devrik Cümle Ritmi

İngilizce sabit SVO diziliminde vurguyu vermek için cümleyi yarıp `It is X that...` (*cleft sentence*) kurar veya kelimeleri **kalın (bold)** yazar. LLM'ler bunu Türkçeye *"İşte tam da bu noktada..."*, *"Asıl önemli olan şey şudur ki..."* gibi dolgu kalıplarıyla taşır.

Türkçede ise sözcük dizimi esnektir ve **vurgu yuvası yüklemin hemen önündeki konumdur**:

- **Nötr (Zaman/Yer odaklı):** *"Ben dün raporu **Ahmet'e** gönderdim."* (Kime gönderildiği vurgulanıyor)
- **Özne Vurgusu:** *"Dün raporu Ahmet'e **ben** gönderdim."* (Gönderenin kim olduğu vurgulanıyor)
- **Zaman Vurgusu:** *"Ben raporu Ahmet'e **dün** gönderdim."* (Ne zaman gönderildiği vurgulanıyor)
- **Nesne Vurgusu:** *"Ben dün Ahmet'e **raporu** gönderdim."* (Neyin gönderildiği vurgulanıyor)

### Devrik Cümle Kullanımı ve Sınırı
Günlük, edebi ve blog/deneme Türkçesinde yüklemin cümle sonundan öne çekilmesi (devrik cümle) metne nefes ve konuşma sıcaklığı katar:

- **Makine:** *"Kimse bu uzun hata raporlarını sonuna kadar okumuyor."*
- **İnsan (Blog/Deneme):** *"Kimse sonuna kadar okumuyor bu uzun hata raporlarını."*
- **Kota Yasağı:** Teknik, kurumsal ve akademik register'larda devrik cümle kullanma. Blog/deneme register'ında ise 400 kelimelik bir metinde en fazla 2-3 doğal devrik cümle kullan. Her cümleyi devrik yapmak yeni bir yapay tike dönüşür.

## 5. Zamir Düşürme (Pro-Drop) ve Gereksiz `"Bir"` / `"Kendi"` Temizliği

### A. Kişi ve İşaret Zamiri Düşürme
Türkçe yüklemdeki şahıs ekleriyle (`-Im, -sIn, -Iz, -lAr`) ve isimdeki iyelik ekleriyle özneyi zaten kodlar. İngilizcedeki zorunlu `I, we, they, it, this` zamirlerini her cümlede Türkçeye taşımak metni ağırlaştırır:

- **Makine:** *"Biz önce veritabanını yedekledik, sonra biz migration script'ini çalıştırdık. O sorunsuz tamamlandı."*
- **İnsan:** *"Önce veritabanını yedekledik, ardından migration script'ini çalıştırdık. İşlem sorunsuz tamamlandı."*

### B. İngilizce `a / an` Çevirisi Olan Gereksiz `"Bir"` Sıfatı
Çeviri kokan Türkçenin bir numaralı imzası, her sıfat-isim tamlamasının ortasına İngilizce `a/an` karşılığı olarak `"bir"` sıkıştırmaktır:

- **Makine:** *"Bu güncelleme **büyük bir önem** taşıyor ve **yüksek bir performans** ile **iyi bir kullanıcı deneyimi** sunuyor."*
- **İnsan:** *"Bu güncelleme **büyük önem** taşıyor, **yüksek performans** ve **iyi kullanıcı deneyimi** sunuyor."*
- **Kural:** `"Bir"` sözcüğü sayıca teklik vurgulanmıyorsa soyut kavramların (`büyük önem`, `ciddi artış`, `geniş kapsam`, `derin etki`, `yüksek hız`) önünden silinir.

### C. İngilizce `his/her/its own` Çevirisi Olan Gereksiz `"Kendi"` ve İyelik Zamirleri

- **Makine:** *"Her servis **kendi veritabanına** bağlanır ve **onun kendi** yapılandırmasını okur."*
- **İnsan:** *"Her servis kendi veritabanına bağlanıp yapılandırmasını okur."* (İyelik eki `-sI` zaten aitliği verir, zıtlık yoksa `kendi` tekrarlanmaz).

## 6. Edilgen Çatı (`tarafından`) ve Kof Yardımcı Fiil Temizliği

### A. Edilgen Çatı ve `"tarafından"` Kirliliği
İngilizce akademik ve kurumsal metinlerdeki `was developed by X` yapısı Türkçeye `X tarafından geliştirilmiştir` olarak kopyalanır. Türkçede eylemi yapan belliyse cümle **etken (active)** kurulur:

- **Makine:** *"Yeni kimlik doğrulama modülü güvenlik ekibimiz tarafından test edilmiş ve onaylanmıştır."*
- **İnsan:** *"Güvenlik ekibimiz yeni kimlik doğrulama modülünü test edip onayladı."*

### B. Kof Yardımcı Fiiller (Light Verb Inflation)
LLM'ler tek bir Türkçe fiille anlatılabilecek eylemleri isim + yardımcı fiil (`gerçekleştirmek, sağlamak, bulunmak, olmak, yapmak, sahip olmak`) öbekleriyle şişirir:

| Şişirilmiş Yapay Öbek (Kof Fiil) | Doğal ve Güçlü Türkçe Fiil | Örnek Dönüşüm |
| :--- | :--- | :--- |
| **gerçekleştirmek / icra etmek** | yapmak, düzenlemek, kurmak, tamamlamak | *"Toplantı gerçekleştirdik"* -> *"Toplantı yaptık"* / *"Analiz gerçekleştirdi"* -> *"Analiz etti"* |
| **sağlamak** (aşırı kullanım) | sunmak, vermek, kazandırmak, doğrudan ettirgen çatı (`-DIr`, `-t`) | *"Hız artışı sağlar"* -> *"Sistemi hızlandırır"* / *"Destek sağlar"* -> *"Destek verir"* |
| **katkıda bulunmak / yardımcı olmak** | katkı sunmak, desteklemek, yararı dokunmak | *"Büyümesine katkıda bulunur"* -> *"Büyümesini destekler"* |
| **sahip olmak** (`have / has` çevirisi) | `-lI` eki, `var`, `barındırmak`, `içermek`, `taşımak` | *"Yüksek hıza sahiptir"* -> *"Çok hızlıdır"* / *"Üç katmana sahiptir"* -> *"Üç katmandan oluşur"* |
| **ev sahipliği yapmak** (`host / feature`) | barındırmak, ağırlamak, yer almak | *"Bölge birçok tarihi yapıya ev sahipliği yapmaktadır"* -> *"Bölgede pek çok tarihi yapı var"* |
| **rol oynamak** (`play a role`) | belirlemek, etkilemek, işe yaramak | *"Kritik bir rol oynamaktadır"* -> *"Belirler / belkemiğini oluşturur"* |
| **olarak** (aşırı edat kullanımı) | `-cA`, hâl ekleri veya doğrudan yüklem | *"İlk adım olarak veriyi sildik"* -> *"İlk adımda veriyi sildik"* / *"Sonuç olarak"* -> *"Sonuçta"* |

## 7. Kanıtsallık Kipi (`-mIş`) ve Geniş Zaman / Şimdiki Zaman Ayrımı

- **Delil Kipi (`-mIş` vs. `-DI`):** İngilizce görgü tanıklığını fiil çekiminde ayırmaz (`The server crashed at 3 AM`). Türkçede olayı bizzat görmediysen, log'dan okuduysan veya sonradan fark ettiysen `-mIş` kullanılır:
  - **Makine:** *"Gece yarısı bellek sızıntısı oldu ve servis kapandı. Sabah log'lara baktığımızda fark ettik."*
  - **İnsan:** *"Gece yarısı bellek sızıntısı olmuş, servis de kapanmış. Sabah log'lara bakınca fark ettik."*
- **Geniş Zaman (`-Ir/-Ar`) vs. Şimdiki Zaman (`-yor`):** Bir sistemin genel kuralını veya değişmez çalışma prensibini anlatırken `-yor` ile `-Ir/-Ar` kiplerini karıştırma:
  - **Makine:** *"Redis veriyi bellekte tutuyor ve diske asenkron yazıyor."*
  - **İnsan (Teknik Tanım):** *"Redis veriyi bellekte tutar, diske ise asenkron yazar."*

## 8. Ad Tamlaması Zincirlerini Kırma (Maksimum 3 İsim Kuralı)

İngilizce teknik ve kurumsal tamlamaları (`customer segmentation module performance optimization process`) Türkçeye eklerle üst üste yığmak okunabilirliği yok eder. Bir tamlamada en fazla 3 isim yan yana gelebilir, fazlasını sıfat-fiil veya hâl ekleriyle çöz:

- **Makine:** *"Müşteri segmentasyon modülü performans iyileştirme çalışması sonuç raporu"*
- **İnsan:** *"Müşteri segmentasyon modülünde yaptığımız performans çalışmasının sonuçları"*

## 9. Öz-Düzeltme (Self-Correction) ve Söylem Parçacıkları

Makine Türkçesi her şeyi baştan mutlak bir kesinlikle biliyormuş gibi yazar. İnsan yazar ise düşünürken cümleyi daraltır, çekince koyar ve Türkçenin doğal söylem parçacıklarını (`işte`, `ise`, `zaten`, `hani`, `yani`, `bir de`, `tabii`, `daha doğrusu`) yerli yerinde kullanır:

- **Makine:** *"Silme işlemi idempotenttir, bu nedenle dağıtık sistemlerde tercih edilir."*
- **İnsan:** *"Silme işlemi idempotent olduğu için tercih ediliyor. Güncellemek de çalışır tabii ama bir şey ters gittiğinde sessizce bozulur."*
- **Makine:** *"Birinci yöntem hızlıdır, ikinci yöntem yavaştır."*
- **İnsan:** *"Birinci yöntem hızlı, ikincisi ise yavaş."*
