#!/bin/bash
# ==============================================================================
# SCRIPT ĐẨY DASHBOARD LÊN GITHUB PAGES TỰ ĐỘNG
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "========================================================"
echo "🚀 ĐANG CHUẨN BỊ ĐẨY DASHBOARD LÊN GITHUB PAGES"
echo "========================================================"

# Đảm bảo index.html là dashboard mới nhất
cp omnichannel_performance_dashboard.html index.html
touch .nojekyll

# Khởi tạo Git nếu chưa có
if [ ! -d ".git" ]; then
    echo "📦 Khởi tạo Git Repository..."
    git init
    git branch -M main
fi

# Cấu hình user git
git config user.name "Ecom Operations"
git config user.email "operations@30shine.com"

# Kiểm tra Token từ tham số dòng lệnh hoặc Config hoặc Nhập vào
GITHUB_TOKEN="$1"
REPO_URL="$2"

if [ -z "$REPO_URL" ]; then
    REPO_URL="github.com/phamphilong0711-cell/Ecom-Dashboard.git"
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo ""
    echo "🔑 Vui lòng nhập GitHub Personal Access Token (PAT) của bạn (bắt đầu bằng ghp_...):"
    read -r GITHUB_TOKEN
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Lỗi: Bạn chưa cung cấp GitHub Token. Không thể đẩy lên GitHub."
    exit 1
fi

echo "🔗 Cấu hình Remote Origin..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://${GITHUB_TOKEN}@${REPO_URL}"

echo "📁 Đang thêm các file dashboard tĩnh vào Git..."
git add index.html omnichannel_performance_dashboard.html .nojekyll .gitignore

echo "💾 Đang tạo commit..."
git commit -m "Deploy September 2026 Ecom Operations Dashboard to GitHub Pages" || echo "Không có thay đổi mới để commit."

echo "☁️ Đang đẩy lên GitHub (main branch)..."
git push -u origin main --force

echo ""
echo "========================================================"
echo "🎉 THÀNH CÔNG! DASHBOARD ĐÃ ĐƯỢC ĐẨY LÊN GITHUB!"
echo "🌐 Link GitHub Pages của bạn:"
echo "👉 https://phamphilong0711-cell.github.io/Ecom-Dashboard/"
echo "========================================================"
