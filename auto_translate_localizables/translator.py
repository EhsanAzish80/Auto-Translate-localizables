"""
Core translator with strict placeholder preservation and validation.
"""

import re
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    from deep_translator import GoogleTranslator
except ImportError:
    raise ImportError(
        "deep-translator is required. Install with: pip install deep-translator"
    )

try:
    from lxml import etree as ET
    USING_LXML = True
except ImportError:
    import xml.etree.ElementTree as ET
    USING_LXML = False

from .language_map import LANGUAGE_MAP, get_google_translate_code


# Units that should NOT be translated
UNITS = ['kg', 'lbs', 'ml', 'oz', 'min', 'sec', 'hr', 'km', 'mi', 'ft', 'in', 'm', 'cm']

# Placeholder patterns to preserve (iOS/Xcode specific)
PLACEHOLDER_PATTERN = re.compile(
    r'(%[@dlld]+|'           # %@, %d, %lld
    r'%\d+\$[@dlld]+|'       # %1$@, %2$d (positional)
    r'\$\(.*?\)|'            # $(variable)
    r'\{\d+\}|'              # {0}, {1} (format strings)
    r'°[CF]|'                # Temperature units
    r'💧)'                   # Water drop emoji (common in fitness apps)
)


class PlaceholderValidator:
    """Validates that placeholders are preserved during translation."""
    
    @staticmethod
    def extract_placeholders(text: str) -> List[str]:
        """Extract all placeholders from text."""
        return PLACEHOLDER_PATTERN.findall(text)
    
    @staticmethod
    def validate(original: str, translated: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that all placeholders from original appear in translated.
        
        Args:
            original: Original text
            translated: Translated text
            
        Returns:
            (is_valid, error_message)
        """
        original_placeholders = PlaceholderValidator.extract_placeholders(original)
        translated_placeholders = PlaceholderValidator.extract_placeholders(translated)
        
        # Check counts match
        if len(original_placeholders) != len(translated_placeholders):
            return False, (
                f"Placeholder count mismatch: "
                f"original has {len(original_placeholders)}, "
                f"translated has {len(translated_placeholders)}"
            )
        
        # Check all placeholders are preserved (order may differ in some languages)
        original_set = set(original_placeholders)
        translated_set = set(translated_placeholders)
        
        missing = original_set - translated_set
        if missing:
            return False, f"Missing placeholders: {', '.join(missing)}"
        
        extra = translated_set - original_set
        if extra:
            return False, f"Extra placeholders: {', '.join(extra)}"
        
        return True, None


class XLIFFTranslator:
    """Handles translation of XLIFF files with strict validation."""
    
    def __init__(self, workspace_dir: str, fail_on_placeholder_mismatch: bool = True):
        """
        Initialize translator.
        
        Args:
            workspace_dir: Path to workspace containing .xcloc folders
            fail_on_placeholder_mismatch: If True, fail on placeholder validation errors
        """
        self.workspace_dir = Path(workspace_dir)
        self.fail_on_placeholder_mismatch = fail_on_placeholder_mismatch
        self.stats = {}
        self.errors = []
        
    def extract_placeholders(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """Extract placeholders and replace with markers for translation."""
        placeholders = []
        modified_text = text
        
        # Find all placeholders
        matches = list(PLACEHOLDER_PATTERN.finditer(text))
        
        for i, match in enumerate(matches):
            placeholder = match.group(0)
            marker = f"__PH{i}__"  # More distinctive marker
            placeholders.append((marker, placeholder))
            modified_text = modified_text.replace(placeholder, marker, 1)
        
        return modified_text, placeholders
    
    def restore_placeholders(self, text: str, placeholders: List[Tuple[str, str]]) -> str:
        """Restore placeholders in translated text."""
        for marker, placeholder in placeholders:
            text = text.replace(marker, placeholder)
        return text
    
    def should_skip_translation(self, text: str) -> bool:
        """Check if text should be skipped (only placeholders or units)."""
        if not text or not text.strip():
            return True
        
        # Skip if it's only a unit
        if text.strip() in UNITS:
            return True
        
        # Skip if it's just placeholders
        clean_text = PLACEHOLDER_PATTERN.sub('', text).strip()
        if not clean_text or clean_text in ['.', ',', '!', '?', '...', ':', ';']:
            return True
        
        return False
    
    def translate_text(
        self, 
        text: str, 
        target_lang: str, 
        source_lang: str = 'en'
    ) -> Tuple[str, Optional[str]]:
        """
        Translate text while preserving placeholders.
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (default: 'en')
            
        Returns:
            (translated_text, error_message)
        """
        if self.should_skip_translation(text):
            return text, None
        
        # Extract placeholders
        text_to_translate, placeholders = self.extract_placeholders(text)
        
        # Skip if nothing left to translate
        if not text_to_translate.strip():
            return text, None
        
        try:
            # Translate
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            translated = translator.translate(text_to_translate)
            
            # Restore placeholders
            if placeholders:
                translated = self.restore_placeholders(translated, placeholders)
            
            # Validate placeholders are preserved
            is_valid, error = PlaceholderValidator.validate(text, translated)
            if not is_valid:
                error_msg = f"Placeholder validation failed: {error}"
                if self.fail_on_placeholder_mismatch:
                    return text, error_msg  # Return original on validation failure
                else:
                    print(f"  [WARNING] {error_msg}")
            
            return translated, None
            
        except Exception as e:
            error_msg = f"Translation error: {e}"
            return text, error_msg
    
    def process_xliff_file(
        self, 
        xliff_path: Path, 
        target_lang: str,
        source_lang: str = 'en',
        dry_run: bool = False,
        only_missing: bool = False
    ) -> Tuple[int, int]:
        """
        Process a single XLIFF file.
        
        Args:
            xliff_path: Path to XLIFF file
            target_lang: Target language code for Google Translate
            source_lang: Source language code
            dry_run: If True, don't save changes
            only_missing: If True, only translate missing strings
            
        Returns:
            (translated_count, error_count)
        """
        try:
            # Read original content for backup
            with open(xliff_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Parse XML
            if USING_LXML:
                parser = ET.XMLParser(remove_blank_text=False, strip_cdata=False)
                tree = ET.parse(str(xliff_path), parser)
            else:
                ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
                tree = ET.parse(xliff_path)
            
            root = tree.getroot()
            ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}
            
            # Find all trans-units
            trans_units = root.findall('.//xliff:trans-unit', ns)
            
            translated_count = 0
            error_count = 0
            modified = False
            
            for unit in trans_units:
                # Get source text
                source = unit.find('xliff:source', ns)
                if source is None or source.text is None or not source.text.strip():
                    continue
                
                source_text = source.text
                
                # Check for existing target
                target = unit.find('xliff:target', ns)
                
                # Determine if translation is needed
                needs_translation = False
                
                if target is None:
                    needs_translation = True
                    # Create target element
                    if USING_LXML:
                        target = ET.SubElement(unit, '{urn:oasis:names:tc:xliff:document:1.2}target')
                    else:
                        source_index = list(unit).index(source)
                        target = ET.Element('target')
                        unit.insert(source_index + 1, target)
                elif not target.text or target.text.strip() == '':
                    needs_translation = True
                elif target.get('state') == 'needs-review-l10n':
                    needs_translation = True
                elif only_missing and target.text and target.text.strip() == source_text.strip():
                    # Target exists but is the same as source (untranslated) - needs translation
                    needs_translation = True
                elif only_missing:
                    # Skip if we're only doing missing strings and target exists with different content
                    continue
                
                if needs_translation:
                    # Translate
                    translated_text, error = self.translate_text(
                        source_text, target_lang, source_lang
                    )
                    
                    if error:
                        error_count += 1
                        self.errors.append({
                            'file': xliff_path.name,
                            'text': source_text[:50],
                            'error': error
                        })
                    
                    if not dry_run:
                        target.text = translated_text
                        target.set('state', 'translated')
                        modified = True
                    
                    translated_count += 1
                    
                    # Rate limiting - be nice to Google
                    if translated_count % 10 == 0:
                        time.sleep(0.5)
            
            # Save file if modified
            if not dry_run and modified:
                if USING_LXML:
                    tree.write(
                        str(xliff_path),
                        encoding='UTF-8',
                        xml_declaration=True,
                        pretty_print=True
                    )
                else:
                    tree.write(
                        xliff_path,
                        encoding='UTF-8',
                        xml_declaration=True,
                        method='xml'
                    )
                
                # Validate saved file
                try:
                    with open(xliff_path, 'r', encoding='utf-8') as f:
                        test_content = f.read()
                    if '<?xml' not in test_content[:100]:
                        # Restore original if corrupted
                        with open(xliff_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                        return 0, translated_count
                except Exception:
                    # Restore original on error
                    with open(xliff_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    return 0, translated_count
            
            return translated_count, error_count
            
        except Exception as e:
            print(f"  [ERROR] Error processing {xliff_path.name}: {e}")
            # Restore original if we have it
            if 'original_content' in locals():
                try:
                    with open(xliff_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                except Exception:
                    pass
            return 0, 1
    
    def process_language_folder(
        self,
        lang_code: str,
        dry_run: bool = False,
        only_missing: bool = False
    ) -> Dict[str, Tuple[int, int]]:
        """
        Process all XLIFF files in a language folder.
        
        Args:
            lang_code: Language code (e.g., 'de', 'fr', 'zh-Hans')
            dry_run: If True, don't save changes
            only_missing: If True, only translate missing strings
            
        Returns:
            Dictionary mapping file names to (translated_count, error_count)
        """
        lang_folder = self.workspace_dir / f"{lang_code}.xcloc"
        
        if not lang_folder.exists():
            print(f"[WARNING] Folder not found: {lang_folder}")
            return {}
        
        # Get Google Translate code
        target_lang = get_google_translate_code(lang_code)
        if not target_lang:
            print(f"[WARNING] No language mapping for: {lang_code}")
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
            print(f"\n[FILE] {xliff_file.name}")
            translated, errors = self.process_xliff_file(
                xliff_file, target_lang, 'en', dry_run, only_missing
            )
            results[xliff_file.name] = (translated, errors)
            
            status = "✓" if errors == 0 else "⚠"
            print(f"  [{status}] Translated {translated} entries ({errors} errors)")
        
        return results
    
    def process_all_languages(
        self,
        skip_languages: List[str] = None,
        dry_run: bool = False,
        only_missing: bool = False
    ) -> Dict[str, Dict[str, Tuple[int, int]]]:
        """
        Process all language folders in workspace.
        
        Args:
            skip_languages: List of language codes to skip
            dry_run: If True, don't save changes
            only_missing: If True, only translate missing strings
            
        Returns:
            Nested dictionary of results
        """
        skip_languages = skip_languages or ['en']
        
        print(f"\n{'='*60}")
        print(f"XLIFF Bulk Translation")
        print(f"{'='*60}")
        print(f"Workspace: {self.workspace_dir}")
        print(f"Skipping: {', '.join(skip_languages)}")
        print(f"Mode: {'DRY RUN' if dry_run else 'TRANSLATION'}")
        print(f"Only missing: {only_missing}")
        print(f"{'='*60}\n")
        
        # Get all language folders
        lang_folders = [d for d in self.workspace_dir.glob("*.xcloc")]
        
        results = {}
        
        for lang_folder in sorted(lang_folders):
            lang_code = lang_folder.name.replace('.xcloc', '')
            
            if lang_code in skip_languages:
                print(f"[SKIP] {lang_code}")
                continue
            
            try:
                lang_results = self.process_language_folder(
                    lang_code, dry_run, only_missing
                )
                results[lang_code] = lang_results
                time.sleep(1)  # Rate limiting between languages
                
            except Exception as e:
                print(f"[ERROR] Error processing {lang_code}: {e}")
                continue
        
        return results
