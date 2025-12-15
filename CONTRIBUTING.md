# Contributing to auto-translate-localizables

Thank you for your interest in contributing! 🎉

## Quick Links

- 📖 [Main Documentation](README.md)
- 🐛 [Report a Bug](https://github.com/EhsanAzish80/Auto-Translate-localizables/issues)
- 💡 [Request a Feature](https://github.com/EhsanAzish80/Auto-Translate-localizables/issues)
- 💬 [Discussions](https://github.com/EhsanAzish80/Auto-Translate-localizables/discussions)

---

## How to Contribute

### Reporting Bugs

If you find a bug, please [open an issue](https://github.com/EhsanAzish80/Auto-Translate-localizables/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Sample XLIFF files if possible (sanitized)

### Suggesting Features

Feature requests are welcome! Please include:
- Clear use case
- Expected behavior
- Why it would be useful to others
- Any implementation ideas

---

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/Auto-Translate-localizables.git
cd Auto-Translate-localizables
```

### 2. Install in Development Mode

```bash
# Install package in editable mode
pip install -e .

# Or use the install script
./install_dev.sh

# Install optional dev dependencies
pip install -e ".[dev]"
```

### 3. Verify Installation

```bash
# Test CLI
auto-translate-xcloc --version

# Test Python import
python -c "from auto_translate_localizables import XLIFFTranslator; print('✓')"
```

---

## Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
# or
git checkout -b fix/bug-description
```

### 2. Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings for public functions
- Keep functions focused and testable

```python
def process_xliff_file(
    self, 
    xliff_path: Path, 
    target_lang: str,
    dry_run: bool = False
) -> Tuple[int, int]:
    """
    Process a single XLIFF file.
    
    Args:
        xliff_path: Path to XLIFF file
        target_lang: Target language code
        dry_run: If True, don't save changes
        
    Returns:
        (translated_count, error_count)
    """
    # Implementation
```

### 3. Test Your Changes

```bash
# Test CLI functionality
auto-translate-xcloc --workspace ./test_data --dry-run

# Test specific features
python -c "
from auto_translate_localizables import PlaceholderValidator
result, error = PlaceholderValidator.validate('Test %@', 'Test %@')
print(f'Valid: {result}')
"

# Check syntax
python -m py_compile auto_translate_localizables/*.py
```
   python -m py_compile translate_xliff.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: description of your feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Explain what you changed and why

## Development Setup

### Prerequisites
- Python 3.7+
- pip
- Git

### Setup
```bash
# Clone your fork
git clone https://github.com/EhsanAzish80/Auto-Translate-localizables.git
cd Auto-Translate-localizables

# Install dependencies
pip3 install -r requirements.txt

# Install development dependencies (optional)
pip3 install pylint black pytest
```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### Testing Checklist

Before submitting a PR, please verify:
- [ ] Code runs without errors
- [ ] GUI opens and functions correctly
- [ ] CLI mode works with all options
- [ ] No syntax errors (`python -m py_compile`)
- [ ] Existing functionality not broken
- [ ] Documentation updated if needed
- [ ] No hardcoded paths or credentials

## Areas for Contribution

We especially welcome contributions in:

### High Priority
- [ ] Unit tests for translation logic
- [ ] Integration tests with sample XLIFF files
- [ ] Error handling improvements
- [ ] Performance optimization

### Medium Priority
- [ ] Support for additional translation APIs (DeepL, Azure)
- [ ] Translation memory/cache
- [ ] Custom placeholder pattern configuration
- [ ] Export translation statistics to CSV/JSON

### Nice to Have
- [ ] Dark mode for GUI
- [ ] Batch workspace processing
- [ ] Translation quality scoring
- [ ] Undo/redo functionality
- [ ] Progress bar for individual files

## Project Structure

```
xliff-translator/
├── localization_app.py       # GUI application
├── translate_xliff.py         # CLI tool
├── requirements.txt           # Dependencies
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
├── README_TRANSLATION.md     # CLI documentation
├── CONTRIBUTING.md           # This file
├── LICENSE                    # MIT License
├── .gitignore                # Git ignore rules
├── run.sh                    # Startup script
└── .github/
    └── workflows/
        └── test.yml          # CI/CD
```

## Core Components

### XLIFFTranslator Class
- Handles XLIFF parsing and translation
- Preserves placeholders and formatting
- Manages Google Translate API calls

### LocalizationApp Class
- GUI interface using Tkinter
- Language detection
- Progress tracking
- Log display

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

## Code of Conduct

Be respectful and constructive:
- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making this project better! 🙏
