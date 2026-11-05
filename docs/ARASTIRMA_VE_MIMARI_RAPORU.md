# Türkçe Dilbilimi, TDK Yazım Kılavuzu ve Anti-AI Mimarisi Araştırma Raporu

Bu rapor, `turkish-anti-ai-skill` açık kaynak projesinin kuramsal ve pratik temelini oluşturmak üzere yürütülen üç sütunlu araştırmanın (Türkçe Dilbilimi & TDK, Küresel Humanizer Mimarileri ve GitHub Agent Skills Standartları) bulgularını içerir.

## 1. İngilizce Eğitimli Modellerin Türkçedeki Yapısal Kusurları (Translationese)

Büyük dil modelleri (LLM), İngilizce ağırlıklı eğitim verisi ve RLHF süreçleri nedeniyle Türkçe metin üretirken kelimeleri Türkçe seçse de cümle mimarisini İngilizce (Sağa Dallanan SVO) olarak kurar. Doğal Türkçe ise **sondan eklemeli (agglutinative)** ve **sola dallanan (left-branching)** bir dildir:

1. **Dallanma Yönü (Branching Direction):** İngilizcede yan cümleler baş ismin sağına takılır (*"We built a system that scans data"*). Model bunu Türkçeye *"Bir sistem kurduk, bu sistem verileri tarıyor"* veya Hint-Avrupa tipi `ki` bağlacıyla (*"Öyle bir sistem kurduk ki..."*) taşır. Doğal Türkçede yan cümle sıfat-fiil (`-An, -DIk, -AcAk`) alarak baş ismin soluna yerleşir: *"Verileri tarayan bir sistem kurduk."*
2. **Bağlaç (`ve`) vs. Ulaç (Zarf-Fiil) Sistemi:** İngilizce sıralı eylemleri `and`, `then`, `when`, `as` bağlaçlarıyla birleştirir. Doğal Türkçe ise iki yüklem arasındaki ilişkiyi ulaç ekleriyle (`-Ip, -IncA, -dIkçA, -ArAk, -mAdAn`) kaynaştırır (*"Veriyi çekip işledik"*, *"Cache dolunca istekler yavaşladı"*).
3. **Koşulaç (`is/are`) ve `-DIr / -mAktAdIr` Salgını:** İngilizce geniş zaman isim cümlesindeki zorunlu `is/are` koşulacı, Türkçe model çıktılarında her cümlenin `-DIr` veya `-mAktAdIr` ile bitmesine yol açar. Oysa Türkçede geniş zaman isim cümlesinde koşulaç sıfırdır; akademik/resmi register dışında bu ekler silinir.
4. **Vurgu Yuvası (Pre-Verbal Focus) ve Devrik Cümle Ritmi:** Türkçede vurgu kalın yazıyla veya *"İşte tam da bu noktada"* dolgusuyla değil, vurgulanacak öğenin **yüklemin hemen önündeki yuvaya** çekilmesiyle kurulur.
5. **Özne Düşürme (Pro-Drop) ve Gereksiz `"Bir"` / `"Kendi"` Kullanımı:** Yüklemdeki şahıs eki özneyi zaten taşıdığından gereksiz zamirler (`ben, biz, o`) ve İngilizce `a/an` çevirisi olan soyut isim önündeki `"bir"` sıfatları (*"büyük bir önem"* -> *"büyük önem"*) temizlenir.
6. **Edilgen Çatı (`tarafından`) ve Kof Yardımcı Fiiller:** *"Ekibimiz tarafından gerçekleştirilmiştir"* gibi edilgen ve şişirilmiş yardımcı fiil öbekleri (`gerçekleştirmek, sağlamak, katkıda bulunmak, sahip olmak, ev sahipliği yapmak`) doğrudan Türkçe eylem fiillerine dönüştürülür.
7. **Kanıtsallık Kipi (`-mIş`):** Görgü tanıklığı olmayan, log kaydından okunan veya sonradan fark edilen olaylarda kesin geçmiş zaman (`-DI`) yerine Türkçenin delil kipi (`-mIş`) kullanılır.

## 2. Küresel ve Yerel Anti-AI / Humanizer Mimarilerinin Karşılaştırması

| Proje / Kaynak | Temel Yaklaşım | `turkish-anti-ai-skill` İçine Alınan Mimari Prensip |
| :--- | :--- | :--- |
| [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | İçerik şişirme, negatif paralellikler ve yüzeysel `-ing` analizlerinin taksonomisi | Katman 1 (P0) kompozisyon ve retorik kalıp yasakları |
| [blader/humanizer](https://github.com/blader/humanizer) | 25 kural, şiddet ağırlıklandırması ve `Mark -> Draft -> Audit` döngüsü | 4 adımlı iş akışı ve tek görülmede vs. yoğunlukta tetiklenen kural hiyerarşisi |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | Tier 1/2/3 kelime tabloları, `rewrite / detect / edit` modları ve `dist/` derlemesi | 3 katmanlı sözlük, çalışma modları ve çoklu ajan (`dist/` + `.mdc`) paketlemesi |
| [durmazoguzhan/turkish-humanify](https://github.com/durmazoguzhan/turkish-humanify) | Türkçe cümle mimarisi, register dozajı, fonetik ek uyumu ve Olgusal Sadakat Kilidi | Sola dallanma, ulaç sistemi, 5 register kalibrasyonu ve Anti-Fabrication Lock |
| [oguzhankayan/turkish-native](https://github.com/oguzhankayan/turkish-native) | SaaS/UI lokalizasyon kalıpları ve aşırı düzeltmeyi (overcorrection) önleme | Tier-3 SaaS/ürün tablosu ve doğal Türkçe ifadeleri koruma (*Gotchas*) |
| [bushrabeg/turkce-humanizer](https://github.com/bushrabeg/turkce-humanizer) | TDK noktalama referansı ve 5 mutlak noktalama/bağlaç yasağı | Katman 3 Beş Mutlak Noktalama Yasağı ve yazar profili kalibrasyonu |

## 3. Agent Skills (`SKILL.md`) ve Çoklu Ajan Uyumluluk Standartları

- **Progressive Disclosure (Aşamalı Yükleme):** [Agent Skills Spesifikasyonu](https://agentskills.io/specification) uyarınca `SKILL.md` dosyası 500 satırın altında tutularak yalnızca iş akışını yönetir; detaylı dilbilimi ve TDK tabloları `references/` altından ihtiyaç anında okunur.
- **Evrensel Kurulum (`npx skills` & `gh skill`):** Hem kök dizinde `SKILL.md` hem de `skills/turkish-anti-ai-skill/` paket dizini bulundurularak [Vercel Labs `npx skills` CLI](https://github.com/vercel-labs/skills), GitHub CLI (`gh skill`) ve Claude Cowork plugin sistemleriyle %100 uyumluluk sağlanır.
