# 🌍 XLIFF Localization Translator for Xcode

A standalone Python application with GUI for automatically translating Xcode XLIFF localization files. Perfect for iOS, macOS, watchOS, and tvOS projects with multiple language support.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)
![Xcode](https://img.shields.io/badge/Xcode-Localization-blue.svg)
![Languages](https://img.shields.io/badge/languages-100+-green.svg)

## ✨ Features

- 🖥️ **User-Friendly GUI** - Simple Tkinter interface, no command line required
- 🔍 **Auto-Detection** - Automatically finds all Xcode localization folders (.xcloc)
- 🌐 **100+ Languages** - Supports all major languages with Google Translate
- 🎯 **Xcode Compatible** - Works with iOS, macOS, watchOS, and tvOS projects
- 🛡️ **Smart Translation** - Preserves placeholders (%@, %d), units (kg, ml), and special characters
- ⚡ **Fast & Efficient** - Batch processing with progress tracking
- 💾 **Safe** - Validates XLIFF structure for Xcode compatibility
- 🌍 **Cross-Platform** - Works on macOS, Linux, and Windows
- 🎯 **Selective Translation** - Choose which languages to translate

## 📸 Screenshots

### Main Interface
The app provides:
- Workspace folder selection
- Automatic language detection
- Default language selection
- Multi-select target languages
- Real-time translation log
- Progress tracking

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/EhsanAzish80/Auto-Translate-localizables
cd Auto-Translate-localizables
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

### Running the App

**GUI Mode (Recommended):**
```bash
python3 localization_app.py
```

**Command Line Mode:**
```bash
# Translate all languages
python3 translate_xliff.py

# Translate specific languages only
python3 translate_xliff.py --only de fr ja

# Dry run (preview without changes)
python3 translate_xliff.py --dry-run
```

## 📖 Usage Guide

### Using the GUI App

1. **Select Workspace**
   - Click "Browse..." to select your localization folder
   - The folder should contain `.xcloc` subfolders

2. **Auto-Detect Languages**
   - App automatically detects all available languages
   - Choose your default/source language (typically English)

3. **Select Target Languages**
   - Select which languages you want to translate to
   - Multiple selection supported (Cmd/Ctrl + Click)

4. **Start Translation**
   - Click "🚀 Start Translation"
   - Monitor progress in the log window
   - Translation can be stopped anytime

### Command Line Options

```bash
python3 translate_xliff.py [OPTIONS]

Options:
  -w, --workspace PATH    Path to localization workspace
  -d, --dry-run          Preview mode (no changes)
  -s, --skip LANGS       Languages to skip (default: en ar)
  -o, --only LANGS       Only translate these languages
```

## 🗂️ Folder Structure

Your localization workspace should look like:
```
localization/
├── en.xcloc/
│   └── Localizable.xliff
├── de.xcloc/
│   └── Localizable.xliff
├── fr.xcloc/
│   └── Localizable.xliff
├── ja.xcloc/
│   └── Localizable.xliff
└── ...
```

## 🌐 Supported Languages (100+)

### Major Languages
| Code | Language | Code | Language | Code | Language |
|------|----------|------|----------|------|----------|
| ar | Arabic | hi | Hindi | pt-BR | Portuguese (Brazil) |
| bn | Bengali | hu | Hungarian | ro | Romanian |
| cs | Czech | id | Indonesian | ru | Russian |
| da | Danish | it | Italian | sk | Slovak |
| de | German | ja | Japanese | sv | Swedish |
| el | Greek | ko | Korean | th | Thai |
| en | English | nl | Dutch | tr | Turkish |
| es | Spanish | pl | Polish | uk | Ukrainian |
| fi | Finnish | pt | Portuguese | vi | Vietnamese |
| fr | French | zh-Hans | Chinese (Simplified) | zh-Hant | Chinese (Traditional) |

### Additional Languages
Afrikaans, Albanian, Amharic, Armenian, Azerbaijani, Basque, Belarusian, Bosnian, Bulgarian, Catalan, Cebuano, Chichewa, Corsican, Croatian, Esperanto, Estonian, Filipino, Frisian, Galician, Georgian, Gujarati, Haitian Creole, Hausa, Hawaiian, Hebrew, Hmong, Icelandic, Igbo, Irish, Javanese, Kannada, Kazakh, Khmer, Kurdish, Kyrgyz, Lao, Latin, Latvian, Lithuanian, Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Maori, Marathi, Mongolian, Myanmar, Nepali, Norwegian, Odia, Pashto, Persian, Punjabi, Samoan, Scots Gaelic, Serbian, Sesotho, Shona, Sindhi, Sinhala, Slovenian, Somali, Sundanese, Swahili, Tajik, Tamil, Telugu, Uyghur, Urdu, Uzbek, Welsh, Xhosa, Yiddish, Yoruba, Zulu

**Total: 100+ languages supported for Xcode localization!**

See [LANGUAGE_MAP](localization_app.py) for the complete mapping.

## 🛡️ Translation Features

### What's Preserved
- ✅ **Placeholders**: `%@`, `%d`, `%lld`, `%1$@`, etc.
- ✅ **Units**: kg, lbs, ml, oz, min
- ✅ **Special Characters**: °C, °F, 💧
- ✅ **Formatting**: Punctuation, spacing, newlines
- ✅ **XLIFF Structure**: Valid XML for Xcode

### Translation Logic
The app only translates entries that:
- Have no `<target>` element
- Have empty `<target>` text
- Are marked with `state="needs-review-l10n"`

Already translated entries are **never** overwritten.

## 📋 Requirements

- Python 3.7 or higher
- Internet connection (for Google Translate API)
- macOS/Linux/Windows with Tkinter support

### Dependencies
```
deep-translator>=1.11.4  # Google Translate API
lxml>=4.9.0             # Better XLIFF/XML handling
```

## 🔧 Development

### Project Structure
```
Auto-Translate-localizables/
├── localization_app.py      # GUI application
├── translate_xliff.py        # CLI tool
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── README_TRANSLATION.md     # Detailed CLI docs
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

### Running Tests
```bash
# Test with dry run
python3 translate_xliff.py --dry-run --workspace /path/to/test/folder
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool uses Google Translate API through the `deep-translator` library. Translation quality depends on:
- Google Translate accuracy for the language pair
- Context preservation in short strings
- Placeholder and formatting complexity

Always review translations before production use.

## 🙏 Acknowledgments

- Built with [deep-translator](https://github.com/nidhaloff/deep-translator) for Google Translate integration
- Uses [lxml](https://lxml.de/) for robust XLIFF parsing
- Inspired by the need to streamline iOS app localization

## 📞 Support

If you encounter any issues or have questions:
- Open an [Issue](https://github.com/EhsanAzish80/Auto-Translate-localizables/issues)
- Check the [documentation](README_TRANSLATION.md)
- Review existing issues and discussions

## 🗺️ Roadmap

- [ ] Support for other translation services (DeepL, Azure)
- [ ] Translation memory/cache
- [ ] Batch workspace processing
- [ ] Export translation statistics
- [ ] Custom placeholder patterns
- [ ] Translation quality scoring

---

Made with ❤️ for the localization community
