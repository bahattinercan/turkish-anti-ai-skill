---
name: turkish-anti-ai-skill
description: Türkçe metni insan eliyle yazılmış gibi doğal yazar veya onarır. Kullanıcı Türkçe bir metin için "insanileştir", "humanize et", "AI hissiyatını sil" veya "doğal Türkçeye çevir" dediğinde, metinde çeviri kokusu ya da TDK hatası denetimi istediğinde, Türkçe blog, makale, kurumsal yazı, sosyal medya içeriği veya teknik doküman yazarken kullan.
license: MIT
metadata:
  author: yucezerey
  version: "1.0.0"
---

# Turkish Anti-AI Skill (Doğal Türkçe ve Anti-Slop Mimari Kılavuzu)

Bu yetenek, Büyük Dil Modellerinin (LLM) İngilizce ağırlıklı eğitim verisi ve RLHF süreçleri yüzünden ürettiği "Yapay Zeka Türkçesini" (kelimeleri Türkçe ama cümle iskeleti İngilizce olan, mekanik, şişirilmiş ve tekdüze metinleri) doğal, nefes alan ve TDK kurallarına tam uyumlu insan Türkçesine dönüştürür.

Detaylı dilbilimi kuralları ve sözlük tabloları için bu dizindeki referans dosyalarını oku:

- `references/sentaks-ve-morfoloji.md`: Sola dallanma, ulaç sistemi, vurgu yuvası, `-DIr/-mAktAdIr` dozajı, zamir düşürme ve kof yardımcı fiil dönüşümleri.
- `references/ai-turkcesi-sozlugu.md`: Tier-1 (kesin AI ifşaları), Tier-2 (bürokratik bağlaçlar) ve Tier-3 (SaaS/pazarlama çeviri kalıpları) sözlüğü.
- `references/tdk-ve-noktalama.md`: 5 mutlak noktalama yasağı, TDK birleşik/ayrı kelimeler ve yabancı teknik terimlerin Türkçe okunuşa göre ek uyumu.
- `references/register-ve-ornekler.md`: 5 register × 9 üslup boyutu matrisi ve uçtan uca Before/After dönüşüm çiftleri.

## Temel İlkeler

1. **Kelime Değiştirmek Yetmez, Cümle Mimarisini Yeniden Kur:** Türkçe sondan eklemeli (agglutinative) ve sola dallanan (left-branching) bir dildir. İngilizcenin sağa dallanan SVO iskeletini koruyarak yalnızca eşanlamlı kelime değiştirmek AI etkisini silmez. Önce cümle mimarisini onar.
2. **Olgusal Sadakat Kilidi (Anti-Fabrication Lock):** Onarım (`rewrite`) modunda kaynak metinde bulunmayan hiçbir sayı, tarih, özel isim, kişisel anekdot veya nedensellik bağı uydurma. "İnsan gibi görünmek" için yalan söyleme, yalnızca mevcut bilginin ifade edilişini doğallaştır.
3. **Register (Bağlam) Dozajı:** Her metin aynı tonda yazılmaz. Akademik makalede `-mAktAdIr` eki doğalken, blog veya kurumsal bültende yapay durur. İşleme başlamadan önce metnin register'ını belirle.
4. **Sınırları Olan Kurallar:** Sınırı olmayan her kural yeni bir yapay tike dönüşür. Devrik cümle, söylem parçacığı (`işte`, `zaten`, `hani`) veya kısa cümle kullanımını kotaya bağlama ve silme testinden geçmeyen hiçbir üslup aracını metinde tutma.

## Çalışma Modları

Kullanıcı isteğine göre aşağıdaki üç moddan birini seç:

- **Onarım Modu (`rewrite` - Varsayılan):** Mevcut bir Türkçe metni veya çeviriyi alır, olgusal sadakati %100 koruyarak AI kalıplarını temizler ve cümle mimarisini Türkçeleştirir.
- **Üretim Modu (`write`):** Verilen bir konu veya taslaktan sıfırdan Türkçe metin üretir. Kompozisyon ve cümle kararlarını ilk cümleden itibaren İngilizce düşünmeden, doğrudan Türkçe kurar.
- **Denetim Modu (`audit`):** Metni yeniden yazmaz. Metindeki P0 (Kesin AI İfşası), P1 (Yapısal Çeviri Kokusu) ve P2 (Ritim/Noktalama Kusuru) sinyallerini alıntılayarak raporlar.

## Adım Adım İş Akışı (Mark -> Draft -> Audit -> Deletion Test)

### Adım 1: Register ve Üslup Kalibrasyonu

Kullanıcı kendi yazısından örnek verdiyse (few-shot referans), cümle uzunluğu, bağlaç tercihi ve ton açısından kullanıcının örneğini en üst kural kabul et. Örnek yoksa metni şu 5 register'dan birine ata (`references/register-ve-ornekler.md`):

| Register | Kompozisyon Müdahalesi | Cümle Mimarisi | `-DIr` / `-mAktAdIr` | Devrik Cümle ve Parçacık |
| :--- | :--- | :--- | :--- | :--- |
| **Blog / Deneme / Sosyal Medya** | Tam (Sahne ile başla, ilan etme) | Tam (Ulaç, özne düşürme, `-mIş`) | Tamamen sil | Serbest (400 kelimede maks. 2-3 devrik) |
| **Teknik Doküman / Mühendislik** | Orta (Doğrudan probleme gir) | Tam (Sola dallanma, ulaç, net yüklem) | Sil (Geniş zaman `-Ir/-Ar` kullan) | Devrik yok, parçacık çok az |
| **Kurumsal / İş İletişimi / SaaS** | Orta (Tezi ilk cümlede söyle) | Tam (Edilgeni etkene çevir, kof fiili at) | Yalnızca resmi tanımlarda | Devrik yok, doğal ve doğrudan |
| **Akademik / Resmi / Hukuki** | Kapalı (Belge iskeletini koru) | Sola dallanma, ulaç ve vurgu yuvası | Korunur, tekrarı azaltılır (100 kelimede yaklaşık 0,5-2,5, art arda 3 cümle aynı ekle bitmez) | Kesinlikle yasak |
| **Edebi / Anlatı** | Tam (Ritim ve imge odaklı) | Tam (Nefes uzunluğu varyasyonu yüksek) | Tamamen sil | Anlatı ritmine göre doğal |

### Adım 2: Üç Katmanlı Dönüşüm

#### Katman 1: Kompozisyon ve Retorik Kalıplar (P0 Sinyalleri)

- **Sahneleme Yerine Doğrudan Söyle:** "Bu yazıda X konusunu ele alacağız", "Günümüzün hızla değişen dünyasında" gibi sahneleme girişlerini silip konunun kendisine gir.
- **Negatif Paralellikleri Kaldır:** "Sadece X değil, aynı zamanda Y", "Bu bir A değil, bir B'dir" ve "X ile değil, Y ile" gibi tüm negatif paralellik kalıplarını olumlu ve net bir yargıya dönüştür (detaylar: `references/ai-turkcesi-sozlugu.md`).
- **Tek Satırlık Dramatik Kapanışları ve Özet Kuyruklarını Sil:** Paragraf sonlarındaki "İşte asıl fark burada ortaya çıkıyor.", "Sonuç olarak X'in önemi yadsınamaz." gibi ders veren kapanışları kes.
- **Üçlü Liste (Rule of Three) Otomatizmini Kır:** Fikirleri sürekli üçlü sıfat veya üçlü örnek grupları ("hızlı, güvenilir ve ölçeklenebilir") halinde dizme. Gerçekten kaç öğe varsa o kadarını sırala.
- **Kalın Etiketli Madde İmlerini (`**Başlık:** Açıklama`) Çöz:** Gerekmedikçe her paragrafı madde imine çevirme. Liste şartsa kalın etiket + iki nokta şablonu yerine yalın cümle kur.

#### Katman 2: Türkçe Cümle Mimarisi ve Sentaks (P1 Sinyalleri)

Detaylı kurallar ve örnekler için `references/sentaks-ve-morfoloji.md` dosyasını oku:

- **Sola Dallanma (Left-Branching):** Niteleyicileri ve yan cümleleri baş ismin arkasına veya Hint-Avrupa tipi `ki` bağlacıyla cümle sonuna takma, sıfat-fiillerle (`-An`, `-DIk`, `-AcAk`) ismin önüne al (*"Bir sistem kurduk, bu sistem verileri tarıyor"* -> *"Verileri tarayan bir sistem kurduk"*).
- **Refleks `ve` Yerine Ulaç (Zarf-Fiil) Sistemi:** Sıralı eylemleri mekanik `ve` veya `ve sonra` ile bağlamak yerine Türkçenin ulaç eklerini (`-Ip`, `-IncA`, `-dIkçA`, `-ArAk`, `-mAdAn`) kullan (*"Veriyi çektik ve işledik"* -> *"Veriyi çekip işledik"*).
- **`-DIr` ve `-mAktAdIr` Salgınını Durdur:** İngilizcedeki `is/are` koşulacını her cümlede `-DIr` veya `-mektedir` olarak çevirme. Akademik/hukuki register dışında *"Bu yöntem etkilidir ve hız sağlamaktadır"* yerine *"Bu yöntem etkili, sistemi de hızlandırıyor"* de.
- **Vurgu Yuvasını (Yüklem Önü) Kullan:** Türkçede vurgu kalın yazıyla veya *"Tam da bu noktada"* dolgusuyla değil, vurgulanacak öğeyi yüklemin hemen önüne çekerek verilir (*"Dün İzmir'e ben gittim"* vs. *"Ben İzmir'e dün gittim"*).
- **Zamir Düşürme (Pro-Drop) ve Gereksiz `"Bir"` / `"Kendi"` Temizliği:** Yüklemdeki şahıs eki özneyi zaten taşıyorsa `ben, sen, o, biz` zamirlerini düşür. İngilizce `a/an` karşılığı olarak her sıfat tamlamasına sokulan gereksiz `"bir"` kelimesini (*"iyi bir performans"* -> *"iyi performans"*) ve `own` çevirisi olan gereksiz `"kendi"` zamirini sil.
- **Edilgen Çatı (`tarafından`) ve Kof Yardımcı Fiilleri Temizle:** *"Ekibimiz tarafından gerçekleştirilmiştir"* yerine *"Ekibimiz yaptı"* de. *"Artış sağlamak / katkıda bulunmak / sahip olmak"* yerine doğrudan *"artırmak / katkı sunmak / barındırmak"* fiillerini kullan.
- **Kanıtsallık Kipi (`-mIş`):** Dolaylı öğrenilen, log kaydından okunan veya sonradan fark edilen durumlarda kesin geçmiş zaman (`-DI`) yerine Türkçenin delil kipini (`-mIş`) kullan (*"Sunucu gece yeniden başlamış"*).

#### Katman 3: TDK Yazım Kılavuzu, Noktalama ve Terminoloji (P2 Sinyalleri)

Detaylı kurallar için `references/tdk-ve-noktalama.md` dosyasını oku:

- **Beş Mutlak Noktalama ve Bağlaç Yasağı:**
  1. Diyalog dışında ara söz veya vurgu için **uzun çizgi (em-dash)** kullanma, yerine virgül veya nokta koy.
  2. Sayı ve tarih aralıklarında orta çizgi (en-dash) değil, TDK standardı olan **kısa çizgi (`-`)** kullan (`04.30-05.00`, `2024-2026`).
  3. İki bağımsız cümleyi İngilizce tarzı **noktalı virgül köprüsüyle** birbirine yapıştırma, cümleyi noktayla bitir.
  4. **`ama`, `fakat`, `lakin`, `ancak`, `ve`, `veya`, `ya da`** bağlaçlarından önce veya sonra virgül koyma.
  5. Başlıklarda İngilizce *Title Case* (her kelimenin ilk harfi büyük, `Ve / İle` dahil) yapma. Tümce düzeni kullan veya TDK kuralına göre bağlaçları küçük yaz (`ve`, `ile`, `ya da`).
- **Teknik Terimleri Zorla Çevirme, Okunuşuna Göre Ek Getir:** Sektörde yerleşik Türkçe karşılığı olmayan teknik terimleri (`endpoint`, `deploy`, `middleware`, `queue`, `cache`, `idempotent`) *"uç nokta, olay güdümlü, ara katman"* diye zorla çevirme. Kesme işaretiyle gelen ekleri yazılışa göre değil, **Türkçe okunuşa (fonetiğe)** göre getir: `cache'i` (keş), `queue'yu` (kü), `SQL'i` (es-kü-el), `JSON'ı` (ceyson).
- **TDK Bağlaç ve Birleşik Kelime Denetimi:** Bulunma durumu eki `-da/-de` (bitişik) ile bağlaç olan `da/de`'yi (ayrı), ilgi/sıfat eki `-ki` ile bağlaç olan `ki`'yi (`halbuki`, `oysaki`, `çünkü`, `mademki` kalıplaşmış bitişikler hariç ayrı) ve `birçok`, `birkaç`, `hiçbir`, `herhangi bir`, `pek çok`, `art arda`, `yanı sıra` yazımlarını denetle.

### Adım 3: Öz-Denetim (Self-Audit) ve Cümle Ritmi (Burstiness) Kontrolü

Taslağı oluşturduktan sonra kullanıcıya sunmadan önce şu kontrolleri yap:

- **Cümle Uzunluğu Varyasyonu (Burstiness CoV >= 0.40):** Arka arkaya gelen tüm cümleler 15-22 kelime bandında toplanmışsa ritim mekanikleşmiştir (CoV < 0.35). 3 veya daha fazla cümleli her paragrafta en az bir kısa/vurucu cümle (3-6 kelime) ile en az bir ulaçlı/sola dallanan uzun cümleyi (18-28 kelime) bir arada kullanarak değişim katsayısını (CoV) >= 0.40 seviyesinde tut.
- **Tier-1 Yasaklı Kelime Taraması:** Metinde `adeta`, `yadsınamaz`, `kritik bir rol oynamaktadır`, `derinlemesine`, `yelpaze`, `dönüm noktası`, `bununla birlikte`, `öte yandan`, `söz konusu`, `bu bağlamda` kalıplarının kalmadığından emin ol (`references/ai-turkcesi-sozlugu.md`).
- **Olgusal Sadakat Kontrolü:** Kaynak metindeki tüm sayılar, tarihler, teknik terimler ve iddialar korundu mu? Kaynakta olmayan bir sıfat veya abartı eklendi mi?

### Adım 4: Silme Testi (Deletion Test) ve Çıktı Teslimi

- Metne eklediğin her söylem parçacığını (`işte`, `zaten`, `tabii`), devrik cümleyi veya bağlacı test et: Kaldırdığında anlamdan veya tondan hiçbir şey eksilmiyorsa o öğeyi sil.
- Kullanıcı özellikle değişiklik raporu istemediyse ("neleri değiştirdin?" veya `audit` modu dışında) **yalnızca temizlenmiş/yazılmış metni** döndür ve başına "Elbette, metnin doğal Türkçeye çevrilmiş hali aşağıdadır:" gibi sohbet artıkları ekleme.

## Sık Yapılan Hatalar (Gotchas)

- **Aşırı Düzeltme (Overcorrection) Tuzağı:** Doğal bir Türkçe metinde geçen her `"bir"` kelimesini veya her devrik cümleyi hata sanma. `"Sen satışa bak"`, `"Site kurmak"`, `"Linki gönder"` gibi doğal ve yerleşik kullanımlara dokunma.
- **Öz-Türkçecilik Tuzağı:** Bu yetenek yabancı kökenli kelimeleri yasaklayan bir "arı dil" aracı değildir. Günlük ve mesleki Türkçede yaşayan kelimeleri (`performans`, `strateji`, `sistem`, `detay`) zorlama karşılıklarla değiştirme.
- **Sahte Samimiyet:** Kurumsal veya teknik bir metni insanlaştırmak adına metne *"Kahvenizi alın ve arkanıza yaslanın"*, *"Hepimiz oradaydık"* gibi çeviri blog klişeleri ekleme.
- **İkame Kelime Tiki (Replacement Tic) Tuzağı:** "Kritik bir rol oynar" veya "kusursuz bir şekilde" gibi yapay ifadeleri silerken her cümleye refleks olarak "doğrudan", "aslında" veya "ciddi ölçüde" ekleme. Çoğu zaman zarfı tamamen atıp fiili yalnız bırakmak en doğal sonucu verir.
- **Kılık Değiştirmiş Negatif Paralellik Tuzağı:** "Sadece X değil, aynı zamanda Y" kalıbını temizlerken yerine "X ile değil, Y ile" veya "geçici bir X değil, kalıcı bir Y" gibi başka bir negatif paralellik kurma. Olumsuz yarıyı tamamen atıp ne olduğunu söyle.


<!-- KAYNAK: references/sentaks-ve-morfoloji.md -->

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
  - **İnsan (Akademik - Kalibre Edilmiş Doz):** Akademik metinde `-mAktAdIr` korunur, sorun ekin kendisi değil tekrarıdır. Başlangıç hedefi olarak 100 kelimede yaklaşık `0,5 - 2,5` kullan. Bu aralık bir korpus ölçümüne dayanmaz, dedektörün kalibre edilebilir varsayılan değeridir. Art arda üç cümleyi aynı ekle (`-mektedir`, `-mıştır`, `-dır`) bitirme, geniş zaman (`-Ir/-Ar`) ve `-mIştIr` ile nöbetleşe kullan.

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


<!-- KAYNAK: references/ai-turkcesi-sozlugu.md -->

# "Yapay Zeka Türkçesi" (AI Slop & Translationese) Sözlüğü

Büyük Dil Modelleri (LLM), İngilizce eğitim verisinde aşırı temsil edilen klişeleri (`delve into`, `tapestry`, `testament to`, `pivotal`, `not only... but also`) Türkçeye birebir kalıp çevirisi (calque) olarak taşır. Bu sözlük, Türkçe metinlerdeki yapay zeka izlerini önem derecesine göre (Tier 1, Tier 2, Tier 3) sınıflandırır ve doğal Türkçe karşılıklarını sunar.

## 1. Tier-1: Kesin AI İfşaları (Tek Görülmede Silinmesi veya Değiştirilmesi Gerekenler)

Bu kelime ve kalıplar, doğal Türkçe metinlere kıyasla LLM çıktılarında 10 ila 50 kat daha sık görülür. Metinde tek bir kez bile geçseler müdahale edilmelidir.

| İngilizce Kaynak Kalıp | Yapay Zeka Türkçesi (Yasaklı / Klişe) | Doğal ve İnsani Türkçe Alternatifi | Örnek Dönüşüm (Önce -> Sonra) |
| :--- | :--- | :--- | :--- |
| *undeniable / undeniably* | **yadsınamaz / yadsınamaz bir gerçek ki / inkar edilemez** | açık, ortada, belli, tartışmasız (veya tamamen silip doğrudan olguyu yaz) | *"Yapay zekanın etkisi yadsınamaz."* -> *"Yapay zeka iş yapış biçimimizi değiştirdi."* |
| *virtually / almost like / veritable* | **adeta** (her benzetmede kullanımı) | neredeyse, sanki, gibi (çoğu zaman tamamen silinmeli) | *"Sektörde adeta bir devrim yarattı."* -> *"Sektörün kurallarını değiştirdi."* |
| *delve into / dive deep into* | **derinlemesine inmek / derinlemesine incelemek / mercek altına almak** | ayrıntısına bakmak, yakından incelemek, deşmek, ele almak | *"Konunun derinlemesine inelim."* -> *"Konunun ayrıntılarına bakalım."* |
| *tapestry / mosaic / kaleidoscope* | **zengin bir doku / mozaik / harman / yelpaze (geniş bir yelpazede)** | çeşitlilik, bir arada bulunmak, çok yönlü yapı, farklı alanlarda | *"Kültürel bir mozaik ve geniş bir yelpaze sunar."* -> *"Farklı kültürleri bir araya getirir."* |
| *stands as a testament to* | **...nın bir kanıtıdır / en büyük göstergesidir / nişanesidir** | ...-dığını gösterir, ortaya koyar | *"Bu başarı ekibin azminin bir kanıtıdır."* -> *"Bu sonuç ekibin ne kadar sıkı çalıştığını gösteriyor."* |
| *plays a pivotal / crucial role* | **kritik bir rol oynamaktadır / hayati öneme sahiptir / kilit rol üstlenir** | belirler, belkemiğini oluşturur, çok önemli, şart | *"Veri kalitesi model başarısında kritik bir rol oynamaktadır."* -> *"Modelin başarısını veri kalitesi belirler."* |
| *in today's fast-paced / digital world* | **günümüzün hızla değişen dünyasında / dijitalleşen çağımızda** | **Tamamen sil.** (Konuya doğrudan gir) | *"Günümüzün hızla değişen dünyasında hız önemlidir."* -> *"Müşteri artık saniyeler içinde yanıt bekliyor."* |
| *not only X, but also Y* | **sadece X değil, aynı zamanda Y / yalnızca X olmakla kalmayıp...** | hem X hem Y, X'in yanında Y de..., X yapıyor üstelik Y... | *"Sadece hızı artırmakla kalmaz, aynı zamanda maliyeti düşürür."* -> *"Hem hızı artırır hem de maliyeti düşürür."* |
| *it is not X, it is Y* (Negatif Paralellik) | **bu bir X değil, bir Y'dir / mesele X değil, Y** | Olumsuz yarıyı atıp yalnızca Y olduğunu söyle (kimsenin iddia etmediği X'i reddetme) | *"Bu sadece bir güncelleme değil, yeni bir başlangıçtır."* -> *"Bu sürümle mimariyi baştan aşağı yeniledik."* |
| *unlock the potential / unleash* | **potansiyelini ortaya çıkarmak / tam potansiyeline ulaşmak / kilidini açmak** | verimli kullanmak, önünü açmak, kapasitesini artırmak | *"Ekibinizin potansiyelini ortaya çıkarın."* -> *"Ekibinizin elini güçlendirin / daha verimli çalışın."* |
| *watershed moment / turning point* | **dönüm noktası / kilometre taşı / çığır açan (groundbreaking)** | önemli eşik, yeni aşama, ilk kez ... sağlayan | *"Sektör için çığır açan bir dönüm noktasıdır."* -> *"Sektörde ilk kez gerçek zamanlı denetim sağlıyor."* |
| *seamlessly / effortless* | **kusursuz bir şekilde / pürüzsüzce / zahmetsizce** | kolayca, takılmadan, doğrudan, ek ayar gerektirmeden | *"Mevcut sisteminizle kusursuz bir şekilde entegre olur."* -> *"Mevcut sisteminize ek ayar gerektirmeden bağlanır."* |
| *meticulously / painstakingly* | **titizlikle / özenle hazırlanmış** | dikkatle, tek tek kontrol edilerek (veya somut kanıt ver) | *"Titizlikle eğitilmiş modelimiz..."* -> *"120 bin Türkçe belgeyle eğitilen modelimiz..."* |
| *nestled in the heart of* | **...nın kalbinde yer alan** | ... merkezindeki, ...'da bulunan | *"İstanbul'un kalbinde yer alan ofisimiz..."* -> *"Levent'teki ofisimiz..."* |

## 2. Tier-2: Bürokratik Bağlaçlar, Geçiş Dolguları ve Şişirilmiş Sıfatlar (Yoğunlukta Temizlenenler)

Bu ifadeler tek başına yanlış değildir ancak LLM'ler her paragraf başında ve cümle geçişinde bunları mekanik olarak tekrarlar. Bir metinde birden fazla geçiyorsa silinmeli veya sadeleştirilmelidir.

| Kategori | Yapay Zeka / Çeviri Kalıbı | Doğal Türkçe Alternatifi veya Eylem |
| :--- | :--- | :--- |
| **Geçiş Bağlaçları (*Moreover / Furthermore / However*)** | **Bununla birlikte / Öte yandan / Buna ek olarak / Dahası / Üstelik** (her paragraf başında) | Bağlacı silip cümleye gir. Gerekiyorsa `Ayrıca`, `Ama`, `Üstelik`, `Diğer taraftan` veya cümle içi `ise / de` kullan. |
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
| *Leverage / Utilize* | **Kaldıraç olarak kullanmak / İstifade etmek / Yararlanmak** | Kullanmak / Değerlendirmek |
| *No credit card required* | **Kredi kartı istenmez / Kart istemiyoruz** | Kredi kartı gerekmez |
| *Send on WhatsApp / Share on X* | **WhatsApp'ta gönder / X üzerinde paylaş** | WhatsApp'tan gönder / X'te paylaş (Hâl eki uyumuna dikkat) |
| *See who opened and edited* | **Kim açtı, kim düzenledi gör** | Kimin açtığını, kimin düzenlediğini gör |
| *Let's dive in! / Here's the thing:* | **Hadi başlayalım! / Mesele şu ki: / İşin sırrı şurada:** | **Tamamen sil.** |

## 4. Sohbet ve Asistan Artıkları (Chat Residue - Anında Silinecekler)

Metin çıktılarının başında veya sonunda asla yer almaması gereken ifadeler:

- *"Elbette! İşte metninizin daha doğal ve insani Türkçeye uyarlanmış hali:"*
- *"Harika bir konu! Gelin bu konuyu birlikte inceleyelim."*
- *"Umarım bu düzenleme işinize yarar! Başka bir değişiklik isterseniz lütfen belirtin."*
- *"Değişiklik Özeti: 1. Uzun çizgiler kaldırıldı..."* (Kullanıcı özellikle `audit` veya açıklama istemediyse ekleme).


<!-- KAYNAK: references/tdk-ve-noktalama.md -->

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


<!-- KAYNAK: references/register-ve-ornekler.md -->

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
| **Kip Dağılımı** | `-yor`, `-DI`, `-mIş` (delil), geniş zaman | Geniş zaman (`-Ir/-Ar` kurallar için), `-DI`, `-mIş` | Geniş zaman, `-yor`, `-DI` | Geniş zaman, `-mAktAdIr` (100 kelimede yaklaşık 0,5-2,5), `-DIr` | Tüm kipler serbest |
| **Söylem Parçacıkları** | `işte, zaten, ise, hani, tabii, daha doğrusu` | `ise, aslında, daha doğrusu, örneğin` | `ise, özellikle, doğrudan` | Yalnızca `ise, nitekim, dolayısıyla` | Doğal akışa göre serbest |
| **Devrik Cümle Oranı** | 400 kelimede 2-3 adet | Sıfır (0) | Sıfır (0) | Sıfır (0) | Anlatı ritmine göre doğal |
| **Terim Tercihi** | Günlük karşılıklar veya okunuşa göre çekimli terim | Yerleşik İngilizce terim olduğu gibi (`endpoint'e`) | Sektör standardı, jargonsuz sade Türkçe | TDK ve alan terimleri (`veri tabanı, alanyazın`) | Türkçe duygu ve imge değeri yüksek sözcükler |
| **Açılış Hamlesi** | Sahne, somut gözlem veya doğrudan soru | Doğrudan problem veya mimari karar | Temel değer önermesi veya ana mesaj | Araştırma problemi veya olgusal çerçeve | Atmosfer, detay veya iç ses |

## 2. Aynı İddianın 4 Farklı Register'daki Doğal Yazımı

- **Ham AI Çıktısı (Makine Türkçesi):**
  > *"Cache stratejisinin doğru bir şekilde belirlenmesi, sistem performansı açısından kritik bir öneme sahiptir ve gecikme sürelerinin azaltılmasında yadsınamaz bir rol oynamaktadır."*
- **Akademik / Resmi Register:**
  > *"Önbellekleme stratejisinin doğru kurgulanması, sistem performansını ve yanıt sürelerini belirlemektedir."*
- **Teknik / Mühendislik Register:**
  > *"Cache stratejisini doğru kurgulamak performansı artırır ve gecikmeyi düşürür."*
- **Kurumsal / Ürün Register:**
  > *"Doğru önbellek kurgusu, sisteminizi hızlandırırken yanıt sürelerini kısaltır."*
- **Blog / Deneme Register:**
  > *"Performansı belirleyen asıl şey cache stratejisi işte. Doğru kurduğunuzda gecikme yarı yarıya düşüyor."*

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
> Uzaktan çalışma artık şirket kültürünün kalıcı bir parçası. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik artıyor. İşin zor kısmı, ekip aynı ofisi paylaşmazken iletişimi koparmamak. Kalıcı çözüm ise çalışma düzenini baştan sona bu yeni ritme göre kurgulamaktan geçiyor.

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
> Çok okunan bir `cache` anahtarının süresi dolduğu anda gelen yüzlerce istek aynı anda veritabanına yüklenir ve sistemi kilitler. Özellikle yüksek trafikli `endpoint`'lerde bu durum kesintiye yol açar. Dağıtık kilit (`distributed lock`) kullanarak veritabanına yalnızca tek bir isteğin gitmesini sağlayabilirsiniz ama bu yöntem diğer isteklerin bekleme süresini uzatır.

### Örnek 3: Akademik / Analitik Metin (Olgusal Sadakat ve Dozaj Korunarak)

**Önce (Tipik AI Türkçesi):**
> Türkiye'de 2020-2024 yılları arasında yenilenebilir enerji yatırımları sadece artış göstermekle kalmamış, aynı zamanda enerji arz güvenliğinde de çığır açan bir dönüm noktası olmuştur. Enerji Bakanlığı tarafından paylaşılan verilere göre, güneş enerjisi kurulu gücü %112 oranında bir büyüme gerçekleştirmiştir ki bu durum sektörün dinamik yapısının en büyük kanıtıdır.

**Sonra (Doğal İnsan Türkçesi - Akademik Register):**
> Türkiye'de 2020-2024 döneminde hız kazanan yenilenebilir enerji yatırımları, enerji arz güvenliğinin yapısını da dönüştürmüştür. Enerji Bakanlığının verilerine göre güneş enerjisi kurulu gücü bu dönemde %112 büyümüştür.
