#!/bin/bash
# Quick commit and release script for v1.0.0

set -e

echo "🚀 Preparing v1.0.0 Release"
echo ""

# Check git status
echo "📋 Current changes:"
git status --short
echo ""

# Confirm
read -p "Commit and tag v1.0.0? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cancelled."
    exit 1
fi

# Commit
echo ""
echo "📝 Committing changes..."
git add .
git commit -m "v1.0.0: Production package with GitHub Actions

✨ Features:
- Modern Python package (auto_translate_localizables)
- pip-installable via pyproject.toml
- CLI entry points: auto-translate-xcloc, xcloc-translate
- Strict placeholder validation (113 languages)
- CI-friendly modes (--dry-run, --only-missing, --fail-on-placeholder-mismatch)

🤖 GitHub Actions:
- Auto-translate workflow (triggers on en.xcloc changes)
- Validate translations workflow (PR validation)
- Automatic PR creation with detailed descriptions

📚 Documentation:
- Professional README (450+ lines)
- INSTALL_GUIDE, QUICK_REFERENCE, CONTRIBUTING
- CHANGELOG with roadmap

🔧 Infrastructure:
- Modern pyproject.toml packaging
- Comprehensive error handling
- Safety features (backup/restore, validation)
- Proper exit codes for CI

This transforms the tool from scripts to production-ready package
with full CI/CD automation."

# Tag
echo ""
echo "🏷️  Creating v1.0.0 tag..."
git tag -a v1.0.0 -m "v1.0.0: Production release

Complete transformation to production package:
- Modern Python packaging
- GitHub Actions automation
- 113 language support
- Comprehensive documentation
- CI/CD ready"

# Push
echo ""
echo "📤 Pushing to GitHub..."
git push origin main --tags

echo ""
echo "✅ SUCCESS! Release v1.0.0 published"
echo ""
echo "View release: https://github.com/EhsanAzish80/Auto-Translate-localizables/releases"
echo ""
echo "Next steps:"
echo "  1. Check GitHub Actions are working"
echo "  2. Create release notes on GitHub"
echo "  3. (Optional) Publish to PyPI: python3 -m build && twine upload dist/*"
echo ""
