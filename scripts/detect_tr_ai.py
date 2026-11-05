#!/usr/bin/env python3
"""
detect_tr_ai.py - Deterministik Türkçe AI Yazım İzi (AI Slop & Translationese) Tarayıcısı
Kullanım: python3 scripts/detect_tr_ai.py <dosya_yolu.md> [--json]
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

TIER1_PATTERNS = [
    (r"\byadsınamaz\b", "Tier-1 Klişe: 'yadsınamaz' (undeniable calque)"),
    (r"\badeta\b", "Tier-1 Klişe: 'adeta' (aşırı benzetme zarfı)"),
    (r"\bderinlemesine\s+(?:inmek|incelemek|bakmak|ele\s+almak)\b", "Tier-1 Klişe: 'derinlemesine inmek/incelemek' (delve into calque)"),
    (r"\bkritik\s+(?:bir\s+)?(?:rol\s+oyna|öneme\s+sahip)", "Tier-1 Klişe: 'kritik bir rol oynamak / öneme sahip olmak'"),
    (r"\bgeniş\s+bir\s+yelpaze", "Tier-1 Klişe: 'geniş bir yelpaze' (wide range/spectrum calque)"),
    (r"\bsadece\s+[^,.]+?\s+değil,\s*aynı\s+zamanda\b", "P0 Yapısal: 'sadece X değil, aynı zamanda Y' (negatif paralellik)"),
    (r"\byalnızca\s+[^,.]+?\s+olmakla\s+kalmayıp\b", "P0 Yapısal: 'yalnızca X olmakla kalmayıp' (not only... but also)"),
    (r"\bgünümüzün\s+hızla\s+değişen\b", "P0 Sahneleme: 'günümüzün hızla değişen...' (boş giriş klişesi)"),
    (r"\bçığır\s+açan\b|\bdönüm\s+noktası\b", "Tier-1 Şişirme: 'çığır açan / dönüm noktası' (groundbreaking/watershed)"),
    (r"\bpotansiyelini\s+ortaya\s+çıkar", "Tier-1 Klişe: 'potansiyelini ortaya çıkarmak' (unlock potential)"),
]

TIER2_PATTERNS = [
    (r"\bbununla\s+birlikte\b|\böte\s+yandan\b", "Tier-2 Geçiş: 'bununla birlikte / öte yandan' (moreover/however)"),
    (r"\bbelirtmek\s+gerekir\s+ki\b|\bunutulmamalıdır\s+ki\b", "Tier-2 Dolgu: 'belirtmek gerekir ki / unutulmamalıdır ki'"),
    (r"\bsöz\s+konusu\b|\bbu\s+bağlamda\b|\bbu\s+doğrultuda\b", "Tier-2 Bürokratik: 'söz konusu / bu bağlamda / bu doğrultuda'"),
    (r"\bbütüncül\s+(?:bir\s+)?yaklaşım\b", "Tier-2 Jargon: 'bütüncül yaklaşım' (holistic approach)"),
    (r"\bsonuç\s+olarak\b|\bözetlemek\s+gerekirse\b", "Tier-2 Kapanış: 'sonuç olarak / özetlemek gerekirse'"),
    (r"\btarafından\s+(?:gerçekleştiril|yapıl|sağlan)", "P1 Sentaks: Edilgen çatı + 'tarafından' + kof yardımcı fiil"),
]

PUNCTUATION_AND_TDK_PATTERNS = [
    (r"—", "P2 Noktalama: Uzun çizgi (em-dash '—') kullanımı (TDK diyalog dışında yasaklar)"),
    (r"\d+[–]\d+", "P2 Noktalama: Sayı aralığında orta çizgi (en-dash '–') kullanımı (TDK kısa çizgi '-' şart koşar)"),
    (r",\s*(?:ama|fakat|lakin|veya|ya da)\b", "P2 Noktalama: Karşıtlık/seçenek bağlacından ('ama/fakat/ya da') önce virgül"),
    (r"\b(?:birşey|herşey|hiçbirşey|yada|bir çok|bir kaç|pekçok|ard arda|yanısıra|önsöz|önyargı|işbirliği|farketmek)\b", "P2 TDK İmla Hatası: Birleşik/ayrı yazılan kelime hatası"),
]

# Büyük/küçük harf ve Türkçe ı/i ayrımına duyarlı fonetik ek hataları
CASE_SENSITIVE_PATTERNS = [
    (r"\b(?:cache'ı|cache'de|cache'dan|SQL'ı|SQL'da|SQL'dan|JSON'i|JSON'de|queue'ya|React'ı|React'da|Node\.js'ı|Node\.js'da)\b", "P2 Fonetik Ek Hatası: Yabancı terime Türkçe okunuşu yerine yazılışına göre ek getirilmesi"),
]


def analyze_text(text: str) -> dict:
    findings = []
    for pattern, label in TIER1_PATTERNS + TIER2_PATTERNS + PUNCTUATION_AND_TDK_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            findings.append({
                "rule": label,
                "match": match.group(0),
                "position": match.start(),
            })

    for pattern, label in CASE_SENSITIVE_PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append({
                "rule": label,
                "match": match.group(0),
                "position": match.start(),
            })

    words = re.findall(r"\b\w+\b", text)
    word_count = max(len(words), 1)
    mektedir_count = len(re.findall(r"\w+m[ae]kt[ae]d[ıi]r\b", text, flags=re.IGNORECASE))
    mektedir_per_100 = round((mektedir_count / word_count) * 100, 2)

    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if len(s.strip().split()) > 1]
    sent_lengths = [len(s.split()) for s in sentences]
    if len(sent_lengths) >= 3:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((x - mean_len) ** 2 for x in sent_lengths) / len(sent_lengths)
        cov = round(math.sqrt(variance) / mean_len, 2) if mean_len > 0 else 0.0
    else:
        cov = 0.5

    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "sentence_length_cov": cov,
        "low_burstiness_warning": cov < 0.35 and len(sentences) >= 4,
        "mektedir_per_100_words": mektedir_per_100,
        "high_mektedir_warning": mektedir_per_100 > 2.5,
        "total_flags": len(findings),
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser(description="Türkçe AI Yazım İzi (AI Slop) Tarayıcısı")
    parser.add_argument("file", help="Taranacak metin veya Markdown dosyası")
    parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında ver")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Hata: {args.file} bulunamadı.", file=sys.stderr)
        sys.exit(2)

    report = analyze_text(path.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"=== Turkish Anti-AI Denetim Raporu: {path.name} ===")
        print(f"Kelime Sayısı: {report['word_count']} | Cümle Sayısı: {report['sentence_count']}")
        print(f"Cümle Uzunluğu Değişim Katsayısı (Burstiness CoV): {report['sentence_length_cov']} (İnsan hedefi: >= 0.40)")
        print(f"'-mAktAdIr' Yoğunluğu (100 kelimede): {report['mektedir_per_100_words']}")
        print(f"Toplam Yakalanan AI/TDK Sinyali: {report['total_flags']}")
        for item in report["findings"]:
            print(f"  - [{item['rule']}] -> \"{item['match']}\"")


if __name__ == "__main__":
    main()
