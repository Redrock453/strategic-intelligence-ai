#!/bin/bash
# Запускай в корні strategic-intelligence-ai репо
# git clone https://github.com/Redrock453/strategic-intelligence-ai (якщо ще не)
# cd strategic-intelligence-ai
# bash push_arch.sh

set -e

echo "📁 Створюємо docs/ папку..."
mkdir -p docs

echo "📄 Копіюємо файли..."
# Поклади arch_timeline.html поруч з цим скриптом
cp arch_timeline.html docs/architecture.html 2>/dev/null || \
  echo "⚠️  Поклади arch_timeline.html поруч зі скриптом"

# ARCHITECTURE.md вже має бути в корні репо
echo "✅ Файли готові"

git add docs/architecture.html ARCHITECTURE.md 2>/dev/null || git add docs/ ARCHITECTURE.md

git commit -m "docs: AI infrastructure architecture v2.0 + roadmap

- Full stack: Signal/Telegram → Control Plane → Workers → LLM  
- 7-week Gantt timeline from 2026-03-04
- strategic-intelligence-ai = Document AI + OSINT + multi-agent core
- Roadmap: Phase 1 credentials rotation → Telegram bot → doc AI
- Marked Browser Use 502 as BLOCKER
- Decision: drop openclaw, use Control Plane as hub"

git push origin main

echo ""
echo "✓ Запушено!"
echo "👉 https://github.com/Redrock453/strategic-intelligence-ai"
