# XLIFF Bulk Translation Script

This Python script automates the translation of XLIFF localization files for all languages while carefully preserving:
- ✅ Units (kg, ml, oz, lbs) - NOT translated
- ✅ Placeholders (%@, %lld, %d, etc.) - Preserved in exact positions
- ✅ Punctuation and formatting
- ✅ Special characters (°C, °F, 💧)

## Installation

```bash
# Install dependencies
pip3 install -r requirements.txt
```

## Usage

### 1. Dry Run (Preview Mode)
Test the script without making changes:
```bash
python3 translate_xliff.py --dry-run
```

### 2. Translate All Languages
Translate all languages except English and Arabic (already done):
```bash
python3 translate_xliff.py
```

### 3. Translate Specific Languages
Translate only specific languages:
```bash
# Translate only German and French
python3 translate_xliff.py --only de fr

# Translate only Japanese
python3 translate_xliff.py --only ja
```

### 4. Custom Skip List
Skip specific languages:
```bash
python3 translate_xliff.py --skip en ar de
```

### 5. Custom Workspace Path
Specify a different workspace directory:
```bash
python3 translate_xliff.py --workspace /path/to/your/localization
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--workspace` | `-w` | Path to localization workspace | `/Users/ehsanazish/Downloads/localization` |
| `--dry-run` | `-d` | Preview mode (no changes) | False |
| `--skip` | `-s` | Languages to skip | `en ar` |
| `--only` | `-o` | Only process these languages | None |

## Supported Languages

The script supports 30+ languages:
- Arabic (ar) ✅ Already done
- Czech (cs)
- Danish (da)
- German (de)
- Greek (el)
- Spanish (es, es-419, es-US)
- Finnish (fi)
- French (fr)
- Hindi (hi)
- Indonesian (id)
- Italian (it)
- Japanese (ja)
- Korean (ko)
- Dutch (nl)
- Polish (pl)
- Portuguese (pt-BR, pt-PT)
- Romanian (ro)
- Russian (ru)
- Slovak (sk)
- Swedish (sv)
- Thai (th)
- Turkish (tr)
- Ukrainian (uk)
- Vietnamese (vi)
- Chinese Simplified (zh-Hans)
- Chinese Traditional (zh-Hant)

## How It Works

1. **Scans** each `.xcloc` folder for XLIFF files
2. **Identifies** entries needing translation:
   - Entries with no `<target>` element
   - Entries with empty `<target>`
   - Entries with `state="needs-review-l10n"`
3. **Extracts** placeholders before translation
4. **Translates** using Google Translate API
5. **Restores** placeholders in exact positions
6. **Updates** XLIFF files with `state="translated"`

## Example Output

```
============================================================
🚀 XLIFF Bulk Translation
============================================================
Workspace: /Users/ehsanazish/Downloads/localization
Skipping: en, ar
Mode: TRANSLATION MODE
============================================================

============================================================
🌍 Processing CS → cs
============================================================

📄 Processing: cs.xliff
    Translated 10 entries...
    Translated 20 entries...
  ✅ Translated 247 entries

============================================================
📊 TRANSLATION SUMMARY
============================================================

CS       →  247 entries translated
DE       →  251 entries translated
FR       →  245 entries translated
...
============================================================
✨ TOTAL: 6,847 entries translated across 28 languages
============================================================
```

## Safety Features

- **Dry run mode** to preview changes
- **Placeholder preservation** ensures app won't crash
- **Unit preservation** keeps measurements readable
- **Rate limiting** to avoid API throttling
- **Error handling** continues even if one file fails

## Troubleshooting

### Import Error
If you get an import error for `deep-translator`:
```bash
pip3 install deep-translator
```

### Permission Error
If you can't write to files:
```bash
chmod +w *.xcloc/Localized\ Contents/*.xliff
```

### Rate Limiting
If you hit API rate limits, the script includes automatic delays. For large batches, consider:
- Running overnight
- Processing in smaller batches with `--only`

## Notes

⚠️ **Backup First**: Always backup your localization files before running in non-dry-run mode

✅ **Arabic Complete**: The ar.xcloc translation is already complete and will be skipped

🔄 **Re-runnable**: Safe to run multiple times - only translates missing entries

📝 **Manual Review**: Always review translations for context and cultural appropriateness
