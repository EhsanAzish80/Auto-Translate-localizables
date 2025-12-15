# 📋 Quick Command Reference

## Installation

```bash
# From PyPI (when published)
pip install auto-translate-localizables

# From source (development)
pip3 install -e .

# Or use install script
./install_dev.sh
```

## Essential Commands

```bash
# Get help
auto-translate-xcloc --help

# Check version
auto-translate-xcloc --version

# List all supported languages
auto-translate-xcloc --list-languages
```

## Common Workflows

### 1️⃣ First Time Translation
```bash
# Translate everything (except English)
auto-translate-xcloc --workspace /path/to/localization
```

### 2️⃣ Dry Run (Safe Preview)
```bash
# See what would happen without changing files
auto-translate-xcloc --workspace /path/to/localization --dry-run
```

### 3️⃣ Update Only New Strings
```bash
# Only translate missing strings, preserve existing
auto-translate-xcloc --workspace /path/to/localization --only-missing
```

### 4️⃣ Specific Languages
```bash
# Translate only German, French, Spanish
auto-translate-xcloc --workspace /path/to/localization --only de fr es

# Translate all except English and Arabic
auto-translate-xcloc --workspace /path/to/localization --skip en ar
```

### 5️⃣ CI/CD Mode
```bash
# Fail on placeholder validation errors
auto-translate-xcloc \
  --workspace /path/to/localization \
  --fail-on-placeholder-mismatch
```

### 6️⃣ Combo Moves
```bash
# Dry run + only missing + specific languages
auto-translate-xcloc \
  --workspace ./localization \
  --only-missing \
  --only de fr es \
  --dry-run

# CI mode + only missing (safest for automation)
auto-translate-xcloc \
  --workspace ./localization \
  --only-missing \
  --fail-on-placeholder-mismatch
```

## Python API

```python
from auto_translate_localizables import XLIFFTranslator

# Basic usage
translator = XLIFFTranslator(workspace_dir="/path/to/localization")
results = translator.process_all_languages(skip_languages=['en'])

# With validation strictness
translator = XLIFFTranslator(
    workspace_dir="/path/to/localization",
    fail_on_placeholder_mismatch=True
)

# Process specific language
results = translator.process_language_folder('de', dry_run=False)

# Only missing strings
results = translator.process_all_languages(
    skip_languages=['en'],
    only_missing=True
)

# Check for errors
if translator.errors:
    for error in translator.errors:
        print(f"{error['file']}: {error['error']}")
```

## Xcode Workflow

```bash
# 1. Export from Xcode
# Product → Export Localizations... → Save to ~/Desktop/Localization

# 2. Translate
auto-translate-xcloc --workspace ~/Desktop/Localization

# 3. Import back to Xcode
# Product → Import Localizations... → Select ~/Desktop/Localization
```

## Troubleshooting

```bash
# Command not found after install?
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# Or find where it was installed
pip3 show auto-translate-localizables

# Or use as Python module
python3 -m auto_translate_localizables.cli --help

# Test Python import
python3 -c "from auto_translate_localizables import XLIFFTranslator; print('OK')"
```

## File Structure Expected

```
workspace/
├── en.xcloc/
│   └── Localized Contents/
│       └── en.xliff
├── de.xcloc/
│   └── Localized Contents/
│       └── de.xliff
└── fr.xcloc/
    └── Localized Contents/
        └── fr.xliff
```

## Common Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| `de` | German | `fr` | French |
| `es` | Spanish | `it` | Italian |
| `ja` | Japanese | `ko` | Korean |
| `zh-Hans` | Chinese (Simplified) | `zh-Hant` | Chinese (Traditional) |
| `pt` | Portuguese | `pt-BR` | Portuguese (Brazil) |
| `ru` | Russian | `ar` | Arabic |
| `hi` | Hindi | `th` | Thai |
| `vi` | Vietnamese | `id` | Indonesian |

**See all:** `auto-translate-xcloc --list-languages`

## Exit Codes

- `0` - Success
- `1` - Error (validation failed, file not found, etc.)
- `130` - Interrupted by user (Ctrl+C)

## Pro Tips

💡 Use `--dry-run` first to verify everything looks right  
💡 Use `--only-missing` for incremental updates  
💡 Use `--fail-on-placeholder-mismatch` in CI for safety  
💡 Keep English (`en`) in skip list - it's usually the source  
💡 Check git diff after translating to review changes  
💡 For large projects (1000+ strings), run in batches or use `--only-missing`  

## Where to Get Help

- 📖 Full docs: [README_NEW.md](README_NEW.md)
- 🛠️ Installation: [INSTALL_GUIDE.md](INSTALL_GUIDE.md)
- 🐛 Issues: https://github.com/EhsanAzish80/Auto-Translate-localizables/issues
- 💬 Inline help: `auto-translate-xcloc --help`
