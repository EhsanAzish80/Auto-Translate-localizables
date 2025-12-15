# 🌍 auto-translate-localizables

**Automates Xcode .xcloc localization using reproducible, CI-friendly machine translation—built for real iOS teams.**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/auto-translate-localizables/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](https://github.com/EhsanAzish80/Auto-Translate-localizables)

---

## Why This Exists

**Xcode exports `.xcloc`, but Apple provides no bulk translation workflow.** This tool fills that gap.

If you've ever manually translated hundreds of localization strings, or copy-pasted between Xcode and Google Translate, you know the pain. This tool automates the entire workflow while maintaining safety and reproducibility.

---

## The Problem → Solution

### Before 😤
```
1. Export .xcloc from Xcode
2. Open each language's XLIFF file
3. Copy string → Google Translate → Paste
4. Repeat 500 times
5. Hope you didn't break any %@ placeholders
6. Import back into Xcode
7. Build fails because placeholders got mangled
```

### After ✨
```bash
auto-translate-xcloc --workspace ./localization
```

**That's it.** All languages translated. Placeholders preserved. XLIFF structure validated. Ready for Xcode import.

---

## ✨ Features

- **🎯 Zero Configuration** — Automatically detects languages and structure
- **🛡️ Strict Placeholder Preservation** — Validates `%@`, `%d`, `{0}`, etc. are preserved exactly
- **🌐 100+ Languages** — Supports all major languages via Google Translate
- **⚡ CI-Friendly** — `--dry-run`, `--only-missing`, `--fail-on-placeholder-mismatch` modes
- **🔍 Smart Translation** — Skips units (kg, ml), preserves formatting, handles special characters
- **💾 Safe by Default** — Validates XLIFF structure, auto-restores on corruption
- **📦 Proper Package** — Install via pip, use as CLI or Python library
- **🎯 Xcode Compatible** — Works with iOS, macOS, watchOS, tvOS projects

---

## 🚀 Installation

### Install from PyPI (recommended)
```bash
pip install auto-translate-localizables
```

### Install from source
```bash
git clone https://github.com/EhsanAzish80/Auto-Translate-localizables
cd Auto-Translate-localizables
pip install -e .
```

### Verify installation
```bash
auto-translate-xcloc --version
```

---

## 📖 Usage

### Basic Usage

```bash
# Translate all languages
auto-translate-xcloc --workspace /path/to/localization

# Dry run (see what would happen)
auto-translate-xcloc --workspace ./localization --dry-run

# Only translate missing strings (preserve existing)
auto-translate-xcloc --workspace ./localization --only-missing
```

### Advanced Usage

```bash
# Translate specific languages only
auto-translate-xcloc --workspace ./localization --only de fr es

# Skip certain languages
auto-translate-xcloc --workspace ./localization --skip en ar

# CI mode: fail on placeholder mismatches
auto-translate-xcloc --workspace ./localization --fail-on-placeholder-mismatch

# List all supported languages
auto-translate-xcloc --list-languages
```

### Expected Directory Structure

```
workspace/
├── en.xcloc/
│   └── Localized Contents/
│       └── en.xliff
├── de.xcloc/
│   └── Localized Contents/
│       └── de.xliff
├── fr.xcloc/
│   └── Localized Contents/
│       └── fr.xliff
└── es.xcloc/
    └── Localized Contents/
        └── es.xliff
```

This is the standard structure Xcode creates when you export localizations.

---

## 🔧 As a Python Library

```python
from auto_translate_localizables import XLIFFTranslator

# Create translator
translator = XLIFFTranslator(
    workspace_dir="/path/to/localization",
    fail_on_placeholder_mismatch=True
)

# Translate all languages
results = translator.process_all_languages(
    skip_languages=['en'],
    dry_run=False,
    only_missing=False
)

# Process specific language
results = translator.process_language_folder('de', dry_run=False)

# Check for errors
if translator.errors:
    for error in translator.errors:
        print(f"Error: {error['file']}: {error['error']}")
```

---

## 🎯 Workflow Integration

### Xcode Export → Translate → Import

```bash
# 1. Export from Xcode
# Product → Export Localizations...

# 2. Translate
auto-translate-xcloc --workspace ./LocalizationExport

# 3. Import back to Xcode
# Product → Import Localizations...
```

### With Version Control

```bash
# After exporting from Xcode
git add localization/*.xcloc
auto-translate-xcloc --workspace ./localization
git diff  # Review translations
git commit -m "Update translations"
```

---

## 🤖 CI/CD Integration

### GitHub Actions Example

```yaml
name: Update Translations

on:
  workflow_dispatch:
  push:
    paths:
      - 'localization/en.xcloc/**'

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install translator
        run: pip install auto-translate-localizables
      
      - name: Translate
        run: |
          auto-translate-xcloc \
            --workspace ./localization \
            --only-missing \
            --fail-on-placeholder-mismatch
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "🌍 Update translations"
          commit-message: "Update localization files"
          branch: auto-translations
```

---

## 🛡️ Safety Features

### Placeholder Preservation

The tool **strictly validates** that placeholders are preserved:

```python
# Original
"You have %d items in %@"

# ✅ Valid translation (German)
"Sie haben %d Artikel in %@"

# ❌ Invalid - placeholder count mismatch
"Sie haben Artikel in %@"  # Missing %d

# ❌ Invalid - placeholder type changed
"Sie haben %@ Artikel in %d"  # Swapped types
```

### XLIFF Validation

- Validates XML structure before and after translation
- Auto-restores original file if corruption detected
- Preserves XML namespaces and attributes
- Maintains Xcode-compatible formatting

### Rate Limiting

- Automatic delays between translations
- Prevents Google Translate rate limiting
- Configurable batch sizes

---

## 🌍 Supported Languages

100+ languages supported. Run `auto-translate-xcloc --list-languages` for full list.

Common examples:
- 🇩🇪 German (`de`)
- 🇫🇷 French (`fr`)
- 🇪🇸 Spanish (`es`, `es-419`, `es-MX`)
- 🇨🇳 Chinese Simplified (`zh-Hans`)
- 🇹🇼 Chinese Traditional (`zh-Hant`)
- 🇯🇵 Japanese (`ja`)
- 🇰🇷 Korean (`ko`)
- 🇷🇺 Russian (`ru`)
- 🇵🇹 Portuguese (`pt`, `pt-BR`, `pt-PT`)
- And many more...

---

## ⚠️ Important Disclaimers

### Machine Translation

**This tool uses Google Translate.** Output quality varies by language. Always have translations reviewed by native speakers before shipping to production.

### Placeholder Limitations

While the tool validates placeholder **preservation**, it cannot validate placeholder **position** correctness in all languages. Some languages require different word orders.

### Rate Limits

Google Translate has rate limits. For very large projects (1000+ strings), run with `--only-missing` on subsequent runs.

---

## 🔄 Development Workflow

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/EhsanAzish80/Auto-Translate-localizables
cd Auto-Translate-localizables

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests (when available)
pytest

# Format code
black .

# Type checking
mypy auto_translate_localizables
```

### Package Structure

```
auto-translate-localizables/
├── auto_translate_localizables/
│   ├── __init__.py          # Package exports
│   ├── cli.py               # CLI entry point
│   ├── translator.py        # Core translation logic
│   └── language_map.py      # Language code mappings
├── pyproject.toml           # Modern Python packaging
├── README.md
└── LICENSE
```

---

## 🎓 Examples

### Example 1: First-Time Translation

```bash
# Export from Xcode to ~/Desktop/Localization
# Run translation
auto-translate-xcloc --workspace ~/Desktop/Localization

# Output:
# ============================================================
# XLIFF Bulk Translation
# ============================================================
# Workspace: /Users/you/Desktop/Localization
# Skipping: en
# Mode: TRANSLATION
# ============================================================
# 
# ============================================================
# Processing DE -> de
# ============================================================
# 
# [FILE] Localizable.xliff
#   [✓] Translated 245 entries (0 errors)
# 
# [✓] de        ->  245 translated,    0 errors
# 
# ============================================================
# TOTAL: 245 entries translated
#        0 errors
# ============================================================
```

### Example 2: Update Only Missing

```bash
# You've added 20 new strings to English
auto-translate-xcloc --workspace ./localization --only-missing

# Only translates the 20 new strings, preserves existing translations
```

### Example 3: CI Validation

```bash
# In CI pipeline
auto-translate-xcloc \
  --workspace ./localization \
  --dry-run \
  --fail-on-placeholder-mismatch

# Exit code 0 = all good
# Exit code 1 = validation errors found
```

---

## 🤝 Contributing

Contributions welcome! This project follows standard Python best practices.

### Areas for contribution:
- DeepL translation provider support
- Azure Translator support
- Custom terminology/glossary support
- Translation memory (TM) integration
- Improved placeholder validation
- GUI improvements
- Test coverage

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [deep-translator](https://github.com/nidhaloff/deep-translator) - Translation API wrapper
- [lxml](https://lxml.de/) - Robust XML processing
- Apple Xcode XLIFF format

---

## 📧 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/EhsanAzish80/Auto-Translate-localizables/issues)
- **Author**: Ehsan Azish
- **Email**: ehsanazish80@gmail.com

---

## 🚀 Roadmap

### Phase 2 - Automation (Next)
- [ ] GitHub Action for automated translation
- [ ] Pre-commit hook integration
- [ ] Translation quality scoring

### Phase 3 - Translation Quality
- [ ] DeepL provider support
- [ ] OpenAI GPT translation option
- [ ] Per-language provider override
- [ ] Custom terminology support

### Phase 4 - Enterprise Features
- [ ] Translation memory (TM) support
- [ ] Terminology glossaries
- [ ] Translation review workflow
- [ ] Analytics and reporting

---

**Star ⭐ this repo if it saved you time!**
