# Project Information

**Project Name:** XLIFF Localization Translator  
**Version:** 1.0.0  
**License:** MIT  
**Python Required:** 3.7+  
**Platform:** Cross-platform (macOS, Linux, Windows)

## Description

A standalone Python application with GUI for automatically translating XLIFF localization files. Designed specifically for iOS/Xcode projects with support for 30+ languages.

## Key Features

✅ User-friendly Tkinter GUI interface  
✅ Auto-detection of localization folders  
✅ Smart placeholder preservation (%@, %d, etc.)  
✅ Unit and special character preservation  
✅ Command-line interface for automation  
✅ Real-time progress tracking  
✅ Support for 30+ languages via Google Translate  
✅ Safe translation (backs up and validates XLIFF)  
✅ Selective language translation  

## Tech Stack

- **Language:** Python 3.7+
- **GUI Framework:** Tkinter (built-in)
- **Translation API:** Google Translate (via deep-translator)
- **XML Parser:** lxml (with ElementTree fallback)
- **Platform:** Cross-platform

## Dependencies

```
deep-translator>=1.11.4  # Google Translate integration
lxml>=4.9.0             # Better XML/XLIFF parsing
```

## File Structure

```
xliff-translator/
├── localization_app.py          # Main GUI application (584 lines)
├── translate_xliff.py            # CLI tool (398 lines)
├── requirements.txt              # Python dependencies
├── setup.sh                      # Automated setup script
├── run.sh                        # Quick launch script
├── README.md                     # Main documentation
├── QUICKSTART.md                # Quick start guide
├── README_TRANSLATION.md        # Detailed CLI docs
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                       # MIT License
├── .gitignore                   # Git ignore rules
└── .github/
    └── workflows/
        └── test.yml             # CI/CD pipeline
```

## Usage Modes

### 1. GUI Mode (Recommended for most users)
```bash
./run.sh
# or
python3 localization_app.py
```

### 2. CLI Mode (For automation/scripting)
```bash
python3 translate_xliff.py --workspace /path/to/localization
python3 translate_xliff.py --only de fr ja
python3 translate_xliff.py --dry-run
```

## Supported Languages

Arabic, Czech, Danish, German, Greek, English, Spanish (multiple variants), Finnish, French, Hindi, Indonesian, Italian, Japanese, Korean, Dutch, Polish, Portuguese (Brazil/Portugal), Romanian, Russian, Slovak, Swedish, Thai, Turkish, Ukrainian, Vietnamese, Chinese (Simplified/Traditional)

## Translation Approach

The tool intelligently:
1. Scans .xcloc folders for XLIFF files
2. Identifies untranslated or incomplete entries
3. Extracts placeholders and special characters
4. Translates using Google Translate API
5. Restores placeholders in exact positions
6. Validates XLIFF structure
7. Updates files with state="translated"

## Preservation Rules

**Preserved Elements:**
- Placeholders: %@, %d, %lld, %1$@, %2$d, etc.
- Units: kg, lbs, ml, oz, min
- Special characters: °C, °F, 💧
- Formatting: Punctuation, spacing, newlines
- XLIFF structure: Valid XML for Xcode compatibility

**Translation Rules:**
- Only translates missing or incomplete targets
- Never overwrites existing translations
- Respects state="translated" markers
- Preserves source language entries

## Installation

**Quick Install:**
```bash
./setup.sh
```

**Manual Install:**
```bash
pip3 install -r requirements.txt
```

## Testing

**Syntax Check:**
```bash
python -m py_compile localization_app.py
python -m py_compile translate_xliff.py
```

**Dry Run:**
```bash
python3 translate_xliff.py --dry-run --workspace test/folder
```

**GUI Test:**
```bash
python3 localization_app.py
```

## Performance

- Processes ~100-200 entries per minute (varies by language)
- Rate limiting: 0.5s delay every 10 entries
- Memory efficient: Streams XLIFF files
- Safe: Backs up before modifying

## Limitations

- Requires internet connection for Google Translate
- Translation quality depends on Google Translate API
- Context-limited for short strings
- May need manual review for specialized terminology

## Future Enhancements

- [ ] Support for DeepL, Azure Translator APIs
- [ ] Translation memory/cache system
- [ ] Batch workspace processing
- [ ] Export statistics to CSV/JSON
- [ ] Custom placeholder patterns
- [ ] Translation quality scoring
- [ ] Dark mode for GUI
- [ ] Undo/redo functionality

## GitHub Repository Setup

**Recommended branches:**
- `main` - Stable releases
- `develop` - Development branch
- Feature branches: `feature/*`
- Bugfix branches: `bugfix/*`

**Recommended tags:**
- `v1.0.0` - Initial release
- Follow semantic versioning

## Support

- GitHub Issues: Bug reports and feature requests
- Discussions: Questions and community support
- Wiki: Detailed guides and examples

## Credits

Built with:
- [deep-translator](https://github.com/nidhaloff/deep-translator) by @nidhaloff
- [lxml](https://lxml.de/) by the lxml team
- Python Tkinter for GUI

## Statistics

- **Total Lines of Code:** ~1000+ lines
- **Languages Supported:** 30+
- **File Formats:** XLIFF 1.2
- **Platforms:** macOS, Linux, Windows
- **License:** MIT (Open Source)

---

**Author:** Ehsan Azish (@ehsanazish80)  
**Created:** December 2025  
**Last Updated:** December 15, 2025  
**Status:** Active Development
