# Katkıda Bulunma Rehberi (CONTRIBUTING.md)

`turkish-anti-ai-skill` projesine katkıda bulunmak istediğin için teşekkürler! Bu projenin temel ilkesi, "bence bu kelime güzel değil" gibi öznel yargılar yerine, **Büyük Dil Modellerinin (LLM) Türkçe çıktılarında istatistiksel olarak aşırı temsil edilen kalıpları, İngilizce sözdizimsel kopyaları (calque/translationese) ve TDK Yazım Kılavuzu kurallarını** kanıta dayalı olarak belgelemektir.

## 1. Yeni Bir "Yapay Zekâ Türkçesi" Kalıbı Ekleme Kuralları

Yeni bir kelime, bağlaç veya cümle yapısı için Pull Request (PR) veya Issue açarken lütfen aşağıdaki şablonu doldur:

- **Kalıp / Kelime Adı:** (Örn: *"potansiyelini ortaya çıkarmak"*)
- **İngilizce Kaynak Kalıp (Calque):** (Örn: *"unlock the potential"*)
- **Şiddet Derecesi (Severity):**
  - `P0 / Tier-1`: Tek görülmede dahi kesin AI ifşası olan kalıplar.
  - `P1 / Sentaks`: İngilizce cümle iskeletinin Türkçeye kopyalanması.
  - `P2 / Tier-2 & TDK`: Yoğunlukta yapay duran bağlaçlar veya TDK noktalama/imla hataları.
- **Önce (Makine Türkçesi Örneği):** Kalıbın gerçek bir LLM çıktısındaki doğal olmayan kullanımı.
- **Sonra (İnsan Türkçesi Örneği):** Olgusal sadakati bozmadan onarılmış doğal Türkçe karşılığı.
- **İstisna / Sınır Durumu (Do-Not-Flag):** Bu kuralın hangi register'da veya bağlamda **uygulanmaması** gerektiği (Örn: `-mAktAdIr` eki akademik/resmî register'da korunur).
- **Kural Türü:** `[TDK]`, `[Dil bilgisi]` veya `[Üslup]`. Cümle yapısı kurallarında `[Dil bilgisi]` etiketi yalnızca uyulmadığında cümlenin bozulduğu ya da anlamın kaydığı durumlar içindir, dayanağını göster (bkz. `references/sentaks-ve-morfoloji.md` başındaki kaynaklar). Bir kuralı `[TDK]` diye etiketlemek için TDK Yazım Kılavuzu'ndaki ([yazim.tdk.gov.tr](https://yazim.tdk.gov.tr/index.html)) veya Güncel Türkçe Sözlük'teki ([sozluk.gov.tr](https://sozluk.gov.tr/)) ilgili maddeyi bağlantısıyla göster. Kılavuzda karşılığı olmayan kurallar `[Üslup]` olarak eklenir ve dedektörde "TDK hatası" diye raporlanmaz.

## 2. Paket Senkronizasyonu ve Doğrulama

`SKILL.md` veya `references/*.md` dosyalarında değişiklik yaptıktan sonra PR açmadan önce şu iki komutu çalıştır:

```bash
# 1. Tek parça dist/ dosyasını ve skills/ alt paketini güncelle
python3 scripts/build_dist.py

# 2. Paket bütünlüğünü, dedektör kurallarını ve eval senaryolarını doğrula
python3 scripts/run_tests.py
```

`run_tests.py` üç bölüm koşar: paket bütünlüğü, dedektör kural testleri, `evals/evals.json` senaryoları. Raporu `docs/TEST_VE_DOGRULAMA_RAPORU.txt` dosyasına kendisi yazar; **rapor elle düzenlenmez**, bayatladığı için üretimi otomatikleştirildi. Aynı komut CI'da da koşar ve depodaki rapor güncel değilse CI kırmızıya döner. Kodu değiştirdiysen raporu da commit et.

Dedektör davranışını (yeni kalıp, register istisnası, eşik) değiştirdiğinde `scripts/run_tests.py` içindeki “Dedektör kural testleri” bölümüne o davranışı sabitleyen bir kontrol ekle. Kural gevşetip test eşiğini düşürerek yeşil elde etme: eşiği düşürdüysen nedenini PR açıklamasında yaz.

## 3. Olgusal Sadakat İlkemiz

Test ve örnek (`evals/evals.json` ve `references/register-ve-ornekler.md`) eklerken "Sonra (After)" metinlerinde kaynak metinde bulunmayan hiçbir yeni sayı, tarih, özel isim veya kişisel anekdot eklenmediğinden emin ol. Miktar ve kesinlik de bilgidir: Kaynak "birçok" diyorsa "yüzlerce", "artırabilir" diyorsa "artırır" yazma. Klişeyi silince somut bilgi gerekiyorsa ve kaynakta yoksa `[somut veri: ...]` yer tutucusunu kullan.

Bu kural artık denetleniyor: `run_tests.py`, her eval senaryosunun çıktısında kaynakta olmayan sayı, miktar/abartı sözü (`yüzlerce`, `binlerce`, `bütün`, `herkes`...) veya senaryoda `must_not_add` ile yasaklanmış ifade arar; `must_preserve_hedges` ile ihtiyat kiplerinin korunmasını ister. Yeni bir senaryo eklerken bu alanları doldur.
