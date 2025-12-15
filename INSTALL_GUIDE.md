# Installation & Testing Guide

## Quick Install (Development)

```bash
./install_dev.sh
```

Or manually:

```bash
pip install -e .
```

## Verify Installation

```bash
# Check version
auto-translate-xcloc --version

# List supported languages
auto-translate-xcloc --list-languages

# Get help
auto-translate-xcloc --help
```

## Test the Package

### 1. Basic Validation

```bash
# Validate package structure
python3 -c "from auto_translate_localizables import XLIFFTranslator, LANGUAGE_MAP; print('✓ Import successful')"

# Check CLI entry point
which auto-translate-xcloc

# Alternative command name
which xcloc-translate
```

### 2. Test with Sample Data

If you have a localization workspace:

```bash
# Dry run to verify detection
auto-translate-xcloc --workspace /path/to/localization --dry-run

# Translate one language only
auto-translate-xcloc --workspace /path/to/localization --only de --dry-run
```

### 3. Test Placeholder Validation

```python
from auto_translate_localizables.translator import PlaceholderValidator

# Test valid translation
original = "You have %d items"
translated = "Du hast %d Artikel"
is_valid, error = PlaceholderValidator.validate(original, translated)
print(f"Valid: {is_valid}")  # Should be True

# Test invalid translation (missing placeholder)
bad_translation = "Du hast Artikel"
is_valid, error = PlaceholderValidator.validate(original, bad_translation)
print(f"Valid: {is_valid}, Error: {error}")  # Should be False
```

## Build for Distribution

### Build Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Output:
# dist/
#   auto_translate_localizables-1.0.0-py3-none-any.whl
#   auto_translate_localizables-1.0.0.tar.gz
```

### Test Distribution

```bash
# Test install from wheel
pip install dist/auto_translate_localizables-1.0.0-py3-none-any.whl

# Verify
auto-translate-xcloc --version
```

### Publish to PyPI (when ready)

```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## Common Issues

### Command not found after install

```bash
# Ensure pip bin directory is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Or use Python module syntax
python3 -m auto_translate_localizables.cli --help
```

### Import errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or reinstall package
pip install -e . --force-reinstall
```

## Development Workflow

```bash
# 1. Make code changes
vim auto_translate_localizables/translator.py

# 2. Package already installed in editable mode, changes are live

# 3. Test immediately
auto-translate-xcloc --help

# 4. Format code (optional)
pip install black
black auto_translate_localizables/

# 5. Commit
git add .
git commit -m "Feature: Add xyz"
```

## Next Steps

Once everything works:

1. ✅ Replace old README with new one
2. ✅ Update GitHub repository description
3. ✅ Create release tag v1.0.0
4. ✅ Publish to PyPI
5. ✅ Add GitHub Action for CI

See [README_NEW.md](README_NEW.md) for the polished documentation.
