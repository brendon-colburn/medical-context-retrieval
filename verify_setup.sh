#!/bin/bash
# Setup verification script for Medical RAG Demo

echo "🔍 Medical RAG Demo - Setup Verification"
echo "========================================"
echo ""

ISSUES=0

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python installed: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    ISSUES=$((ISSUES + 1))
fi

echo ""

# Check .env file
if [ -f .env ]; then
    echo "✅ .env file exists"

    # Check for required keys
    if grep -q "AZURE_OPENAI_API_KEY" .env; then
        echo "   ✅ AZURE_OPENAI_API_KEY found"
    else
        echo "   ❌ AZURE_OPENAI_API_KEY missing"
        ISSUES=$((ISSUES + 1))
    fi

    if grep -q "AZURE_OPENAI_ENDPOINT" .env; then
        echo "   ✅ AZURE_OPENAI_ENDPOINT found"
    else
        echo "   ❌ AZURE_OPENAI_ENDPOINT missing"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "❌ .env file not found"
    echo "   Create .env with Azure OpenAI credentials"
    ISSUES=$((ISSUES + 1))
fi

echo ""

# Check required directories
for dir in rag cache voila_config examples artifacts; do
    if [ -d "$dir" ]; then
        echo "✅ Directory exists: $dir"
    else
        echo "❌ Directory missing: $dir"
        ISSUES=$((ISSUES + 1))
    fi
done

echo ""

# Check demo notebook
if [ -f demo.ipynb ]; then
    echo "✅ demo.ipynb exists"
else
    echo "❌ demo.ipynb missing"
    ISSUES=$((ISSUES + 1))
fi

echo ""

# Check Python dependencies
echo "📦 Checking Python dependencies..."
MISSING_DEPS=0

# Map package names to their import names
declare -A packages=(
    ["voila"]="voila"
    ["ipywidgets"]="ipywidgets"
    ["faiss-cpu"]="faiss"
    ["requests"]="requests"
    ["beautifulsoup4"]="bs4"
    ["openai"]="openai"
)

for package in "${!packages[@]}"; do
    import_name="${packages[$package]}"
    if python3 -c "import $import_name" 2>/dev/null; then
        echo "   ✅ $package"
    else
        echo "   ❌ $package not installed"
        MISSING_DEPS=$((MISSING_DEPS + 1))
    fi
done

if [ $MISSING_DEPS -gt 0 ]; then
    echo ""
    echo "⚠️  Run: pip install -r requirements.txt"
    ISSUES=$((ISSUES + 1))
fi

echo ""

# Check cache
if [ -d cache ] && [ "$(ls -A cache 2>/dev/null)" ]; then
    CACHE_SIZE=$(du -sh cache | cut -f1)
    echo "✅ Cache populated: $CACHE_SIZE"
else
    echo "⚠️  Cache empty - first run will take ~5 minutes to build index"
fi

echo ""
echo "========================================"

if [ $ISSUES -eq 0 ]; then
    echo "🎉 Setup verification passed!"
    echo ""
    echo "Ready to launch demo:"
    echo "  ./launch_demo.sh"
    exit 0
else
    echo "❌ Found $ISSUES issue(s)"
    echo ""
    echo "Please resolve issues above before running demo."
    exit 1
fi
