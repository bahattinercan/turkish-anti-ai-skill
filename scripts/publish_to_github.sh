#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "=============================================================================="
echo "🚀 TURKISH-ANTI-AI-SKILL GITHUB YAYINLAMA VE GİZLİLİK DENETİM ARACI"
echo "=============================================================================="

# 1. GitHub CLI oturum kontrolü
if ! gh auth status >/dev/null 2>&1; then
    echo "🔑 GitHub CLI oturumu açık değil. Tarayıcı üzerinden giriş başlatılıyor..."
    gh auth login -h github.com -p https -w -s repo
fi

GH_USER="$(gh api user -q .login)"
echo "✅ Aktif GitHub Kullanıcısı: @$GH_USER"

# 2. README.md ve plugin.json içindeki kullanıcı adını otomatik senkronize et
if [ "$GH_USER" != "yucezerey" ]; then
    sed -i '' "s/yucezerey/$GH_USER/g" README.md .claude-plugin/plugin.json SKILL.md
    python3 scripts/build_dist.py
    git add .
    git commit -m "chore: update GitHub username to $GH_USER" || true
fi

# 3. turkish-anti-ai-skill reposunu oluştur veya güncelle (Public)
if gh repo view "$GH_USER/turkish-anti-ai-skill" >/dev/null 2>&1; then
    echo "📦 Repo zaten mevcut ($GH_USER/turkish-anti-ai-skill). Public yapılıyor ve push ediliyor..."
    gh repo edit "$GH_USER/turkish-anti-ai-skill" --visibility public --accept-visibility-change-consequences || true
    git remote remove origin 2>/dev/null || true
    git remote add origin "https://github.com/$GH_USER/turkish-anti-ai-skill.git"
    git push -u origin main --force
else
    echo "📦 Yeni Public repo oluşturuluyor ve push ediliyor: $GH_USER/turkish-anti-ai-skill..."
    gh repo create "$GH_USER/turkish-anti-ai-skill" \
        --public \
        --source=. \
        --remote=origin \
        --description "Türkçe metinlerdeki yapay zeka izlerini (AI slop, translationese, çeviri kokan cümle mimarisi ve TDK hatalarını) temizleyen Agent Skill ve Humanizer paketi." \
        --push
fi

# 4. Repo açıklamasını ve keşfedilebilirlik etiketlerini (GitHub Topics) ayarla
echo "🏷️  GitHub Topics (Etiketler) ve repo ayarları yapılandırılıyor..."
gh repo edit "$GH_USER/turkish-anti-ai-skill" \
    --description "Türkçe metinlerdeki yapay zeka izlerini (AI slop, translationese, çeviri kokan cümle mimarisi ve TDK hatalarını) temizleyen Agent Skill ve Humanizer paketi." \
    --add-topic "agent-skills" \
    --add-topic "ai-skills" \
    --add-topic "claude-code" \
    --add-topic "cursor-rules" \
    --add-topic "gemini-cli" \
    --add-topic "codex" \
    --add-topic "humanizer" \
    --add-topic "ai-writing" \
    --add-topic "de-slop" \
    --add-topic "turkish" \
    --add-topic "turkish-nlp" \
    --add-topic "tdk" \
    --add-topic "prompt-engineering" \
    --add-topic "llm"

# 5. Hesaptaki diğer tüm repoları kontrol et ve Public olanları Private yap
echo ""
echo "🔒 Hesaptaki diğer tüm repoların gizlilik (Private) durumu denetleniyor..."
OTHER_PUBLIC_REPOS=$(gh repo list "$GH_USER" --limit 200 --json name,visibility --jq '.[] | select(.visibility == "PUBLIC" and .name != "turkish-anti-ai-skill") | .name')

if [ -z "$OTHER_PUBLIC_REPOS" ]; then
    echo "✅ Harika! 'turkish-anti-ai-skill' dışında başka hiçbir Public reponuz bulunmuyor."
else
    for repo in $OTHER_PUBLIC_REPOS; do
        echo "   -> '$GH_USER/$repo' Public bulundu, Private yapılıyor..."
        gh repo edit "$GH_USER/$repo" --visibility private --accept-visibility-change-consequences
        echo "   ✅ '$GH_USER/$repo' artık PRIVATE."
    done
fi

echo ""
echo "=============================================================================="
echo "📊 GÜNCEL GITHUB REPO GÖRÜNÜRLÜK TABLOSU (@$GH_USER)"
echo "=============================================================================="
gh repo list "$GH_USER" --limit 200 --json name,visibility,url --template '{{range .}}{{printf "%-35s | %-10s | %s\n" .name .visibility .url}}{{end}}'
echo "=============================================================================="
echo "🎉 İşlem tamamlandı! Tek Public reponuz: https://github.com/$GH_USER/turkish-anti-ai-skill"
