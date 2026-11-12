---
name: turkish-anti-ai-skill
description: Türkçe metni insan eliyle yazılmış gibi doğal yazar veya onarır. Kullanıcı Türkçe bir metin için "insanileştir", "humanize et", "AI hissiyatını sil" veya "doğal Türkçeye çevir" dediğinde, metinde çeviri kokusu ya da TDK hatası denetimi istediğinde, Türkçe blog, makale, kurumsal yazı, sosyal medya içeriği veya teknik doküman yazarken kullan.
license: MIT
metadata:
  author: yucezerey
  version: "1.1.0"
---

# Turkish Anti-AI Skill (Doğal Türkçe ve Anti-Slop Mimari Kılavuzu)

Bu yetenek, Büyük Dil Modellerinin (LLM) İngilizce ağırlıklı eğitim verisi ve RLHF süreçleri yüzünden ürettiği "Yapay Zekâ Türkçesini" (kelimeleri Türkçe ama cümle iskeleti İngilizce olan, mekanik, şişirilmiş ve tekdüze metinleri) doğal, nefes alan ve TDK kurallarına tam uyumlu insan Türkçesine dönüştürür.

Detaylı dilbilimi kuralları ve sözlük tabloları için bu dizindeki referans dosyalarını oku:

- `references/sentaks-ve-morfoloji.md`: Türkçe cümlenin geometrisi (öge dizilimi, bilgi yapısı, gömme derinliği), sola dallanma, ulaç sistemi, vurgu yuvası, `-DIr` ile `-mAktAdIr` ayrımı, zamir düşürme, adlaştırma zincirleri ve kof yardımcı fiil dönüşümleri.
- `references/ai-turkcesi-sozlugu.md`: Tier-1 (kesin AI ifşaları), Tier-2 (bürokratik bağlaçlar) ve Tier-3 (SaaS/pazarlama çeviri kalıpları) sözlüğü.
- `references/tdk-ve-noktalama.md`: 5 mutlak noktalama yasağı, TDK birleşik/ayrı kelimeler ve yabancı teknik terimlerin Türkçe okunuşa göre ek uyumu.
- `references/register-ve-ornekler.md`: 5 register × 9 üslup boyutu matrisi ve uçtan uca Before/After dönüşüm çiftleri.
- `references/sosyal-medya.md`: LinkedIn, Instagram ve X post register'ı: hook geometrisi, platform karakter/hashtag bütçeleri, emoji ve CTA kuralları, posta özgü AI kalıpları ve yayın kapısı.

## Temel İlkeler

1. **Kelime Değiştirmek Yetmez, Cümle Mimarisini Yeniden Kur:** Türkçe sondan eklemeli (agglutinative) ve sola dallanan (left-branching) bir dildir. İngilizcenin sağa dallanan SVO iskeletini koruyarak yalnızca eşanlamlı kelime değiştirmek AI etkisini silmez. Önce cümle mimarisini onar.
2. **Olgusal Sadakat Kilidi (Anti-Fabrication Lock):** Onarım (`rewrite`) modunda kaynak metinde bulunmayan hiçbir sayı, tarih, özel isim, kişisel anekdot veya nedensellik bağı uydurma. "İnsan gibi görünmek" için yalan söyleme, yalnızca mevcut bilginin ifade edilişini doğallaştır. Bir klişeyi silince yerine somut bilgi gerekiyorsa ve bu bilgi kaynakta yoksa onu uydurma. Ya klişeyi sadeleştirip olduğu kadarını söyle ya da köşeli yer tutucu bırak (`[somut veri: kaç belge?]`) ve kullanıcıya sor. Referans dosyalarındaki örnekler bu biçimi kullanır. Sayı, miktar ve kesinlik derecesi de bilgidir. "Birçok" yerine "yüzlerce", "artırabilir" yerine "artırır" yazmak da uydurmadır.
3. **Register (Bağlam) Dozajı:** Her metin aynı tonda yazılmaz. Akademik makalede `-mAktAdIr` eki doğalken, blog veya kurumsal bültende yapay durur. İşleme başlamadan önce metnin register'ını belirle.
4. **Sınırları Olan Kurallar:** Sınırı olmayan her kural yeni bir yapay tike dönüşür. Devrik cümle, söylem parçacığı (`işte`, `zaten`, `hani`) veya kısa cümle kullanımını kotaya bağlama ve silme testinden geçmeyen hiçbir üslup aracını metinde tutma.

## Çalışma Modları

Kullanıcı isteğine göre aşağıdaki üç moddan birini seç:

- **Onarım Modu (`rewrite` - Varsayılan):** Mevcut bir Türkçe metni veya çeviriyi alır, olgusal sadakati %100 koruyarak AI kalıplarını temizler ve cümle mimarisini Türkçeleştirir.
- **Üretim Modu (`write`):** Verilen bir konu veya taslaktan sıfırdan Türkçe metin üretir. Kompozisyon ve cümle kararlarını ilk cümleden itibaren İngilizce düşünmeden, doğrudan Türkçe kurar.
- **Denetim Modu (`audit`):** Metni yeniden yazmaz. Metindeki P0 (Kesin AI İfşası), P1 (Yapısal Çeviri Kokusu) ve P2 (Ritim/Noktalama Kusuru) sinyallerini alıntılayarak raporlar.
- **Post Modu (`post`):** LinkedIn, Instagram veya X için post yazar ya da mevcut postu onarır. Post register'ı ayrı dosyadadır (`references/sosyal-medya.md`); cümle sayısı az olduğu için ritim ölçümü yerine hook, karakter bütçesi, hashtag, tek CTA ve uydurulmuş sayı kuralları geçerlidir. Yayından önce `scripts/denetle_post.py` kapısı zorunludur.

## Adım Adım İş Akışı (Mark -> Draft -> Audit -> Deletion Test)

### Adım 1: Register ve Üslup Kalibrasyonu

Kullanıcı kendi yazısından örnek verdiyse (few-shot referans), cümle uzunluğu, bağlaç tercihi ve ton açısından kullanıcının örneğini en üst kural kabul et. Örnek yoksa metni şu 5 register'dan birine ata (`references/register-ve-ornekler.md`):

| Register | Kompozisyon Müdahalesi | Cümle Mimarisi | `-DIr` / `-mAktAdIr` | Devrik Cümle ve Parçacık |
| :--- | :--- | :--- | :--- | :--- |
| **Blog / Deneme / Sosyal Medya** | Tam (Sahne ile başla, ilan etme) | Tam (Ulaç, özne düşürme, `-mIş`) | `-mAktAdIr` sil, ad cümlesinde `-DIr` seyrek | Serbest ama seyrek (400 kelimede 2-3 devrik yol gösterici bir tahmin) |
| **Teknik Doküman / Mühendislik** | Orta (Doğrudan probleme gir) | Tam (Sola dallanma, ulaç, net yüklem) | `-mAktAdIr` yerine `-Ar/-Ir` veya `-(I)yor`, tanım cümlesinde `-DIr` korunur | Devrik yok, parçacık çok az |
| **Kurumsal / İş İletişimi / SaaS** | Orta (Tezi ilk cümlede söyle) | Tam (Kurumun kendi eylemini etkene çevir, kof fiili at) | `-mAktAdIr` yalnızca resmî duyuruda, `-DIr` tanımda | Devrik yok, doğal ve doğrudan |
| **Akademik / Resmî / Hukuki** | Kapalı (Belge iskeletini koru) | Sola dallanma, ulaç ve vurgu yuvası | Korunur, tekrarı azaltılır (100 kelimede yaklaşık 0,5-2,5, art arda üç cümle aynı ekle bitmez, geniş zamanla nöbetleşe) | Kesinlikle yasak |
| **Edebî / Anlatı** | Tam (Ritim ve imge odaklı) | Tam (Nefes uzunluğu varyasyonu yüksek) | `-mAktAdIr` sil, `-DIr` anlatı akışında seyrek | Anlatı ritmine göre doğal |

### Adım 2: Üç Katmanlı Dönüşüm

#### Katman 1: Kompozisyon ve Retorik Kalıplar (P0 Sinyalleri)

- **Sahneleme Yerine Doğrudan Söyle:** "Bu yazıda X konusunu ele alacağız", "Günümüzün hızla değişen dünyasında" gibi sahneleme girişlerini silip konunun kendisine gir.
- **Negatif Paralellikleri Kaldır:** "Sadece X değil, aynı zamanda Y", "Bu bir A değil, bir B'dir" ve "X ile değil, Y ile" gibi tüm negatif paralellik kalıplarını olumlu ve net bir yargıya dönüştür (detaylar: `references/ai-turkcesi-sozlugu.md`).
- **Tek Satırlık Dramatik Kapanışları ve Özet Kuyruklarını Sil:** Paragraf sonlarındaki "İşte asıl fark burada ortaya çıkıyor.", "Sonuç olarak X'in önemi yadsınamaz." gibi ders veren kapanışları kes.
- **Üçlü Liste (Rule of Three) Otomatizmini Kır:** Fikirleri sürekli üçlü sıfat veya üçlü örnek grupları ("hızlı, güvenilir ve ölçeklenebilir") hâlinde dizme. Gerçekten kaç öge varsa o kadarını sırala.
- **Kalın Etiketli Madde İmlerini (`**Başlık:** Açıklama`) Çöz:** Gerekmedikçe her paragrafı madde imine çevirme. Liste şartsa kalın etiket + iki nokta şablonu yerine yalın cümle kur.

#### Katman 2: Türkçe Cümle Mimarisi ve Sentaks (P1 Sinyalleri)

Detaylı kurallar ve örnekler için `references/sentaks-ve-morfoloji.md` dosyasını oku:

- **Öge Dizilimi ve Bilgi Yapısı:** Türkçe baş sonda bir dildir. Cümle başına bilinen konuyu, yüklemin hemen önüne yeni ya da vurgulanan bilgiyi koy. Belirtisiz nesneyi yüklemden ayırma (*"Ahmet'e rapor gönderdim"*). İngilizce yarık cümleyi (*"Bunu mümkün kılan şey X'ti"*) odağı yüklem önüne alarak çöz (*"Bunu X mümkün kıldı"*).
- **Sola Dallanma (Left-Branching):** Niteleyicileri ve yan cümleleri baş ismin arkasına ya da `ki` ile cümle sonuna takma, sıfat-fiillerle (`-(y)An`, `-DIk`, `-(y)AcAk`) ismin önüne al (*"Bir sistem kurduk, bu sistem verileri tarıyor"* -> *"Verileri tarayan bir sistem kurduk"*). Ama bir adın önüne ikiden fazla iç içe yan cümle yığma, o durumda cümleyi böl.
- **Refleks `ve` Yerine Ulaç (Zarf-Fiil) Sistemi:** Sıralı eylemleri mekanik `ve` veya `ve sonra` ile bağlamak yerine Türkçenin ulaç eklerini (`-(y)Ip`, `-(y)IncA`, `-DIkçA`, `-(y)ArAk`, `-mAdAn`) kullan (*"Veriyi çektik ve işledik"* -> *"Veriyi çekip işledik"*). Ulaçlı yan cümlenin söylenmeyen öznesi ana cümlenin öznesi sayılır. Özneler farklıysa ulaç kullanma.
- **`-mAktAdIr` ile `-DIr`'ı Ayrı Ele Al:** `-mAktAdIr` akademik ve resmî register dışında `-(I)yor` ya da `-Ar/-Ir` olur (*"kolaylık sağlamaktadır"* -> *"işini kolaylaştırıyor"*). Ad cümlesindeki `-DIr` tanım ve sınıflandırmada korunur (*"Redis bir anahtar-değer veri tabanıdır"*), anlatı akışında seyreltilir. Sıralı yüklemlerde eki yalnızca sonuncuya getir (*"hızlıdır ve güvenilirdir"* -> *"hızlı ve güvenilirdir"*).
- **Vurgu Yuvasını (Yüklem Önü) Kullan:** Türkçede vurgu kalın yazıyla veya *"Tam da bu noktada"* dolgusuyla değil, vurgulanacak ögeyi yüklemin hemen önüne çekerek verilir (*"Dün İzmir'e ben gittim"* vs. *"Ben İzmir'e dün gittim"*). Yüklemden sonraya yalnızca bağlamdan bilinen öge alınabilir.
- **Zamir Düşürme (Pro-Drop), `"Bir"` Yoğunluğu ve `"Kendi"`:** Yüklemdeki kişi eki özneyi zaten taşıyorsa `ben, sen, o, biz` zamirlerini düşür, çünkü açık zamir karşıtlık bildirir. `bir` tek başına hata değildir (*"derin bir iz bıraktı"*). Önce kalıplaşmış birleşik eylemlerin içindekini at (*"büyük bir önem taşıyor"* -> *"büyük önem taşıyor"*), bir cümlede birden fazla *sıfat + bir + soyut ad* varsa seyrelt. `own` çevirisi olan gereksiz `"kendi"` zamirini sil.
- **Edilgen Çatı (`tarafından`), Adlaştırma ve Kof Yardımcı Fiiller:** `tarafından` Türkçenin kendi yapısıdır (*"Köprü Mimar Sinan tarafından yapıldı"*). Yalnızca eyleyen yazarın kendisi ya da kurumu olduğunda (*"Ekibimiz tarafından gerçekleştirilmiştir"* -> *"Ekibimiz yaptı"*) veya kof eylemle birlikte geldiğinde etkene çevir. *"-mAsI gerekmektedir / sağlanmalıdır"* zincirlerini doğrudan çekimle çöz (*"yedeklenmesinin sağlanması gerekmektedir"* -> *"yedeklenmeli"*). *"Gerçekleştirmek, sağlamak, sahip olmak"* öbeklerini seyrelt. `katkıda bulunmak` yerleşik bir deyimdir, sözlükte yer almayan `katkı sunmak` ile değiştirme.
- **Kanıtsallık Kipi (`-mIş`):** Dolaylı öğrenilen, log kaydından okunan veya sonradan fark edilen durumlarda gündelik ve blog register'ında Türkçenin kanıtsallık kipini (`-mIş`) kullan (*"Sunucu gece yeniden başlamış"*). Resmî rapor ve tutanakta kayıtla kesinleşmiş olgu için `-DI` olağandır.

#### Katman 3: TDK Yazım Kılavuzu, Noktalama ve Terminoloji (P2 Sinyalleri)

Detaylı kurallar için `references/tdk-ve-noktalama.md` dosyasını oku:

- **Noktalama ve Bağlaç Kuralları:** `[TDK]` etiketli kurallar TDK Yazım Kılavuzu'na dayanır ve her register'da geçerlidir. `[Üslup]` etiketli kurallar çeviri kokusunu azaltan tercihlerdir ve register'a göre esnetilebilir.
  1. `[TDK]` **Uzun çizgi (em-dash)** yalnızca satır başında konuşma çizgisi olarak kullanılır. Ara söz için virgül ya da TDK'nın ara söz kuralındaki bitişik kısa çizgiyi kullan (*"Küçük bir sürü -dört inekle birkaç koyun- yolun ağzında durmuştu."*). Çoğu zaman en doğal çözüm cümleyi ikiye bölmektir.
  2. `[TDK]` Sayı ve tarih aralıklarında orta çizgi (en-dash) değil **kısa çizgi (`-`)** kullan (`09.30-10.30`, `2024-2026`).
  3. `[TDK]` **`ve`, `veya`, `yahut`, `ya ... ya`** bağlaçlarından önce ve sonra virgül konmaz. `[Üslup]` `ama`, `fakat`, `lakin` için TDK'da virgül kuralı yoktur. İngilizcedeki `..., but` alışkanlığıyla her `ama`dan önce refleks virgül koyma ama uzun cümlede okumayı kolaylaştıran virgülü hata sayma.
  4. `[Üslup]` İç virgülü olmayan iki bağımsız cümleyi İngilizce tarzı **noktalı virgül köprüsüyle** yapıştırma, noktayla ayır. `[TDK]` Noktalı virgülün kılavuzdaki kullanımları doğrudur ve özellikle akademik/hukuki metinde korunur: virgülle ayrılmış tür veya takımları ayırmak, ögeleri arasında virgül bulunan sıralı cümleleri ayırmak.
  5. `[TDK]` Kitap, bildiri ve makalede ana başlık tamamen büyük harfle, alt başlıklar her kelimenin ilk harfi büyük olarak yazılır. Kelimelerin yalnızca ilk harfi büyük yazıldığında `ve`, `ile`, `ya`, `veya`, `yahut`, `ki`, `da`, `de` ve `mı/mi` soru eki küçük kalır (`Suç ve Ceza`). Başlığın tamamı büyük harfle yazıldığında bunlar da büyük yazılır (`YAPAY ZEKÂ VE GELECEK`). Hata, ilk harfleri büyük başlıkta bağlacı büyük yazmaktır (`Yapay Zekâ Ve Gelecek`). `[Üslup]` Blog, teknik belge ve kurumsal metinde ara başlığı tümce düzeninde yazmak daha doğal durur.
- **Teknik Terimleri Zorla Çevirme, Okunuşuna Göre Ek Getir:** Sektörde yerleşik Türkçe karşılığı olmayan teknik terimleri (`endpoint`, `deploy`, `middleware`, `queue`, `cache`, `idempotent`) *"uç nokta, olay güdümlü, ara katman"* diye zorla çevirme. `[TDK]` Kısaltmalara gelen ekler kesmeyle ayrılır ve okunuşa uyar (`TDK'nin`, `TV'ye`). `[Üslup]` Yabancı cins isimlere kesmeyle ek getirmek TDK'da düzenlenmemiş ama yerleşik bir yazım geleneğidir. Bu durumda da ek yazılışa göre değil, **Türkçe okunuşa (fonetiğe)** göre gelir: `cache'i` (keş), `queue'yu` (kü), `SQL'i` (es-kü-el), `JSON'ı` (ceyson).
- **TDK Bağlaç ve Birleşik Kelime Denetimi:** Bulunma durumu eki `-da/-de` (bitişik) ile bağlaç olan `da/de`'yi (ayrı), ilgi/sıfat eki `-ki` ile bağlaç olan `ki`'yi (`belki`, `çünkü`, `hâlbuki`, `mademki`, `meğerki`, `oysaki`, `sanki` kalıplaşmış bitişikler hariç ayrı) ve `birçok`, `birkaç`, `hiçbir`, `herhangi bir`, `pek çok`, `art arda`, `yanı sıra` yazımlarını denetle.

### Adım 3: Öz Denetim (Self-Audit) ve Cümle Ritmi (Burstiness) Kontrolü

Taslağı oluşturduktan sonra kullanıcıya sunmadan önce şu kontrolleri yap:

- **Cümle Uzunluğu Varyasyonu (Burstiness CoV >= 0.40):** Arka arkaya gelen tüm cümleler 15-22 kelime bandında toplanmışsa ritim mekanikleşmiştir. Dedektör iki eşik kullanır: `0.35` altı mekanik (uyarı), `0.40` ve üzeri hedef, arası kabul edilebilir. 3 veya daha fazla cümleli her paragrafta en az bir kısa/vurucu cümle (3-6 kelime) ile en az bir ulaçlı/sola dallanan uzun cümleyi (18-28 kelime) bir arada kullanarak CoV'u `0.40` seviyesinin altına düşürme. Dedektör bu ölçümü yalnızca düz yazı üzerinde yapar; kod bloğu, başlık, tablo satırı ve liste işaretçisi ölçüme girmez. CoV ayrıca kelime sayısı düşük metinlerde (3 cümleden az) güvenilir değildir, tek başına karar ölçütü sayma.
- **Register'da Yerleşik Kalıpları Kusur Sayma:** `söz konusu`, `bu bağlamda`, `sonuç olarak`, `tarafından` + kof eylem gibi kalıplar akademik/resmî/hukuki metinde standarttır. Dedektör bunları o register'da **bilgi** olarak listeler ve puana katmaz; aynı kalıp blog veya kurumsal metinde **sinyal** sayılır. Raporda bir kalemin `[bilgi]` mi `[sinyal]` mi olduğuna bak.
- **Tier-1 Yasaklı Kelime Taraması:** Metinde `âdeta` (`adeta`), `yadsınamaz`, `kritik bir rol oynamaktadır`, `derinlemesine`, `yelpaze`, `dönüm noktası`, `bununla birlikte`, `öte yandan`, `söz konusu`, `bu bağlamda` kalıplarının kalmadığından emin ol (`references/ai-turkcesi-sozlugu.md`).
- **Olgusal Sadakat Kontrolü:** Kaynak metindeki tüm sayılar, tarihler, teknik terimler ve iddialar korundu mu? Kaynakta olmayan bir sayı, yer adı, kişi, sıfat veya abartı eklendi mi? Artış/azalış yönü, olumsuzluk ve ihtiyat (`-ebilir`, `görünüyor`) aynı kaldı mı? Ritim hedefini tutturmak için kaynakta olmayan kısa bir cümle eklendiyse sil.

### Adım 4: Silme Testi (Deletion Test) ve Çıktı Teslimi

- Metne eklediğin her söylem parçacığını (`işte`, `zaten`, `tabii`), devrik cümleyi veya bağlacı test et: Kaldırdığında anlamdan veya tondan hiçbir şey eksilmiyorsa o ögeyi sil.
- Kullanıcı özellikle değişiklik raporu istemediyse ("neleri değiştirdin?" veya `audit` modu dışında) **yalnızca temizlenmiş/yazılmış metni** döndür ve başına "Elbette, metnin doğal Türkçeye çevrilmiş hâli aşağıdadır:" gibi sohbet artıkları ekleme.

## Sosyal Medya Postu ve Yayın Kapısı

Post yazarken `references/sosyal-medya.md` dosyasını oku. Kısaltılmış kural seti:

1. İlk satır somut olgu, 12 kelimeyi geçmez; "Bu yazıda", "Gururla duyuruyoruz" ve "Günümüzün hızla değişen" ile başlamaz.
2. Paragraf başına 1 ile 3 cümle. Beş cümlelik blok, okuru kaydırır.
3. Emoji 0 ile 3 arası ve satır başında madde imi olarak kullanılmaz. Kalın etiketli liste (`**Neden?** ...`) düz cümleye çevrilir.
4. Hashtag sonda: LinkedIn 2 ile 5, Instagram 3 ile 10, X 0 ile 2. Gövde içine etiket serpiştirilmez.
5. Tek CTA, tek fiil. "Yorumlarda buluşalım" ve "beğenin, kaydedin, paylaşın" üçlüsü kullanılmaz.
6. Her sayı `# Teknik doğruluk notu` içinde karşılığını bulur. Notta olmayan sayı uydurulmuş sayıdır. Teknoloji, lisans ve ölçüm iddiaları (`Flutter`, `Apache-2.0`, `sunucu yok`) de aynı notta geçer.
7. `tip: B` ise `gizlilik: kontrol edildi` yazılır; `kaynak: private` ise metinde link ya da kurulum komutu olmaz. `tip: A` ise repo linki gövdede geçer.
8. Fork reposu kendi ürünün gibi anlatılmaz: upstream adı doğruluk notunda, cümle "uyarladım" çerçevesinde kurulur.
9. Instagram postu 6 slayttır; her slaytta `TR:` ve `EN:` satırı olur. Slayt metni de bu kurallara tabidir, çünkü görsele basılan cümle caption'dan çok okunur.
10. Postta e-posta, telefon, IBAN, token, IP ve yerel dosya yolu olmaz; `Github`, `Javascript` gibi yazımlar ve `Faz 3 / W46 / sprint` jargonu düzeltilir.

Yazdıktan sonra kapıyı çalıştır ve hatasız hâle getir:

```
python3 scripts/denetle_post.py <post-dosyasi>      # çıkış 0 = yayına uygun
python3 scripts/denetle_post.py <takvim-dizini>     # bütün postlar
python3 scripts/denetle_post.py --takvim <dizin>    # postlar arası tekrar + denge
python3 scripts/denetle_post.py <post.md> --canli   # kaynak/demo linklerini yokla
python3 scripts/denetle_post.py <post.md> --json --katı
```

Kapı hata veriyorsa metni düzelt; kuralı esnetme, dedektörü atlama. İstisna gerçekten gerekiyorsa `--kural-kapat K12` ya da `post-kapisi.json` ile seviye ez ve gerekçesini yaz. Uyarılar yayını engellemez ama ilk 210 karakter, hashtag bütçesi ve iddia izi gibi okunma kararını etkileyen kalemlerdir.

## Sık Yapılan Hatalar (Gotchas)

- **Aşırı Düzeltme (Overcorrection) Tuzağı:** Doğal bir Türkçe metinde geçen her `"bir"` kelimesini, her `tarafından`ı veya her devrik cümleyi hata sanma. `"Sen satışa bak"`, `"Site kurmak"`, `"Linki gönder"` gibi doğal ve yerleşik kullanımlara dokunma.
- **Aşırı Sola Dallanma Tuzağı:** İngilizce iskeleti onarırken her bilgiyi tek bir adın önüne sıfat-fiillerle yığma. Okurun yükleme varmadan aklında tutması gereken iç içe yan cümle sayısı ikiyi geçiyorsa cümleyi böl.
- **Öz Türkçecilik Tuzağı:** Bu yetenek yabancı kökenli kelimeleri yasaklayan bir "arı dil" aracı değildir. Günlük ve mesleki Türkçede yaşayan kelimeleri (`performans`, `strateji`, `sistem`, `detay`) zorlama karşılıklarla değiştirme.
- **Sahte Samimiyet:** Kurumsal veya teknik bir metni insanlaştırmak adına metne *"Kahvenizi alın ve arkanıza yaslanın"*, *"Hepimiz oradaydık"* gibi çeviri blog klişeleri ekleme.
- **İkame Kelime Tiki (Replacement Tic) Tuzağı:** "Kritik bir rol oynar" veya "kusursuz bir şekilde" gibi yapay ifadeleri silerken her cümleye refleks olarak "doğrudan", "aslında" veya "ciddi ölçüde" ekleme. Çoğu zaman zarfı tamamen atıp fiili yalnız bırakmak en doğal sonucu verir.
- **Kılık Değiştirmiş Negatif Paralellik Tuzağı:** "Sadece X değil, aynı zamanda Y" kalıbını temizlerken yerine "X ile değil, Y ile" veya "geçici bir X değil, kalıcı bir Y" gibi başka bir negatif paralellik kurma. Olumsuz yarıyı tamamen atıp ne olduğunu söyle.


<!-- KAYNAK: references/sentaks-ve-morfoloji.md -->

# Türkçe Cümle Mimarisi (Sentaks) ve Morfoloji Kılavuzu

İngilizce eğitimli dil modellerinin Türkçe çıktılarındaki temel sorun kelime dağarcığı değil, **cümle iskeletinin İngilizce (sağa dallanan SVO) kalmasıdır**. Bu kılavuz önce Türkçe cümlenin geometrisini, sonra çeviri kokan yapıları bu geometriye göre onarmanın kurallarını anlatır.

**Etiketler:**
- `[Dil bilgisi]`: Uyulmazsa cümle bozulur ya da anlam kayar. Dil bilgisi kaynaklarında tanımlı bir yapıya dayanır.
- `[Üslup]`: Uyulmazsa cümle yanlış olmaz ama çeviri kokar ya da ağırlaşır. Register'a göre esner.

**Gösterim:** Büyük harfler ünlü uyumu ya da ünsüz değişimiyle farklı biçimlere giren sesleri gösterir: `A` = a/e, `I` = ı/i/u/ü, `D` = d/t, `C` = c/ç. Ayraç içindeki `(y)`, ünlüyle biten kök ve gövdelerde araya giren kaynaştırma ünsüzüdür (`oku-y-up`, `gel-ip`).

**Dayanak:** Göksel ve Kerslake, *Turkish: A Comprehensive Grammar* (Routledge, 2005). Erguvanlı-Taylan, *The Function of Word Order in Turkish Grammar* (University of California Press, 1984). Yazım ve noktalama için TDK Yazım Kılavuzu.

## 0. Türkçe Cümlenin Geometrisi

Türkçe **baş sonda** (head-final) bir dildir: Öbeklerde belirleyen önce, belirlenen sonra gelir. İngilizce ise sıfat tamlaması ve `-'s` iyelik yapısı dışında çoğu öbekte (eylem öbeği, edat öbeği, yan cümle) bunun tersini yapar.

| Yapı | Türkçe dizilim | İngilizce dizilim |
| :--- | :--- | :--- |
| Cümle | tümleçler + yüklem (*Raporu gönderdim.*) | özne + yüklem + nesne (*I sent the report.*) |
| Ad tamlaması | tamlayan + tamlanan (*sunucunun belleği*) | *the memory of the server* |
| Niteleme | niteleyici yan cümle + ad (*dün kurduğumuz sunucu*) | *the server that we set up yesterday* |
| Edat öbeği | ad + son çekim edatı (*toplantıdan sonra*) | *after the meeting* |
| Yan cümle | yan cümle + ana yüklem (*Gecikeceğini söyledi.*) | *He said that he would be late.* |

Türkçe cümlenin ağırlık merkezi sondadır. Okur cümleyi soldan sağa kurar ve anlam yüklemle kapanır. İngilizce iskelet ise ana yüklemi erkenden verip ayrıntıyı sağa ekler. Bu kılavuzdaki kuralların hepsi bu farktan doğar.

### 0.1 Öge Dizilimi ve Bilgi Yapısı `[Dil bilgisi]`

Türkçede öge sırası serbest görünür ama her konumun bir görevi vardır:

| Konum | Görevi | Örnek |
| :--- | :--- | :--- |
| Cümle başı | Konu: bilinen, üzerine konuşulan öge, zaman ve yer çerçevesi | ***Bu sürümde** iki hata düzelttik.* |
| Yüklemin hemen önü | Odak: yeni ya da vurgulanan bilgi. Cümle vurgusu buraya düşer. | *Hatayı **Ayşe** buldu.* |
| Yüklemden sonra | Arka plan: bağlamdan zaten bilinen, ikincil bilgi | *Okumuyor kimse **bu raporları**.* |

- **Nötr sıra eğilimi:** özne, zaman, yer, dolaylı tümleç, nesne, yüklem (*Ekip dün toplantıda müşteriye yeni planı sundu.*).
- **Belirtisiz nesne yüklemden ayrılmaz:** Eksiz (belirtisiz) nesne yüklemin hemen önünde durur. *"Ahmet'e rapor gönderdim"* doğal, *"Rapor Ahmet'e gönderdim"* bozuk. Belirtili nesne (`-(y)I` ekli) daha serbesttir: Hem *"Raporu Ahmet'e gönderdim"* hem de *"Ahmet'e raporu gönderdim"* doğrudur, yalnızca vurgu değişir.
- **İngilizce yarık cümle (cleft) kopyası:** İngilizce vurguyu *"It was X that..."* ya da *"What made this possible was X"* ile verir. Türkçede odak yüklem önüne konur:
  - **Makine:** *"Bunu mümkün kılan şey, ekibin deneyimiydi."*
  - **İnsan:** *"Bunu ekibin deneyimi mümkün kıldı."*

### 0.2 Ağırlık: Uzun Öge Önce `[Üslup]`

Türkçede uzun ve ağır ögeler kısa ögelerden önce gelme eğilimindedir. Kısa öge yükleme yakın kalır:

- **Ağır:** *"Ahmet'e geçen hafta müşterilerden gelen bütün şikâyet e-postalarını ilettim."*
- **Dengeli:** *"Geçen hafta müşterilerden gelen bütün şikâyet e-postalarını Ahmet'e ilettim."*

İki cümle de dil bilgisi açısından doğrudur. İkincisinde uzun nesne önce okunup bitirilir, alıcı da yüklem önündeki vurgu konumuna oturur.

### 0.3 Gömme Derinliği: Sola Dallanmanın Sınırı `[Üslup]`

Sola dallanma Türkçenin doğal yönüdür ama sınırsız değildir. Bir adın önüne iç içe sıfat-fiil yan cümleleri yığılırsa okur yüklemi bulana kadar her şeyi aklında tutmak zorunda kalır. İngilizce iskeleti onarmaya çalışırken bu aşırılığa düşmek de yapay bir metin üretir.

- **Aşırı yığılmış:** *"Geçen ay müşterinin şikâyet ettiği hatayı düzelttiğimiz sürümde ortaya çıkan yeni sorunu inceleyen ekip rapor yazdı."*
- **Dengeli:** *"Geçen ay müşterinin şikâyet ettiği hatayı yeni sürümde düzelttik. Bu sürümde çıkan yeni sorunu inceleyen ekip rapor yazdı."*
- **Kural:** Bir ad öbeğinin önünde en fazla bir sıfat-fiil yan cümlesi bulunsun, onun içinde de en fazla bir gömülü yan cümle. Daha fazlası varsa cümleyi böl ya da yan cümlelerden birini ulaçla ana yükleme bağla.

## 1. Dallanma Yönü: Sağa Dallanmadan Sola Dallanmaya

İngilizce niteleyicileri ve yan cümleleri baş ismin sağına dizer (*We built a system that scans and reports data every night*). Dil modeli bu iskeleti Türkçeye iki yoldan taşır: Cümleyi bölüp işaret zamiriyle tekrarlar ya da `ki` ile bağlanan bir yan cümle kurar. Türkçe ise niteleyici yan cümleyi sıfat-fiille baş ismin önüne yerleştirir.

| Kusur Türü | Makine Türkçesi (Sağa Dallanan / Calque) | İnsan Türkçesi (Sola Dallanan Doğal Yapı) |
| :--- | :--- | :--- |
| **Kuyruk Yan Cümle** | Bir sistem kurduk, bu sistem her gece verileri tarayıp raporluyor. | Her gece verileri tarayıp raporlayan bir sistem kurduk. |
| **`ki` ile Kurulan Tümleç Yan Cümlesi** | Görüyoruz ki kullanıcılar bu özelliği kullanmıyor. | Kullanıcıların bu özelliği kullanmadığını görüyoruz. |

- **`öyle ... ki` bir hata değildir.** *"Öyle bir mimari tasarladık ki yüksek trafikte bile gecikme olmuyor."* yerleşik bir Türkçe sonuç yapısıdır ve sıfat-fiile çevrilince vurgu kaybolur. Sorun ancak metinde sık tekrar ederse ortaya çıkar.
- **Sıfat-fiil seçimi `[Dil bilgisi]`:** Nitelenen ad yan cümlenin öznesiyse `-(y)An` kullanılır (*kodu yazan geliştirici*). Nesnesi ya da başka bir ögesiyse `-DIk` veya `-(y)AcAk` ile iyelik eki kullanılır (*geliştiricinin yazdığı kod*, *yarın kuracağımız sunucu*). Bu ikisini karıştırmak cümleyi bozar: *"geliştiricinin yazan kod"* yanlıştır.

## 2. Bağlaç (`ve`) Yerine Ulaç (Zarf-Fiil) Sistemi

İngilizce sıralı eylemleri ve neden-sonuç bağlarını `and`, `and then`, `when`, `as` gibi ayrı kelimelerle bağlar. Türkçe ise **ulaç (zarf-fiil)** ekleriyle (`-(y)Ip`, `-(y)IncA`, `-DIkçA`, `-(y)ArAk`, `-mAdAn`) ve ek eylemin ulacı `-(y)ken` ile iki yüklemi tek akışta birleştirir. `-(y)ken` fiil köküne doğrudan gelmez, zaman ekinden sonra gelir (`ilerle-r-ken`, `çalış-ıyor-ken`).

| İlişki Türü | Makine Türkçesi (Mekanik Bağlaçlı) | İnsan Türkçesi (Ulaçlı Doğal Akış) | Kullanılan Ulaç Eki |
| :--- | :--- | :--- | :--- |
| **Ardışık Eylem** | Veriyi çektik ve sonra temizledik. | Veriyi çekip temizledik. | `-(y)Ip` |
| **Zaman / Tetikleme** | Cache doldu ve istekler yavaşlamaya başladı. | Cache dolunca istekler yavaşlamaya başladı. | `-(y)IncA` |
| **Orantı / Süreç** | Trafik arttı ve buna bağlı olarak hata oranı da yükseldi. | Trafik arttıkça hata oranı da yükseldi. | `-DIkçA` |
| **Yöntem / Araç** | Maliyetleri düşürdük ve bu sayede kârlılığı artırdık. | Maliyetleri düşürerek kârlılığı artırdık. | `-(y)ArAk` |
| **Zıtlık / Eş Zamanlılık** | Birinci grup hızlı ilerler ve ikinci grup geride kalır. | Birinci grup hızlı ilerlerken ikincisi geride kalır. | `-Ar` + `-ken` |

- **Sadakat sınırı `[Dil bilgisi]`:** Ulaç iki olay arasında zaman ya da neden bağı kurar. Kaynakta iki cümle yalnızca yan yana duruyorsa ulaçla bağlayıp yeni bir nedensellik uydurma. Virgülle ya da ayrı cümle olarak bırak.
- **Gizli özne `[Dil bilgisi]`:** Ulaçlı yan cümlenin öznesi söylenmemişse okur onu ana cümlenin öznesi sanar. *"Veriyi çekip sistem çöktü."* cümlesi, veriyi sistemin çektiğini söyler. Özne farklıysa ya açıkça yaz ya da iki cümle kur: *"Veriyi çektik, ardından sistem çöktü."*
- **Olumsuzluk kapsamı `[Dil bilgisi]`:** Ana yüklemdeki olumsuzluk `-(y)Ip` ile bağlanan eyleme de yayılabilir. *"Raporu okuyup onaylamadı."* hem "okudu ama onaylamadı" hem de "ikisini de yapmadı" diye anlaşılabilir. Yalnızca ikinci eylem olumsuzsa açık yaz: *"Raporu okudu ama onaylamadı."*
- **Virgül `[TDK]`:** Ulaçtan sonra virgül konmaz. Yalnızca art arda gelen ulaçlar virgülle ayrılır.

## 3. Ek Eylem (`-DIr`) ve `-mAktAdIr`: İki Ayrı Sorun

Bu iki yapı sık karıştırılır ama farklı yerlerde çalışır, onarımları da farklıdır.

### A. `-mAktAdIr` (eylem çekimi)

`-mAktA` (`-mAk` + `-DA`) resmî üslupta süren eylemi bildirir, bildirme eki `-DIr` ile birleşince *artmaktadır, sağlamaktadır* olur. İngilizce şimdiki ve geniş zamanın resmî Türkçeye refleks çevirisidir.

- Akademik, hukuki ve resmî yazışma dışındaki register'larda `-(I)yor` ya da `-Ar/-Ir` kullan.
- **Makine:** *"Bu yöntem geliştiricilere büyük kolaylık sağlamaktadır."*
- **İnsan:** *"Bu yöntem geliştiricilerin işini kolaylaştırıyor."*

### B. Ad cümlesinde bildirme eki `-DIr`

Ad soylu yüklemde `-DIr` ek eylemin bildirme ekidir (*Bu yöntem etkilidir.*). Fiildeki `-mAktAdIr` gibi `-Ar/-Ir` ya da `-(I)yor` ile değiştirilemez. İki seçenek vardır: eki korumak ya da düşürmek.

- **Tanım ve sınıflandırma cümlelerinde korunur:** *"Redis bir anahtar-değer veri tabanıdır."* Ek düşerse (*"Redis bir anahtar-değer veri tabanı."*) cümle yanlış olmaz ama konuşma diline kayar. Belge ve kılavuz metninde ek kalsın.
- **Anlatı ve sohbet akışında seyreltilir:** Art arda her ad cümlesini `-DIr` ile bitirmek metni ders kitabına çevirir.
  - **Makine:** *"Bu yöntem oldukça etkilidir. Burası sistemin en kritik parçasıdır."*
  - **İnsan (blog):** *"Bu yöntem oldukça etkili. Burası da sistemin en kritik parçası."*
- **Anlam farkı:** Konuşma dilinde `-DIr` tahmin de bildirir. Bu kullanım ad soylu yükleme de çekimli fiile de gelir (*"Şimdi evdedir."*, *"Yorulmuştur."*). Gündelik metne eklenen her `-DIr` cümleye ya resmîlik ya da belirsizlik katar.

### C. Grup çekimi (ek eksiltme) `[Üslup]`

Aynı eki alan sıralı yüklemlerde Türkçe eki yalnızca sonuncuya getirir. Eki her yüklemde tekrarlamak İngilizce `is ... and is` dizilişinin kopyasıdır.

- **Makine:** *"Bu yöntem hızlıdır ve güvenilirdir."*
- **İnsan:** *"Bu yöntem hızlı ve güvenilirdir."*

### D. Doz

Akademik register'da `-mAktAdIr` ve `-DIr` korunur, sorun eklerin kendisi değil tekrarıdır. Art arda üç cümleyi aynı ekle (`-mektedir`, `-mıştır`, `-dır`) bitirme, geniş zaman (`-Ar/-Ir`) ve `-mIştIr` ile nöbetleşe kullan. Başlangıç hedefi olarak 100 kelimede yaklaşık 0,5-2,5 `-mAktAdIr` kullanılabilir. **Bu aralık bir derlem ölçümüne dayanmaz**, dedektörün `--register` seçeneğiyle değiştirilebilen varsayılan değeridir. Kesin eşik gibi kullanma.

## 4. Vurgu Yuvası (Yüklem Önü) ve Devrik Cümle

İngilizce sabit dizilimde vurguyu cümleyi yararak (*It is X that...*) ya da kelimeyi **kalın** yazarak verir. Dil modeli bunu Türkçeye *"İşte tam da bu noktada..."*, *"Asıl önemli olan şey şudur ki..."* gibi dolgu kalıplarıyla taşır.

Türkçede vurgu yüklemin hemen önündeki ögeye düşer. Aynı ögeleri yeniden dizmek yeterlidir:

- *"Raporu dün **Ahmet'e** gönderdim."* (Kime gönderildiği öne çıkıyor.)
- *"Raporu dün Ahmet'e **ben** gönderdim."* (Gönderenin kim olduğu öne çıkıyor.)
- *"Raporu Ahmet'e **dün** gönderdim."* (Ne zaman gönderildiği öne çıkıyor.)
- *"Dün Ahmet'e **raporu** gönderdim."* (Neyin gönderildiği öne çıkıyor.)

### Devrik Cümle

Yüklemden sonraki konum, bağlamdan bilinen ve ikinci planda kalan bilgiye ayrılmıştır. Gündelik, edebî ve blog Türkçesinde yüklemi öne almak metne konuşma sıcaklığı katar:

- **Düz:** *"Kimse bu uzun hata raporlarını sonuna kadar okumuyor."*
- **Devrik (blog):** *"Kimse sonuna kadar okumuyor bu uzun hata raporlarını."* (Raporlar bağlamda zaten geçtiği için yüklemden sonraya alınabilir.)
- **Sınır `[Dil bilgisi]`:** Yeni bilgi ve belirtisiz nesne yüklemden sonraya alınmaz. *"Ahmet'e gönderdim rapor."* bozuk bir cümledir.
- **Kota `[Üslup]`:** Teknik, kurumsal ve akademik register'larda devrik cümle kullanma. Blog/deneme register'ında devrik cümleyi seyrek tut, her cümleyi devrik yapmak yeni bir yapay tike dönüşür. 400 kelimede 2-3 devrik cümle yol gösterici bir tahmindir, ölçülmüş bir eşik değildir.

## 5. Zamir Düşürme (Pro-Drop) ve `"Bir"` / `"Kendi"` Yoğunluğu

### A. Kişi ve İşaret Zamiri Düşürme

Türkçe özneyi yüklemdeki kişi ekiyle (`-(y)Im/-m`, `-sIn/-n`, `-(y)Iz/-k`, `-sInIz/-nIz`, `-lAr`), aitliği iyelik ekiyle zaten bildirir. İngilizcedeki zorunlu `I, we, they, it, this` zamirlerini her cümleye taşımak metni ağırlaştırır:

- **Makine:** *"Biz önce veri tabanını yedekledik, sonra biz migration script'ini çalıştırdık. O sorunsuz tamamlandı."*
- **İnsan:** *"Önce veri tabanını yedekledik, ardından migration script'ini çalıştırdık. İşlem sorunsuz tamamlandı."*
- **Anlam `[Dil bilgisi]`:** Türkçede açıkça söylenen özne zamiri karşıtlık ya da vurgu bildirir. *"Ben gittim."* cümlesi "başkası değil, ben" anlamına kayar. Bu yüzden gereksiz zamir yalnızca ağırlık değil, istenmeyen bir vurgu da ekler.

### B. `"Bir"` Yoğunluğu

Sıfat ile ad arasındaki `bir`, Türkçenin kendi belirsizlik işaretidir: *güzel bir gün*, *iyi bir insan*, *derin bir iz bıraktı* doğal Türkçedir. Sorun tek tek kullanımlar değil, **yoğunluktur**. Dil modeli her sıfat tamlamasına İngilizce `a/an` karşılığı olarak `bir` ekler:

- **Makine:** *"Bu güncelleme **büyük bir önem** taşıyor ve **yüksek bir performans** ile **iyi bir kullanıcı deneyimi** sunuyor."*
- **İnsan:** *"Bu güncelleme **büyük önem** taşıyor, **yüksek performans** ve **iyi kullanıcı deneyimi** sunuyor."* (Pazarlama dili kaynağın kendi içeriğidir. Bu örnekte onarılan yalnızca `bir` yoğunluğudur.)
- **Kural `[Üslup]`:** Önce kalıplaşmış birleşik eylemlerin içindeki `bir`i at (*önem taşımak*, *artış göstermek*, *rol oynamak*). Bir cümlede birden fazla *sıfat + bir + soyut ad* varsa seyrelt. Tekil ve somut bir olayı anlatan `bir`e dokunma.

### C. İngilizce `his/her/its own` Çevirisi Olan Gereksiz `"Kendi"`

- **Makine:** *"Her servis **kendi veri tabanına** bağlanır ve **onun kendi** yapılandırmasını okur."*
- **İnsan:** *"Her servis kendi veri tabanına bağlanıp yapılandırmasını okur."* (İyelik eki `-(s)I` zaten aitliği verir. Karşıtlık yoksa `kendi` tekrarlanmaz.)

## 6. Edilgen Çatı (`tarafından`), Adlaştırma ve Kof Yardımcı Fiil

### A. `"tarafından"`

Edilgen çatı Türkçenin kendi yapısıdır ve bilgi yapısını taşır. *"Köprü Mimar Sinan tarafından yapıldı."* kusursuz bir cümledir: Konu köprüdür, yeni bilgi Mimar Sinan'dır. Etkene çevirmek konuyu değiştirir. Çeviri kokusu iki durumda ortaya çıkar:

1. Eyleyen yazarın kendisi ya da kendi kurumu olduğunda:
   - **Makine:** *"Yeni kimlik doğrulama modülü güvenlik ekibimiz tarafından test edilmiş ve onaylanmıştır."*
   - **İnsan:** *"Güvenlik ekibimiz yeni kimlik doğrulama modülünü test edip onayladı."*
2. `tarafından` kof bir eylemle birlikte geldiğinde (*tarafından gerçekleştirilmiştir*, *tarafından sağlanmaktadır*).

### B. Adlaştırma Zincirleri `[Üslup]`

Dil modeli eylemi ada çevirip ardından bir yardımcı eylemle yeniden eyleme bağlar: *"-mAsI gerekmektedir"*, *"-mAsI sağlanmalıdır"*, *"-mAsI önem arz etmektedir"*. Türkçede eylem çoğu zaman doğrudan çekimlenebilir:

- **Makine:** *"Verilerin düzenli olarak yedeklenmesinin sağlanması gerekmektedir."*
- **İnsan:** *"Veriler düzenli olarak yedeklenmeli."*

### C. Kof Yardımcı Fiiller

Tek eylemle söylenebilecek işler ad + yardımcı eylem öbekleriyle şişirilir. Bu öbeklerin çoğu Türkçede yerleşiktir, sorun **sıklık** ve `-mAktAdIr` ile birlikte kullanımdır:

| Şişirilmiş Öbek | Doğal Seçenek | Örnek Dönüşüm |
| :--- | :--- | :--- |
| **gerçekleştirmek / icra etmek** | yapmak, düzenlemek, kurmak, tamamlamak | *"Toplantı gerçekleştirdik"* -> *"Toplantı yaptık"* / *"Analiz gerçekleştirdi"* -> *"Analiz etti"* |
| **sağlamak** (aşırı kullanım) | vermek, kazandırmak, doğrudan oldurgan ya da ettirgen çatı (`-DIr`, `-t`) | *"Hız artışı sağlar"* -> *"Sistemi hızlandırır"* / *"Destek sağlar"* -> *"Destek verir"* |
| **katkıda bulunmak** (aşırı kullanım) | desteklemek, yararı dokunmak | *"Büyümesine katkıda bulunmaktadır"* -> *"Büyümesini destekliyor"*. `Katkıda bulunmak` TDK Güncel Türkçe Sözlük'te yer alan yerleşik bir deyimdir. Onun yerine sözlükte yer almayan `katkı sunmak` önerme. |
| **sahip olmak** (`have / has` çevirisi) | `-lI` eki, `var`, `içermek`, `taşımak` | *"Yüksek hıza sahiptir"* -> *"Çok hızlıdır"* / *"Üç katmana sahiptir"* -> *"Üç katmandan oluşur"* |
| **ev sahipliği yapmak** (`host / feature`) | barındırmak, yer almak | *"Bölge birçok tarihî yapıya ev sahipliği yapmaktadır"* -> *"Bölgede pek çok tarihî yapı var"* |
| **rol oynamak** (`play a role`) | belirlemek, etkilemek | *"Kritik bir rol oynamaktadır"* -> *"Sonucu belirler"* |
| **yer almak / bulunmak** (`-mAktAdIr` ile) | `var`, bulunma eki `-DA` | *"Raporda üç bölüm yer almaktadır"* -> *"Raporda üç bölüm var"* |
| **olan** (gereksiz sıfat-fiil) | `olan`ı düşür | *"Önemli olan bir adım"* -> *"Önemli bir adım"* |
| **olarak** (zincirleme kullanım) | `-DA`, `-CA` veya doğrudan yüklem | *"İlk adım olarak veriyi sildik"* -> *"İlk adımda veriyi sildik"*. *"Sonuç olarak"* resmî metinde olağandır. Hedef, her paragrafın sonuna refleksle eklenen özet etiketidir. |

## 7. Kanıtsallık (`-mIş`) ve Zaman Seçimi

- **Görülen ve öğrenilen geçmiş (`-DI` ve `-mIş`):** Türkçe, olayı görüp görmediğini fiil çekiminde ayırır. İngilizce bunu yapmaz (*The server crashed at 3 AM*). Dil modeli bu yüzden neredeyse hiç `-mIş` kullanmaz. Olay sonradan öğrenilmiş ya da kayıttan çıkarılmışsa, özellikle gündelik ve blog register'ında `-mIş` doğaldır:
  - **Düz anlatım:** *"Gece yarısı bellek sızıntısı oldu ve servis kapandı. Sabah log'lara baktığımızda fark ettik."*
  - **Kanıtsal anlatım:** *"Gece yarısı bellek sızıntısı olmuş, servis de kapanmış. Sabah log'lara bakınca fark ettik."*
  - **Sınır `[Üslup]`:** Olay sonrası raporlarında ve resmî tutanaklarda, kayıtla kesinleşmiş olgu için `-DI` olağandır. `-mIş` ekini zorla yayma.
- **Geniş zaman (`-Ar/-Ir`) ve şimdiki zaman (`-(I)yor`):** Genel doğrular için ikisi de doğal Türkçedir (*"Dünya Güneş'in çevresinde dönüyor."*). Geniş zaman daha tanımsal ve resmî bir ton verir.
  - **Teknik tanım ve şartnamede** geniş zamanı tercih et: *"Redis veriyi bellekte tutar, diske ise asenkron yazar."*
  - **Kural `[Üslup]`:** Aynı paragrafta aynı türden bilgiyi anlatırken ikisini karıştırma.

## 8. Ad Tamlaması Zincirlerini Kırma `[Üslup]`

İngilizce teknik ve kurumsal ad öbeklerini (*customer segmentation module performance optimization process*) Türkçeye belirtisiz ad tamlamalarıyla üst üste zincirleyerek aktarmak okunabilirliği yok eder. Tamlayan eki almadan art arda dizilen adların sayısı üçü geçmesin, fazlasını sıfat-fiil ya da hâl ekleriyle çöz:

- **Makine:** *"Müşteri segmentasyon modülü performans iyileştirme çalışması sonuç raporu"*
- **İnsan:** *"Müşteri segmentasyon modülünün performansını iyileştirme çalışmasının sonuç raporu"* (Kaynakta çalışmayı kimin yaptığı yazmıyor, bu yüzden "yaptığımız" gibi bir özne eklenmez.)

## 9. Cümleler Arası Bağlantı

### A. `"Bu da ... anlamına gelir"` Kalıbı `[Üslup]`

İngilizcedeki *which means* ve *this means that* yapıları Türkçeye cümle başında `Bu da` ile başlayan ikinci bir cümle olarak taşınır. Bağlantı çoğu zaman tek cümlede kurulabilir:

- **Makine:** *"Cache süresi kısa tutuldu. Bu da veri tabanı yükünün artması anlamına geliyor."*
- **İnsan:** *"Cache süresi kısa tutulduğu için veri tabanı yükü artıyor."*

### B. Öz Düzeltme ve Söylem Parçacıkları

Makine Türkçesi her şeyi baştan mutlak bir kesinlikle biliyormuş gibi yazar. İnsan yazar düşünürken cümleyi daraltır, çekince koyar ve Türkçenin söylem parçacıklarını (`ise`, `zaten`, `de`, `yani`, `bir de`, `tabii`, `daha doğrusu`) yerli yerinde kullanır:

- **Makine:** *"Silme işlemi idempotenttir, bu nedenle dağıtık sistemlerde tercih edilir."*
- **İnsan:** *"Silme işlemi idempotent. Dağıtık sistemlerde tercih edilmesinin nedeni de bu."* (Parçacık ve cümle bölme ritmi değiştirir ama kaynağa yeni bir iddia eklemez.)
- **Makine:** *"Birinci yöntem hızlıdır, ikinci yöntem yavaştır."*
- **İnsan:** *"Birinci yöntem hızlı, ikincisi ise yavaş."*
- **Sınır `[Üslup]`:** Her parçacık silme testinden geçmeli. Kaldırıldığında anlamdan ya da tondan bir şey eksilmiyorsa o parçacık süstür, silinir.


<!-- KAYNAK: references/ai-turkcesi-sozlugu.md -->

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


<!-- KAYNAK: references/tdk-ve-noktalama.md -->

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


<!-- KAYNAK: references/register-ve-ornekler.md -->

# Register (Bağlam) Profilleri ve Uçtan Uca Dönüşüm Örnekleri

Doğal Türkçe tek bir kalıptan oluşmaz. Bir sözleşmedeki devrik cümle özensizlik, bir blog yazısındaki `-mAktAdIr` eki ise robotluk üretir. Bu dosya, metin türlerine göre 9 üslup boyutunun nasıl kalibre edileceğini ve uçtan uca (Before / After) dönüşüm örneklerini içerir.

## 1. Dokuz Boyutlu Register ve Üslup Matrisi

Kullanıcı özel bir yazar örneği (few-shot) vermediğinde aşağıdaki 5 profilden uygun olanı seç:

| Boyut | 1. Blog / Deneme / Sosyal Medya | 2. Teknik / Mühendislik | 3. Kurumsal / SaaS / İş İletişimi | 4. Akademik / Resmî / Hukuki | 5. Edebî / Anlatı |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Anlatıcı Kimliği** | Masanın karşısından anlatan deneyimli dost | Gece 2'de o hatayı çözmüş kıdemli mühendis | Müşteriye bizzat yazan net ve dürüst kurucu | Konuya hâkim, soğukkanlı araştırmacı/uzman | Düşüncesini yazarken inşa eden usta yazar |
| **Hitap** | Sen veya Siz (tutarlı) | Sen veya nötr 2. çoğul | Siz | 3. şahıs / nötr | Bağlama göre 1. veya 3. şahıs |
| **Cümle Uzunluğu & Burstiness** | Yüksek dalgalanma (4 kelime ile 28 kelime bir arada) | Orta-Yüksek (Kısa net yargılar + ulaçlı açıklamalar) | Orta (10-20 kelime, net ve taranabilir) | Orta-Uzun (15-30 kelime, sola dallanan yan cümleler) | Çok yüksek dalgalanma (nefes ritmine odaklı) |
| **Cümlecik Bağlama** | Ulaçlar (`-Ip, -IncA`) + nokta/virgül | Ulaçlar (`-Ip, -dIkçA, -ArAk`) + iki nokta | Ulaçlar + net sebep-sonuç bağlaçları | Sıfat-fiiller (`-An, -DIk`) + ulaçlar | Ulaçlar + ritmik tekrarlar ve virgül |
| **Kip Dağılımı** | `-yor`, `-DI`, `-mIş` (delil), geniş zaman | Geniş zaman (`-Ir/-Ar` kurallar için), `-DI`, `-mIş` | Geniş zaman, `-yor`, `-DI` | Geniş zaman, `-mAktAdIr` (100 kelimede yaklaşık 0,5-2,5), `-DIr` | Tüm kipler serbest |
| **Söylem Parçacıkları** | `işte, zaten, ise, hani, tabii, daha doğrusu` | `ise, aslında, daha doğrusu, örneğin` | `ise, özellikle, doğrudan` | Yalnızca `ise, nitekim, dolayısıyla` | Doğal akışa göre serbest |
| **Devrik Cümle Oranı** | 400 kelimede 2-3 adet | Sıfır (0) | Sıfır (0) | Sıfır (0) | Anlatı ritmine göre doğal |
| **Terim Tercihi** | Günlük karşılıklar veya okunuşa göre çekimli terim | Yerleşik İngilizce terim olduğu gibi (`endpoint'e`) | Sektör standardı, jargonsuz sade Türkçe | TDK ve alan terimleri (`veri tabanı, alan yazını`) | Türkçe duygu ve imge değeri yüksek sözcükler |
| **Açılış Hamlesi** | Sahne, somut gözlem veya doğrudan soru | Doğrudan problem veya mimari karar | Temel değer önermesi veya ana mesaj | Araştırma problemi veya olgusal çerçeve | Atmosfer, detay veya iç ses |

## 2. Aynı İddianın 4 Farklı Register'daki Doğal Yazımı

- **Ham AI Çıktısı (Makine Türkçesi):**
  > *"Cache stratejisinin doğru bir şekilde belirlenmesi, sistem performansı açısından kritik bir öneme sahiptir ve gecikme sürelerinin azaltılmasında yadsınamaz bir rol oynamaktadır."*
- **Akademik / Resmî Register:**
  > *"Önbellekleme stratejisinin doğru belirlenmesi, sistem performansını ve yanıt sürelerini belirlemektedir."*
- **Teknik / Mühendislik Register:**
  > *"Cache stratejisini doğru kurmak performansı artırır ve gecikmeyi düşürür."*
- **Kurumsal / Ürün Register:**
  > *"Doğru önbellek stratejisi, sisteminizi hızlandırırken yanıt sürelerini kısaltır."*
- **Blog / Deneme Register:**
  > *"Performansı belirleyen şeylerden biri cache stratejisi. Doğru kurarsanız gecikme de azalıyor."*
  >
  > (Kaynak "yarı yarıya", "%40" gibi bir miktar vermediği için çıktı da vermez.)

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
> Uzaktan çalışma artık şirket kültürünün kalıcı bir parçası. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik artıyor. İşin zor kısmı, ekip aynı ofisi paylaşmazken iletişimi koparmamak. Kalıcı çözüm ise çalışma düzenini baştan sona bu yeni ritme göre kurmak.

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
> ## Cache stampede sorunu ve çözümü
> Bir `cache` anahtarının süresi dolduğu anda gelen istekler hep birlikte veritabanına yönelip darboğaz oluşturur. Bu sorun özellikle yüksek trafikli `endpoint`'lerde önem kazanır. Dağıtık kilit (`distributed lock`) kullanabilirsiniz ama bu yöntem gecikmeyi artırabilir.

**Sadakat notu:** Kaynak "birçok istek" diyor, çıktı "yüzlerce" demez. Kaynak "artırabilir" diyor, çıktı ihtiyatı silip "artırır" demez. Kaynakta "kesinti" veya "kilitlenme" yok, çıktı bunları eklemez. Terim tutarlılığı için başlıkta ve gövdede aynı terim (`cache`) kullanılır.

### Örnek 3: Akademik / Analitik Metin (Olgusal Sadakat ve Dozaj Korunarak)

**Önce (Tipik AI Türkçesi):**
> Türkiye'de 2020-2024 yılları arasında yenilenebilir enerji yatırımları sadece artış göstermekle kalmamış, aynı zamanda enerji arz güvenliğinde de çığır açan bir dönüm noktası olmuştur. Enerji Bakanlığı tarafından paylaşılan verilere göre, güneş enerjisi kurulu gücü %112 oranında bir büyüme gerçekleştirmiştir ki bu durum sektörün dinamik yapısının en büyük kanıtıdır.

**Sonra (Doğal İnsan Türkçesi - Akademik Register):**
> Türkiye'de 2020-2024 döneminde hız kazanan yenilenebilir enerji yatırımları, enerji arz güvenliğinin yapısını da dönüştürmüştür. Enerji Bakanlığının verilerine göre güneş enerjisi kurulu gücü bu dönemde %112 büyümüştür.


<!-- KAYNAK: references/sosyal-medya.md -->

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
