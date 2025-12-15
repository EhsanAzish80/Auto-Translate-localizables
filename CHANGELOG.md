# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-15

### 🎉 Initial Production Release

Complete transformation from script to production-ready Python package.

### Added

#### Core Features
- **Modern Python Package** (`auto_translate_localizables`)
  - Clean public API with `__init__.py` exports
  - Modular structure: `cli.py`, `translator.py`, `language_map.py`
  - pip-installable via `pyproject.toml`
  
- **CLI Entry Points**
  - `auto-translate-xcloc` - Main command
  - `xcloc-translate` - Alternative command name
  
- **Strict Placeholder Validation**
  - `PlaceholderValidator` class
  - Validates `%@`, `%d`, `%lld`, `%1$@`, `{0}`, `$(var)`, `°C/°F`
  - Returns detailed error messages
  
- **Explicit Language Mapping**
  - 113 languages with explicit mappings
  - No Google auto-guess surprises
  - Regional variant support: `zh-Hans`, `zh-Hant`, `pt-BR`, `es-419`
  - Validation functions: `validate_language_code()`, `get_google_translate_code()`

#### CLI Features
- `--dry-run` - Preview without changes
- `--only-missing` - Incremental translation updates
- `--fail-on-placeholder-mismatch` - Strict validation for CI
- `--skip` - Skip specific languages
- `--only` - Process only specific languages
- `--list-languages` - Show all supported languages
- Proper exit codes (0, 1, 130)

#### Safety Features
- XLIFF structure validation
- Automatic backup and restore on errors
- Rate limiting for translation API
- Error tracking with file/line context
- Preserves XML namespaces and formatting

#### GitHub Actions Workflows
- **Auto-Translate** (`.github/workflows/auto-translate.yml`)
  - Triggers on English localization changes
  - Manual workflow dispatch with options
  - Creates Pull Requests with translations
  - Validates placeholder preservation
  
- **Validate Translations** (`.github/workflows/validate-translations.yml`)
  - Runs on PRs touching localization files
  - Validates XLIFF syntax
  - Checks placeholder preservation

#### Documentation
- **README.md** - Comprehensive 450+ line documentation
  - Problem statement and solution
  - Installation instructions
  - Usage examples (CLI + Python API)
  - CI/CD integration guide
  - Safety features documentation
  - 100+ supported languages
  
- **INSTALL_GUIDE.md** - Development setup and testing
- **QUICK_REFERENCE.md** - Command cheat sheet
- **CONTRIBUTING.md** - Contribution guidelines
- **README.pypi.md** - PyPI package description

#### Package Configuration
- `pyproject.toml` - Modern Python packaging
- `MANIFEST.in` - Package data manifest
- Semantic versioning (v1.0.0)
- Proper dependency declarations
- Entry points configuration

### Changed
- Migrated from scripts to proper package structure
- Updated from `setup.py` to modern `pyproject.toml`
- Improved error handling and reporting
- Enhanced documentation

### Preserved
- Original `localization_app.py` GUI still works
- Original `translate_xliff.py` CLI script still works
- Backward compatibility maintained

---

## Development Roadmap

### [1.1.0] - Planned

#### Translation Quality
- [ ] DeepL translation provider support
- [ ] Provider abstraction layer
- [ ] Per-language provider override
- [ ] Custom terminology support

### [1.2.0] - Planned

#### Enterprise Features
- [ ] Translation memory (TM) support
- [ ] Terminology glossaries
- [ ] Translation review workflow
- [ ] Analytics and reporting
- [ ] Batch processing optimizations

### [2.0.0] - Future

#### Advanced Automation
- [ ] OpenAI GPT translation option
- [ ] Context-aware translations
- [ ] Quality scoring
- [ ] Pre-commit hook integration
- [ ] VS Code extension

---

## Version History

- **1.0.0** (2025-12-15) - Initial production release
  - Complete package transformation
  - GitHub Actions integration
  - Comprehensive documentation
  - 113 language support

---

[1.0.0]: https://github.com/EhsanAzish80/Auto-Translate-localizables/releases/tag/v1.0.0
