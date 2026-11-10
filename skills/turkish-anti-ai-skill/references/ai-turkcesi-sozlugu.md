# "Yapay Zekâ Türkçesi" (AI Slop & Translationese) Sözlüğü

Büyük Dil Modelleri (LLM), İngilizce eğitim verisinde aşırı temsil edilen klişeleri (`delve into`, `tapestry`, `testament to`, `pivotal`, `not only... but also`) Türkçeye birebir kalıp çevirisi (calque) olarak taşır. Bu sözlük, Türkçe metinlerdeki yapay zekâ izlerini önem derecesine göre (Tier 1, Tier 2, Tier 3) sınıflandırır ve doğal Türkçe karşılıklarını sunar.

**Örnekleri okuma kuralı (Olgusal Sadakat Kilidi):** "Sonra" sütunundaki dönüşümler kaynakta olmayan hiçbir sayı, yer, kişi veya iddia eklemez. Bir klişe silinince yerine somut bilgi gerekiyorsa bu bilgi köşeli yer tutucuyla gösterilir (`[somut veri: ...]`). Onarım (`rewrite`) modunda yer tutucuyu kendin doldurma. Kaynakta karşılığı varsa onu kullan, yoksa yer tutucuyu bırakıp kullanıcıya sor ya da cümleyi sadeleştirmekle yetin.

## 1. Tier-1: Kesin AI İfşaları (Tek Görülmede Silinmesi veya Değiştirilmesi Gerekenler)

Bu kelime ve kalıplar, doğal Türkçe metinlere kıyasla LLM çıktılarında 10 ila 50 kat daha sık görülür. Metinde tek bir kez bile geçseler müdahale edilmelidir.

| İngilizce Kaynak Kalıp | Yapay Zekâ Türkçesi (Yasaklı / Klişe) | Doğal ve İnsani Türkçe Alternatifi | Örnek Dönüşüm (Önce -> Sonra) |
| :--- | :--- | :--- | :--- |
| *undeniable / undeniably* | **yadsınamaz / yadsınamaz bir gerçek ki / inkar edilemez** | açık, ortada, belli, tartışmasız (veya tamamen silip doğrudan olguyu yaz) | *"Yapay zekânın etkisi yadsınamaz."* -> *"Yapay zekânın etkisi ortada."* / Kaynakta somut etki varsa: *"Yapay zekâ [somut etki] sağladı."* |
| *virtually / almost like / veritable* | **âdeta** (yaygın yazımıyla `adeta`, her benzetmede kullanımı) | neredeyse, sanki, gibi (çoğu zaman tamamen silinmeli) | *"Sektörde âdeta bir devrim yarattı."* -> *"Sektörün kurallarını değiştirdi."* |
| *delve into / dive deep into* | **derinlemesine inmek / derinlemesine incelemek / mercek altına almak** | ayrıntısına bakmak, yakından incelemek, deşmek, ele almak | *"Konunun derinlemesine inelim."* -> *"Konunun ayrıntılarına bakalım."* |
| *tapestry / mosaic / kaleidoscope* | **zengin bir doku / mozaik / harman / yelpaze (geniş bir yelpazede)** | çeşitlilik, bir arada bulunmak, çok yönlü yapı, farklı alanlarda | *"Kültürel bir mozaik ve geniş bir yelpaze sunar."* -> *"Farklı kültürleri bir araya getirir."* |
| *stands as a testament to* | **...nın bir kanıtıdır / en büyük göstergesidir / nişanesidir** | ...-dığını gösterir, ortaya koyar | *"Bu başarı ekibin azminin bir kanıtıdır."* -> *"Bu sonuç ekibin ne kadar sıkı çalıştığını gösteriyor."* |
| *plays a pivotal / crucial role* | **kritik bir rol oynamaktadır / hayati öneme sahiptir / kilit rol üstlenir** | belirler, çok önemli, şart | *"Veri kalitesi model başarısında kritik bir rol oynamaktadır."* -> *"Modelin başarısı büyük ölçüde veri kalitesine bağlı."* |
| *in today's fast-paced / digital world* | **günümüzün hızla değişen dünyasında / dijitalleşen çağımızda** | **Tamamen sil.** (Konuya doğrudan gir) | *"Günümüzün hızla değişen dünyasında hız önemlidir."* -> *"Hız önemli."* / Nedeni kaynakta varsa: *"Hız önemli çünkü [kaynaktaki gerekçe]."* |
| *not only X, but also Y* | **sadece X değil, aynı zamanda Y / yalnızca X olmakla kalmayıp...** | hem X hem Y, X'in yanında Y de..., X yapıyor üstelik Y... | *"Sadece hızı artırmakla kalmaz, aynı zamanda maliyeti düşürür."* -> *"Hem hızı artırır hem de maliyeti düşürür."* |
| *it is not X, it is Y* (Negatif Paralellik) | **bu bir X değil, bir Y'dir / mesele X değil, Y** | Olumsuz yarıyı atıp yalnızca Y olduğunu söyle (kimsenin iddia etmediği X'i reddetme) | *"Bu sadece bir güncelleme değil, yeni bir başlangıçtır."* -> *"Bu sürüm yeni bir başlangıç."* / Neyin değiştiği kaynakta varsa: *"Bu sürümde [kaynaktaki değişiklik]."* |
| *unlock the potential / unleash* | **potansiyelini ortaya çıkarmak / tam potansiyeline ulaşmak / kilidini açmak** | verimli kullanmak, önünü açmak, kapasitesini artırmak | *"Ekibinizin potansiyelini ortaya çıkarın."* -> *"Ekibinizin elini güçlendirin / daha verimli çalışın."* |
| *watershed moment / turning point* | **dönüm noktası / kilometre taşı / çığır açan (groundbreaking)** | önemli eşik, yeni aşama, ilk kez ... sağlayan | *"Sektör için çığır açan bir dönüm noktasıdır."* -> *"Sektör için önemli bir eşik."* / Neyi ilk kez sağladığı kaynakta varsa: *"Sektörde ilk kez [kaynaktaki yenilik] sağlıyor."* |
| *seamlessly / effortless* | **kusursuz bir şekilde / pürüzsüzce / zahmetsizce** | kolayca, takılmadan, sorunsuz | *"Mevcut sisteminizle kusursuz bir şekilde entegre olur."* -> *"Mevcut sisteminize sorunsuz bağlanır."* |
| *meticulously / painstakingly* | **titizlikle / özenle hazırlanmış** | dikkatle, tek tek kontrol edilerek (veya kaynaktaki somut kanıtı ver) | *"Titizlikle eğitilmiş modelimiz..."* -> *"Modelimiz..."* (sıfatı sil) / Kaynakta varsa: *"[kaynaktaki veri miktarı] belgeyle eğitilen modelimiz..."* |
| *nestled in the heart of* | **...nın kalbinde yer alan** | ... merkezindeki, ...'da bulunan | *"İstanbul'un kalbinde yer alan ofisimiz..."* -> *"İstanbul'un merkezindeki ofisimiz..."* (semt adı kaynakta yoksa ekleme) |

## 2. Tier-2: Bürokratik Bağlaçlar, Geçiş Dolguları ve Şişirilmiş Sıfatlar (Yoğunlukta Temizlenenler)

Bu ifadeler tek başına yanlış değildir ancak LLM'ler her paragraf başında ve cümle geçişinde bunları mekanik olarak tekrarlar. Bir metinde birden fazla geçiyorsa silinmeli veya sadeleştirilmelidir.

| Kategori | Yapay Zekâ / Çeviri Kalıbı | Doğal Türkçe Alternatifi veya Eylem |
| :--- | :--- | :--- |
| **Geçiş Bağlaçları (*Moreover / Furthermore / However*)** | **Bununla birlikte / Öte yandan / Buna ek olarak / Dahası / Üstelik** (her paragraf başında) | Bağlacı silip cümleye gir. Gerekiyorsa `Ayrıca`, `Ama` veya cümle içi `ise / de` kullan. Bu bağlaçlar tek tek yanlış değildir, sorun her paragraf başında refleksle tekrar edilmeleridir. |
| **Sahte Vurgu Girişleri (*It is worth noting / Importantly*)** | **Belirtmek gerekir ki / Şunu vurgulamak önemlidir ki / Unutulmamalıdır ki / Dikkat çekici bir şekilde** | **Tamamen sil.** Vurgulanacak bilgiyi giriş anonsu yapmadan yaz. |
| **İşaret ve Gönderim Dolguları (*Said / Mentioned / In this context*)** | **Söz konusu / Bahsi geçen / Bu bağlamda / Bu doğrultuda / Bu çerçevede / Bu noktada** | İşaret sıfatı (`bu`, `o`) kullan veya ismi doğrudan tekrar et (*"Söz konusu algoritma"* -> *"Bu algoritma"*). |
| **Yüzeysel Sonuç Kuyrukları (*...highlighting / underscoring / fostering*)** | **...olduğunu gözler önüne sermektedir / ...önemini bir kez daha vurgulamaktadır / ...zemini hazırlamaktadır** | Cümle sonundaki bu yorum kuyruklarını kesip olguyu vererek noktayı koy. |
| **Şişirilmiş Kurumsal Jargon (*Holistic / Synergy / Paradigm / Ecosystem*)** | **Bütüncül (holistik) bir yaklaşım / Sinerji yaratmak / Paradigma değişimi / Ekosistem / Dinamik yapı / Proaktif** | Somut karşılık kullan: *"bütüncül yaklaşım"* -> *"tüm süreci kapsayan plan"*, *"ekosistem"* -> *"sektör / ortam / araç seti"*. |
| **Yüzeysel Özet Kapanışları (*In conclusion / To sum up / Overall*)** | **Sonuç olarak / Özetlemek gerekirse / Son tahlilde / Genel bir değerlendirme yapıldığında** | Okur son paragrafta olduğunu zaten görür. Bu başlangıç etiketini silip son sözü söyle. |
| **İhtiyat Yığılması (*Could potentially / Might possibly*)** | **Potansiyel olarak ...-ebilme ihtimali bulunmaktadır / ...söylenebilir ki** | Tek bir ihtiyat eki yeterlidir: *"...-ebilir"* veya *"görünüyor"*. |
| **Belirsiz Otorite Atfı (*Experts argue / Research shows*)** | **Uzmanlar belirtiyor ki / Yapılan araştırmalar göstermektedir ki / Pek çok gözlemciye göre** | Kaynak metinde gerçek bir isim veya araştırma varsa adını yaz, yoksa bu sahte otorite cümlesini sil. |

## 3. Tier-3: Ürün, SaaS, Pazarlama ve Lokalizasyon Klişeleri (Çeviri Kokan Kalıplar)

Web sitelerinde, uygulama arayüzlerinde (UI), kurumsal bültenlerde ve SaaS metinlerinde İngilizceden birebir çevrilen yapay kalıplar:

| İngilizce Kaynak | Çeviri Kokan / Yapay Türkçe | Doğal ve Yerleşik Türkçe |
| :--- | :--- | :--- |
| *Take X to the next level* | **X'i bir üst seviyeye taşıyın / bir sonraki aşamaya geçirin** | X'i geliştirin / hızlandırın / büyütün |
| *Ready to get started?* | **Başlamaya hazır mısınız?** | Hemen başlayın / Denemeye başlayın |
| *Empower your team to...* | **Ekibinizi ... yapmaları için güçlendirin** | Ekibinizin ... yapmasını kolaylaştırın / Ekibinizin elini güçlendirin |
| *Save time and money* | **Zamandan ve paradan tasarruf edin** | Zaman kazanın, maliyetleri düşürün |
| *Tailored to your needs* | **İhtiyaçlarınıza göre özel olarak tasarlanmış / terzi işi** | İhtiyacınıza uygun / İşinize göre uyarlanan |
| *Game-changer* | **Oyun değiştirici / Oyunun kurallarını değiştiren** | Dengeleri değiştiren / İşleri kökten kolaylaştıran |
| *One-stop shop / All-in-one hub* | **Tek durak noktası / Hepsi bir arada merkez** | Tüm araçlar tek ekranda / İhtiyacınız olan her şey tek yerde |
| *Leverage / Utilize* | **Kaldıraç olarak kullanmak / İstifade etmek** | Kullanmak, yararlanmak, değerlendirmek |
| *No credit card required* | **Kredi kartı istenmez / Kart istemiyoruz** | Kredi kartı gerekmez |
| *Send on WhatsApp / Share on X* | **WhatsApp'ta gönder / X üzerinde paylaş** | WhatsApp'tan gönder / X'te paylaş (Hâl eki uyumuna dikkat) |
| *See who opened and edited* | **Kim açtı, kim düzenledi gör** | Kimin açtığını, kimin düzenlediğini gör |
| *Update 2.4 / Version 2.0 / Patch 1.3* | **Güncelleme 2.4'ü / Sürüm 2.0 ile / Yama 1.3'te** | 2.4 Güncellemesini / 2.0 sürümüyle / 1.3 Yamasında (Sayı adın önüne geçer, ek adın sonuna gelir. Tarih bildiren *Son güncelleme 12.03.2025* doğaldır.) |
| *Happy Thursday! / Happy Monday everyone!* | **Mutlu perşembeler! / Herkese mutlu pazartesiler!** | İyi perşembeler! / Herkese merhaba! |
| *Let's dive in! / Here's the thing:* | **Hadi başlayalım! / Mesele şu ki: / İşin sırrı şurada:** | **Tamamen sil.** |

## 4. Sohbet ve Asistan Artıkları (Chat Residue - Anında Silinecekler)

Metin çıktılarının başında veya sonunda asla yer almaması gereken ifadeler:

- *"Elbette! İşte metninizin daha doğal ve insani Türkçeye uyarlanmış hâli:"*
- *"Harika bir konu! Gelin bu konuyu birlikte inceleyelim."*
- *"Umarım bu düzenleme işinize yarar! Başka bir değişiklik isterseniz lütfen belirtin."*
- *"Değişiklik Özeti: 1. Uzun çizgiler kaldırıldı..."* (Kullanıcı özellikle `audit` veya açıklama istemediyse ekleme).
