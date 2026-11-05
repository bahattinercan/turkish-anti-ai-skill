# Katkıda Bulunma Rehberi (CONTRIBUTING.md)

`turkish-anti-ai-skill` projesine katkıda bulunmak istediğin için teşekkürler! Bu projenin temel ilkesi, "bence bu kelime güzel değil" gibi öznel yargılar yerine, **Büyük Dil Modellerinin (LLM) Türkçe çıktılarında istatistiksel olarak aşırı temsil edilen kalıpları, İngilizce sözdizimsel kopyaları (calque/translationese) ve TDK Yazım Kılavuzu kurallarını** kanıta dayalı olarak belgelemektir.

## 1. Yeni Bir "Yapay Zeka Türkçesi" Kalıbı Ekleme Kuralları

Yeni bir kelime, bağlaç veya cümle yapısı için Pull Request (PR) veya Issue açarken lütfen aşağıdaki şablonu doldur:

- **Kalıp / Kelime Adı:** (Örn: *"potansiyelini ortaya çıkarmak"*)
- **İngilizce Kaynak Kalıp (Calque):** (Örn: *"unlock the potential"*)
- **Şiddet Derecesi (Severity):**
  - `P0 / Tier-1`: Tek görülmede dahi kesin AI ifşası olan kalıplar.
  - `P1 / Sentaks`: İngilizce cümle iskeletinin Türkçeye kopyalanması.
  - `P2 / Tier-2 & TDK`: Yoğunlukta yapay duran bağlaçlar veya TDK noktalama/imla hataları.
- **Önce (Makine Türkçesi Örneği):** Kalıbın gerçek bir LLM çıktısındaki doğal olmayan kullanımı.
- **Sonra (İnsan Türkçesi Örneği):** Olgusal sadakati bozmadan onarılmış doğal Türkçe karşılığı.
- **İstisna / Sınır Durumu (Do-Not-Flag):** Bu kuralın hangi register'da veya bağlamda **uygulanmaması** gerektiği (Örn: `-mAktAdIr` eki akademik/resmi register'da korunur).

## 2. Paket Senkronizasyonu ve Doğrulama

`SKILL.md` veya `references/*.md` dosyalarında değişiklik yaptıktan sonra PR açmadan önce şu iki komutu çalıştır:

```bash
# 1. Tek parça dist/ dosyasını ve skills/ alt paketini güncelle
python3 scripts/build_dist.py

# 2. Dedektör betiğinin sorunsuz çalıştığını doğrula
python3 scripts/detect_tr_ai.py README.md
```

## 3. Olgusal Sadakat İlkemiz

Test ve örnek (`evals/evals.json` ve `references/register-ve-ornekler.md`) eklerken "Sonra (After)" metinlerinde kaynak metinde bulunmayan hiçbir yeni sayı, tarih, özel isim veya kişisel anekdot eklenmediğinden emin ol.
