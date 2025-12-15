# 🚀 Quick Start Guide - Xcode XLIFF Translator

## For First-Time Users

### Step 1: Install Dependencies
```bash
pip3 install -r requirements.txt
```

Or use the automated setup:
```bash
./setup.sh
```

### Step 2: Run the App

**Option A: Using the startup script (Recommended)**
```bash
./run.sh
```

**Option B: Direct launch**
```bash
python3 localization_app.py
```

**Option C: Command line mode**
```bash
python3 translate_xliff.py --workspace /path/to/your/xcode/localization
```

## How to Use

### GUI Mode (Recommended for Xcode Projects)

1. **Launch the app**
   - Run `./run.sh` or `python3 localization_app.py`
   - A window will open

2. **Select your workspace**
   - Click "Browse..." button
   - Navigate to your localization folder (the one containing .xcloc folders)
   - Click "Open"

3. **Review detected languages**
   - App automatically scans for .xcloc folders
   - Shows all available languages
   - Select your default/source language (usually English)

4. **Choose target languages**
   - Select which languages you want to translate
   - Hold Cmd (Mac) or Ctrl (Windows/Linux) to select multiple
   - Or Shift+Click to select a range

5. **Start translation**
   - Click "🚀 Start Translation"
   - Watch the progress in the log window
   - Translation happens in the background
   - You can stop anytime with the Stop button

6. **Review results**
   - Check the log for translation statistics
   - Review translated files in your .xcloc folders

### Command Line Mode

**Basic usage:**
```bash
python3 translate_xliff.py --workspace /path/to/localization
```

**Translate only specific languages:**
```bash
python3 translate_xliff.py --only de fr ja
```

**Test without making changes:**
```bash
python3 translate_xliff.py --dry-run
```

**Skip certain languages:**
```bash
python3 translate_xliff.py --skip en ar de
```

## Expected Folder Structure

Your localization workspace should look like this:

```
my-localization/
├── en.xcloc/              ← English (your default language)
│   ├── Localizable.xliff
│   └── Source Contents/
├── de.xcloc/              ← German
│   ├── Localizable.xliff
│   └── Source Contents/
├── fr.xcloc/              ← French
│   ├── Localizable.xliff
│   └── Source Contents/
├── ja.xcloc/              ← Japanese
│   ├── Localizable.xliff
│   └── Source Contents/
└── ...
```

## What Gets Translated?

The app will translate XLIFF entries that:
- ✅ Have no `<target>` element
- ✅ Have an empty `<target>` element
- ✅ Are marked with `state="needs-review-l10n"`

Already translated entries are **skipped** to avoid overwriting your work.

## What's Preserved?

The translation engine preserves:
- ✅ Placeholders: `%@`, `%d`, `%lld`, `%1$@`, etc.
- ✅ Units: kg, lbs, ml, oz, min
- ✅ Special chars: °C, °F, 💧
- ✅ Formatting and punctuation
- ✅ Valid XLIFF/XML structure

## Troubleshooting

### "No .xcloc folders found"
- Make sure you selected the correct workspace folder
- The folder should contain `.xcloc` subfolders
- Check that folder names follow the pattern: `en.xcloc`, `de.xcloc`, etc.

### "Translation error"
- Check your internet connection (required for Google Translate)
- Make sure the XLIFF files are valid XML
- Try translating one language at a time

### "Import error: deep_translator"
- Run: `pip3 install -r requirements.txt`
- Or: `pip3 install deep-translator lxml`

### GUI doesn't open
- Make sure Tkinter is installed (usually comes with Python)
- Try the command line mode instead
- On Linux, you may need: `sudo apt-get install python3-tk`

## Tips

1. **Start with a dry run** to preview what will be translated
2. **Backup your files** before running translations
3. **Translate one language first** to verify the results
4. **Review translations** before committing to production
5. **Use the GUI** for interactive control and monitoring

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review [README_TRANSLATION.md](README_TRANSLATION.md) for CLI options
- Open an issue on GitHub if you encounter problems

---

Happy translating! 🌍
