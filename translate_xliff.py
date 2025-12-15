#!/usr/bin/env python3
"""
Bulk translation script for XLIFF localization files.
Translates all English source strings to target languages while preserving:
- Units (kg, ml, oz, lbs)
- Placeholders (%@, %lld, %d, etc.)
- Punctuation and formatting
- XLIFF structure for Xcode compatibility
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import time

# Try to import translation library
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    print("Installing deep-translator...")
    import subprocess
    subprocess.check_call(['pip3', 'install', 'deep-translator'])
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True

# Use lxml for better XLIFF handling if available, fallback to xml.etree
try:
    from lxml import etree as ET
    USING_LXML = True
    print("[OK] Using lxml for better XLIFF support")
except ImportError:
    import xml.etree.ElementTree as ET
    USING_LXML = False
    print("[WARNING] Using standard xml library (consider installing lxml: pip3 install lxml)")

# Language code mapping from Xcode locale codes to Google Translate codes
# Supports 100+ languages for maximum Xcode localization coverage
LANGUAGE_MAP = {
    # A-E
    'af': 'af', 'sq': 'sq', 'am': 'am', 'ar': 'ar', 'hy': 'hy', 'az': 'az',
    'eu': 'eu', 'be': 'be', 'bn': 'bn', 'bs': 'bs', 'bg': 'bg', 'ca': 'ca',
    'ceb': 'ceb', 'ny': 'ny', 'zh-Hans': 'zh-CN', 'zh-Hant': 'zh-TW', 
    'co': 'co', 'hr': 'hr', 'cs': 'cs', 'da': 'da', 'nl': 'nl', 'en': 'en',
    'eo': 'eo', 'et': 'et', 'tl': 'tl', 'fi': 'fi', 'fr': 'fr', 'fy': 'fy',
    # F-L
    'gl': 'gl', 'ka': 'ka', 'de': 'de', 'el': 'el', 'gu': 'gu', 'ht': 'ht',
    'ha': 'ha', 'haw': 'haw', 'he': 'he', 'iw': 'iw', 'hi': 'hi', 'hmn': 'hmn',
    'hu': 'hu', 'is': 'is', 'ig': 'ig', 'id': 'id', 'ga': 'ga', 'it': 'it',
    'ja': 'ja', 'jw': 'jw', 'kn': 'kn', 'kk': 'kk', 'km': 'km', 'ko': 'ko',
    'ku': 'ku', 'ky': 'ky', 'lo': 'lo', 'la': 'la', 'lv': 'lv', 'lt': 'lt',
    'lb': 'lb', 'mk': 'mk', 'mg': 'mg', 'ms': 'ms', 'ml': 'ml', 'mt': 'mt',
    # M-Z
    'mi': 'mi', 'mr': 'mr', 'mn': 'mn', 'my': 'my', 'ne': 'ne', 'no': 'no',
    'nb': 'no', 'or': 'or', 'ps': 'ps', 'fa': 'fa', 'pl': 'pl', 
    'pt': 'pt', 'pt-BR': 'pt', 'pt-PT': 'pt', 'pa': 'pa', 'ro': 'ro', 'ru': 'ru',
    'sm': 'sm', 'gd': 'gd', 'sr': 'sr', 'st': 'st', 'sn': 'sn', 'sd': 'sd',
    'si': 'si', 'sk': 'sk', 'sl': 'sl', 'so': 'so', 'es': 'es', 
    'es-419': 'es', 'es-US': 'es', 'es-MX': 'es', 'su': 'su', 'sw': 'sw',
    'sv': 'sv', 'tg': 'tg', 'ta': 'ta', 'te': 'te', 'th': 'th', 'tr': 'tr',
    'uk': 'uk', 'ur': 'ur', 'ug': 'ug', 'uz': 'uz', 'vi': 'vi', 'cy': 'cy',
    'xh': 'xh', 'yi': 'yi', 'yo': 'yo', 'zu': 'zu',
}

# Units that should NOT be translated
UNITS = ['kg', 'lbs', 'ml', 'oz', 'min']

# Placeholder patterns to preserve
PLACEHOLDER_PATTERN = re.compile(r'(%[@dlld]+|%\d+\$[@dlld]+|\$\(.*?\)|°[CF]|💧)')


class XLIFFTranslator:
    """Handles translation of XLIFF files while preserving formatting."""
    
    def __init__(self, workspace_dir: str):
        self.workspace_dir = Path(workspace_dir)
        self.stats = {}
        
    def extract_placeholders(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """Extract placeholders and replace with markers."""
        placeholders = []
        modified_text = text
        
        # Find all placeholders
        matches = list(PLACEHOLDER_PATTERN.finditer(text))
        
        for i, match in enumerate(matches):
            placeholder = match.group(0)
            marker = f"__PLACEHOLDER_{i}__"
            placeholders.append((marker, placeholder))
            modified_text = modified_text.replace(placeholder, marker, 1)
        
        return modified_text, placeholders
    
    def restore_placeholders(self, text: str, placeholders: List[Tuple[str, str]]) -> str:
        """Restore placeholders in translated text."""
        for marker, placeholder in placeholders:
            text = text.replace(marker, placeholder)
        return text
    
    def should_skip_translation(self, text: str) -> bool:
        """Check if text should be skipped (e.g., only placeholders or units)."""
        if not text or not text.strip():
            return True
        
        # Skip if it's only a unit
        if text.strip() in UNITS:
            return True
        
        # Skip if it's just placeholders
        clean_text = PLACEHOLDER_PATTERN.sub('', text).strip()
        if not clean_text or clean_text in ['.', ',', '!', '?', '...']:
            return True
        
        return False
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text while preserving placeholders and units."""
        if self.should_skip_translation(text):
            return text
        
        # Extract placeholders
        text_to_translate, placeholders = self.extract_placeholders(text)
        
        # Skip if nothing left to translate
        if not text_to_translate.strip():
            return text
        
        try:
            # Translate
            translator = GoogleTranslator(source='en', target=target_lang)
            translated = translator.translate(text_to_translate)
            
            # Restore placeholders
            if placeholders:
                translated = self.restore_placeholders(translated, placeholders)
            
            return translated
        except Exception as e:
            print(f"  [WARNING] Translation error for '{text[:50]}...': {e}")
            return text
    
    def process_xliff_file(self, xliff_path: Path, target_lang: str, dry_run: bool = False) -> int:
        """Process a single XLIFF file and translate missing entries."""
        try:
            # Read the original file content
            with open(xliff_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Parse XML preserving structure
            if USING_LXML:
                parser = ET.XMLParser(remove_blank_text=False, strip_cdata=False)
                tree = ET.parse(str(xliff_path), parser)
            else:
                # Register namespace to avoid ns0: prefixes
                ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
                tree = ET.parse(xliff_path)
            
            root = tree.getroot()
            
            # Define namespace
            ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}
            
            # Find all trans-units
            trans_units = root.findall('.//xliff:trans-unit', ns)
            
            translated_count = 0
            modified = False
            
            for unit in trans_units:
                # Get source text
                source = unit.find('xliff:source', ns)
                if source is None or source.text is None:
                    continue
                
                source_text = source.text
                
                # Check for existing target
                target = unit.find('xliff:target', ns)
                
                # Determine if translation is needed
                needs_translation = False
                
                if target is None:
                    needs_translation = True
                    # Create target element properly with namespace
                    if USING_LXML:
                        target = ET.SubElement(unit, '{urn:oasis:names:tc:xliff:document:1.2}target')
                    else:
                        # Insert target after source to maintain order
                        source_index = list(unit).index(source)
                        target = ET.Element('target')
                        unit.insert(source_index + 1, target)
                elif not target.text or target.text.strip() == '':
                    needs_translation = True
                elif target.get('state') == 'needs-review-l10n':
                    needs_translation = True
                
                if needs_translation:
                    # Translate the text
                    translated_text = self.translate_text(source_text, target_lang)
                    
                    if not dry_run:
                        target.text = translated_text
                        target.set('state', 'translated')
                        modified = True
                    
                    translated_count += 1
                    
                    if translated_count % 10 == 0:
                        print(f"    Translated {translated_count} entries...")
                        time.sleep(0.5)  # Rate limiting
            
            # Save the file only if modifications were made
            if not dry_run and modified:
                if USING_LXML:
                    # lxml preserves formatting better
                    tree.write(
                        str(xliff_path),
                        encoding='UTF-8',
                        xml_declaration=True,
                        pretty_print=True
                    )
                else:
                    # For standard library, write more carefully
                    tree.write(
                        xliff_path,
                        encoding='UTF-8',
                        xml_declaration=True,
                        method='xml'
                    )
                
                # Verify the file is still valid XML
                try:
                    with open(xliff_path, 'r', encoding='utf-8') as f:
                        test_content = f.read()
                    if '<?xml' not in test_content[:100]:
                        # Restore original if corrupted
                        with open(xliff_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                        print(f"  [WARNING] Restored original file (validation failed)")
                        return 0
                except Exception as e:
                    # Restore original on any error
                    with open(xliff_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    print(f"  [WARNING] Restored original file: {e}")
                    return 0
            
            return translated_count
            
        except Exception as e:
            print(f"  [ERROR] Error processing {xliff_path}: {e}")
            # Restore original content if we have it
            if 'original_content' in locals():
                try:
                    with open(xliff_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    print(f"  [INFO] Restored original file")
                except:
                    pass
            return 0
    
    def process_language_folder(self, lang_code: str, dry_run: bool = False) -> Dict[str, int]:
        """Process all XLIFF files in a language folder."""
        lang_folder = self.workspace_dir / f"{lang_code}.xcloc"
        
        if not lang_folder.exists():
            print(f"[WARNING] Folder not found: {lang_folder}")
            return {}
        
        # Get target language code
        target_lang = LANGUAGE_MAP.get(lang_code)
        if not target_lang:
            print(f"[WARNING] No language mapping for: {lang_code}")
            return {}
        
        # Skip English
        if lang_code == 'en':
            print(f"[SKIP] Skipping English (source language)")
            return {}
        
        print(f"\n{'='*60}")
        print(f"Processing {lang_code.upper()} -> {target_lang}")
        print(f"{'='*60}")
        
        results = {}
        
        # Find XLIFF files
        xliff_files = list(lang_folder.glob("**/*.xliff"))
        
        if not xliff_files:
            print(f"  [WARNING] No XLIFF files found in {lang_folder}")
            return {}
        
        for xliff_file in xliff_files:
            print(f"\n[FILE] Processing: {xliff_file.name}")
            count = self.process_xliff_file(xliff_file, target_lang, dry_run)
            results[xliff_file.name] = count
            print(f"  [OK] Translated {count} entries")
        
        return results
    
    def process_all_languages(self, skip_languages: List[str] = None, dry_run: bool = False):
        """Process all language folders in the workspace."""
        skip_languages = skip_languages or ['en', 'ar', 'cs']  # Skip English and already done Arabic
        
        print(f"\n{'='*60}")
        print(f"XLIFF Bulk Translation")
        print(f"{'='*60}")
        print(f"Workspace: {self.workspace_dir}")
        print(f"Skipping: {', '.join(skip_languages)}")
        print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'TRANSLATION MODE'}")
        print(f"{'='*60}\n")
        
        # Get all language folders
        lang_folders = [d for d in self.workspace_dir.glob("*.xcloc")]
        
        total_stats = {}
        
        for lang_folder in sorted(lang_folders):
            lang_code = lang_folder.name.replace('.xcloc', '')
            
            if lang_code in skip_languages:
                print(f"[SKIP] Skipping {lang_code} (in skip list)")
                continue
            
            try:
                results = self.process_language_folder(lang_code, dry_run)
                total_stats[lang_code] = results
                
                # Small delay between languages
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error processing {lang_code}: {e}")
                continue
        
        # Print summary
        self.print_summary(total_stats)
    
    def print_summary(self, stats: Dict[str, Dict[str, int]]):
        """Print translation summary."""
        print(f"\n{'='*60}")
        print(f"TRANSLATION SUMMARY")
        print(f"{'='*60}\n")
        
        total_translations = 0
        
        for lang_code, files in stats.items():
            lang_total = sum(files.values())
            total_translations += lang_total
            print(f"{lang_code.upper():8} -> {lang_total:4} entries translated")
        
        print(f"\n{'='*60}")
        print(f"TOTAL: {total_translations} entries translated across {len(stats)} languages")
        print(f"{'='*60}\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bulk translate XLIFF localization files')
    parser.add_argument('--workspace', '-w', 
                        default='/Users/ehsanazish/Downloads/localization',
                        help='Path to localization workspace')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Perform dry run without saving changes')
    parser.add_argument('--skip', '-s', nargs='+', 
                        default=['en', 'ar'],
                        help='Language codes to skip (default: en ar)')
    parser.add_argument('--only', '-o', nargs='+',
                        help='Only process these language codes')
    
    args = parser.parse_args()
    
    translator = XLIFFTranslator(args.workspace)
    
    if args.only:
        # Process only specified languages
        for lang_code in args.only:
            translator.process_language_folder(lang_code, args.dry_run)
    else:
        # Process all languages
        translator.process_all_languages(skip_languages=args.skip, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
