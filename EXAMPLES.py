#!/usr/bin/env python3
"""
Example Usage Scripts for XLIFF Localization Translator
This file demonstrates various ways to use the translation tools.
"""

# ============================================================================
# EXAMPLE 1: Using the GUI (Recommended for most users)
# ============================================================================

"""
Simply run:
    python3 localization_app.py

Or use the launcher:
    ./run.sh

Then:
1. Click "Browse..." to select your localization folder
2. App automatically detects all .xcloc folders
3. Select languages you want to translate
4. Choose your default/source language (usually English)
5. Click "🚀 Start Translation"
6. Monitor progress in the log window
"""

# ============================================================================
# EXAMPLE 2: Command Line - Translate All Languages
# ============================================================================

"""
Translate all languages except English and Arabic:

    python3 translate_xliff.py --workspace /path/to/localization

This will:
- Scan all .xcloc folders
- Skip English (source) and Arabic (already done)
- Translate all other languages from English
- Update XLIFF files with translations
"""

# ============================================================================
# EXAMPLE 3: Translate Specific Languages Only
# ============================================================================

"""
Translate only German, French, and Japanese:

    python3 translate_xliff.py --only de fr ja

Or with custom workspace:

    python3 translate_xliff.py \\
        --workspace /path/to/localization \\
        --only de fr ja
"""

# ============================================================================
# EXAMPLE 4: Dry Run (Preview Mode)
# ============================================================================

"""
Test the translation without making any changes:

    python3 translate_xliff.py --dry-run

This will:
- Scan all files
- Show what would be translated
- NOT save any changes
- Perfect for testing before running actual translation
"""

# ============================================================================
# EXAMPLE 5: Custom Skip List
# ============================================================================

"""
Skip specific languages:

    python3 translate_xliff.py --skip en ar de fr

This will translate all languages EXCEPT:
- en (English)
- ar (Arabic)
- de (German)
- fr (French)
"""

# ============================================================================
# EXAMPLE 6: Programmatic Usage
# ============================================================================

from pathlib import Path
from translate_xliff import XLIFFTranslator

def translate_workspace(workspace_path, languages_to_translate):
    """
    Programmatically translate specific languages.
    
    Args:
        workspace_path: Path to the localization workspace
        languages_to_translate: List of language codes to translate
    """
    translator = XLIFFTranslator(workspace_path)
    
    for lang_code in languages_to_translate:
        print(f"\\nTranslating {lang_code}...")
        results = translator.process_language_folder(lang_code)
        print(f"Completed: {sum(results.values())} entries translated")

# Usage:
# translate_workspace('/path/to/localization', ['de', 'fr', 'ja'])


# ============================================================================
# EXAMPLE 7: Batch Processing Multiple Workspaces
# ============================================================================

def batch_translate_projects(projects):
    """
    Translate multiple projects in batch.
    
    Args:
        projects: Dictionary of {project_name: workspace_path}
    """
    from translate_xliff import XLIFFTranslator
    
    for project_name, workspace_path in projects.items():
        print(f"\\n{'='*60}")
        print(f"Processing: {project_name}")
        print(f"{'='*60}")
        
        translator = XLIFFTranslator(workspace_path)
        translator.process_all_languages(skip_languages=['en'])
        
        print(f"\\n✓ Completed {project_name}")

# Usage:
# projects = {
#     'iOS App': '/path/to/ios/localization',
#     'macOS App': '/path/to/macos/localization',
# }
# batch_translate_projects(projects)


# ============================================================================
# EXAMPLE 8: Integration with CI/CD
# ============================================================================

"""
In your CI/CD pipeline (e.g., GitHub Actions):

    - name: Translate Localization Files
      run: |
        pip3 install -r requirements.txt
        python3 translate_xliff.py \\
          --workspace ./localization \\
          --skip en
        
        # Commit changes
        git config user.name "Translation Bot"
        git config user.email "bot@example.com"
        git add localization/*.xcloc
        git commit -m "Auto-translate localization files" || echo "No changes"
        git push
"""

# ============================================================================
# EXAMPLE 9: Custom Translation Workflow
# ============================================================================

def custom_translation_workflow():
    """
    Example of a custom translation workflow with validation.
    """
    from pathlib import Path
    from translate_xliff import XLIFFTranslator
    
    workspace = Path('/path/to/localization')
    translator = XLIFFTranslator(workspace)
    
    # Step 1: Identify languages needing translation
    lang_folders = list(workspace.glob('*.xcloc'))
    languages = [f.name.replace('.xcloc', '') for f in lang_folders]
    
    print(f"Found {len(languages)} languages: {', '.join(languages)}")
    
    # Step 2: Translate each language
    translation_stats = {}
    
    for lang in languages:
        if lang == 'en':  # Skip source language
            continue
        
        print(f"\\nProcessing {lang}...")
        
        try:
            results = translator.process_language_folder(lang, dry_run=False)
            translation_stats[lang] = sum(results.values())
            print(f"  ✓ Translated {translation_stats[lang]} entries")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            translation_stats[lang] = 0
    
    # Step 3: Generate report
    print(f"\\n{'='*60}")
    print("TRANSLATION REPORT")
    print(f"{'='*60}")
    
    for lang, count in sorted(translation_stats.items()):
        print(f"{lang:10} → {count:5} entries")
    
    total = sum(translation_stats.values())
    print(f"\\nTOTAL: {total} entries translated")
    
    return translation_stats

# ============================================================================
# EXAMPLE 10: Error Handling and Logging
# ============================================================================

import logging

def translate_with_logging(workspace_path, languages):
    """
    Translate with comprehensive logging.
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('translation.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    from translate_xliff import XLIFFTranslator
    
    translator = XLIFFTranslator(workspace_path)
    
    for lang in languages:
        logger.info(f"Starting translation for {lang}")
        
        try:
            results = translator.process_language_folder(lang)
            total = sum(results.values())
            logger.info(f"Completed {lang}: {total} entries translated")
        except Exception as e:
            logger.error(f"Failed to translate {lang}: {e}", exc_info=True)

# Usage:
# translate_with_logging('/path/to/localization', ['de', 'fr', 'ja'])


# ============================================================================
# TIPS AND BEST PRACTICES
# ============================================================================

"""
1. ALWAYS backup your localization files before translating
2. Start with --dry-run to preview changes
3. Translate one language first to verify results
4. Review automated translations before production
5. Keep English (or your source language) clean and clear
6. Use meaningful context in your source strings
7. Consider translation quality for critical user-facing text
8. Test translated apps before release

REMEMBER:
- Automated translation is a starting point, not a replacement for human review
- Context matters - short strings may not translate well
- Review placeholders and formatting in translated strings
- Test your app in each language
"""

if __name__ == '__main__':
    print(__doc__)
    print("\\nSee the examples above for various usage patterns.")
    print("Run: python3 translate_xliff.py --help")
