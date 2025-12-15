# auto-translate-localizables

Automates Xcode .xcloc localization using reproducible, CI-friendly machine translation.

## Installation

```bash
pip install auto-translate-localizables
```

## Quick Start

```bash
# Translate all languages in your Xcode localization export
auto-translate-xcloc --workspace /path/to/localization

# See what would happen without making changes
auto-translate-xcloc --workspace /path/to/localization --dry-run

# Only translate missing strings
auto-translate-xcloc --workspace /path/to/localization --only-missing
```

## Documentation

See [full documentation](https://github.com/EhsanAzish80/Auto-Translate-localizables#readme) for:
- Complete usage guide
- CI/CD integration examples
- API reference
- Supported languages (100+)
- Safety features and validation

## Features

✅ Automatic Xcode .xcloc detection  
✅ Strict placeholder preservation (`%@`, `%d`, `{0}`, etc.)  
✅ 100+ language support  
✅ CI-friendly modes (`--dry-run`, `--fail-on-placeholder-mismatch`)  
✅ Safe XLIFF handling with auto-restore  
✅ Command-line + Python library

## License

MIT
