#!/usr/bin/env python3
"""
XLIFF Localization Translation App for Xcode
A standalone GUI application for translating Xcode XLIFF localization files.
Auto-detects languages and translates from default language to all available targets.
Works on macOS, Linux, and Windows.
"""

import os
import re
import sys
import time
import threading
import platform
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Check and import GUI library with cross-platform support
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, scrolledtext, messagebox
except ImportError:
    print("\n" + "="*60)
    print("ERROR: Tkinter not found!")
    print("="*60)
    print("\nTkinter is required for the GUI interface.")
    print("\nInstallation instructions:")
    if platform.system() == "Linux":
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  Fedora: sudo dnf install python3-tkinter")
        print("  Arch: sudo pacman -S tk")
    elif platform.system() == "Darwin":
        print("  Tkinter should be included with Python on macOS.")
        print("  Try reinstalling Python from python.org")
    elif platform.system() == "Windows":
        print("  Tkinter should be included with Python on Windows.")
        print("  Try reinstalling Python from python.org")
    print("\nAlternatively, use the CLI version:")
    print("  python3 translate_xliff.py --help")
    print("="*60 + "\n")
    sys.exit(1)

# Check and import translation library
try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("\n" + "="*60)
    print("Installing required dependency: deep-translator")
    print("="*60)
    import subprocess
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'deep-translator'])
        from deep_translator import GoogleTranslator
        print("✓ Successfully installed deep-translator\n")
    except Exception as e:
        print(f"\n✗ Failed to install deep-translator: {e}")
        print("\nPlease install manually:")
        print("  pip3 install deep-translator")
        sys.exit(1)

# Check and import XML parsing library
try:
    from lxml import etree as ET
    USING_LXML = True
except ImportError:
    print("⚠️  lxml not available, using standard xml library")
    print("   For better XLIFF support, install lxml: pip3 install lxml")
    import xml.etree.ElementTree as ET
    USING_LXML = False

# Language code mapping from Xcode locale codes to Google Translate codes
# Supports 100+ languages for maximum coverage
LANGUAGE_MAP = {
    # Common iOS/Xcode locales
    'af': 'af', 'sq': 'sq', 'am': 'am', 'ar': 'ar', 'hy': 'hy', 'az': 'az',
    'eu': 'eu', 'be': 'be', 'bn': 'bn', 'bs': 'bs', 'bg': 'bg', 'ca': 'ca',
    'ceb': 'ceb', 'ny': 'ny', 'zh-Hans': 'zh-CN', 'zh-Hant': 'zh-TW', 
    'co': 'co', 'hr': 'hr', 'cs': 'cs', 'da': 'da', 'nl': 'nl', 'en': 'en',
    'eo': 'eo', 'et': 'et', 'tl': 'tl', 'fi': 'fi', 'fr': 'fr', 'fy': 'fy',
    'gl': 'gl', 'ka': 'ka', 'de': 'de', 'el': 'el', 'gu': 'gu', 'ht': 'ht',
    'ha': 'ha', 'haw': 'haw', 'he': 'he', 'iw': 'iw', 'hi': 'hi', 'hmn': 'hmn',
    'hu': 'hu', 'is': 'is', 'ig': 'ig', 'id': 'id', 'ga': 'ga', 'it': 'it',
    'ja': 'ja', 'jw': 'jw', 'kn': 'kn', 'kk': 'kk', 'km': 'km', 'ko': 'ko',
    'ku': 'ku', 'ky': 'ky', 'lo': 'lo', 'la': 'la', 'lv': 'lv', 'lt': 'lt',
    'lb': 'lb', 'mk': 'mk', 'mg': 'mg', 'ms': 'ms', 'ml': 'ml', 'mt': 'mt',
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

LANGUAGE_NAMES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
    'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
    'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-Hans': 'Chinese (Simplified)',
    'zh-Hant': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
    'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish',
    'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian',
    'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew', 'iw': 'Hebrew',
    'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic',
    'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian',
    'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh',
    'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish', 'ky': 'Kyrgyz',
    'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian',
    'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay',
    'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi',
    'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'nb': 'Norwegian Bokmål', 'or': 'Odia', 'ps': 'Pashto', 'fa': 'Persian',
    'pl': 'Polish', 'pt': 'Portuguese', 'pt-BR': 'Portuguese (Brazil)',
    'pt-PT': 'Portuguese (Portugal)', 'pa': 'Punjabi', 'ro': 'Romanian',
    'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian',
    'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala',
    'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish',
    'es-419': 'Spanish (Latin America)', 'es-US': 'Spanish (US)',
    'es-MX': 'Spanish (Mexico)', 'su': 'Sundanese', 'sw': 'Swahili',
    'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu',
    'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh',
    'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu',
}

UNITS = ['kg', 'lbs', 'ml', 'oz', 'min']
PLACEHOLDER_PATTERN = re.compile(r'(%[@dlld]+|%\d+\$[@dlld]+|\$\(.*?\)|°[CF]|💧)')


class XLIFFTranslator:
    """Core translation engine."""
    
    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        
    def log(self, message: str):
        """Log a message."""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def extract_placeholders(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """Extract placeholders and replace with markers."""
        placeholders = []
        modified_text = text
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
        """Check if text should be skipped."""
        if not text or not text.strip():
            return True
        if text.strip() in UNITS:
            return True
        clean_text = PLACEHOLDER_PATTERN.sub('', text).strip()
        if not clean_text or clean_text in ['.', ',', '!', '?', '...']:
            return True
        return False
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text while preserving placeholders."""
        if self.should_skip_translation(text):
            return text
        
        text_to_translate, placeholders = self.extract_placeholders(text)
        
        if not text_to_translate.strip():
            return text
        
        try:
            translator = GoogleTranslator(source='en', target=target_lang)
            translated = translator.translate(text_to_translate)
            
            if placeholders:
                translated = self.restore_placeholders(translated, placeholders)
            
            return translated
        except Exception as e:
            self.log(f"  ⚠️  Translation error: {e}")
            return text
    
    def process_xliff_file(self, xliff_path: Path, target_lang: str) -> int:
        """Process a single XLIFF file."""
        try:
            with open(xliff_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            if USING_LXML:
                parser = ET.XMLParser(remove_blank_text=False, strip_cdata=False)
                tree = ET.parse(str(xliff_path), parser)
            else:
                ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
                tree = ET.parse(xliff_path)
            
            root = tree.getroot()
            ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}
            trans_units = root.findall('.//xliff:trans-unit', ns)
            
            translated_count = 0
            modified = False
            
            for unit in trans_units:
                source = unit.find('xliff:source', ns)
                if source is None or source.text is None:
                    continue
                
                source_text = source.text
                target = unit.find('xliff:target', ns)
                needs_translation = False
                
                if target is None:
                    needs_translation = True
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
                
                if needs_translation:
                    translated_text = self.translate_text(source_text, target_lang)
                    target.text = translated_text
                    target.set('state', 'translated')
                    modified = True
                    translated_count += 1
                    
                    if translated_count % 10 == 0:
                        self.log(f"    Translated {translated_count} entries...")
                        time.sleep(0.5)
            
            if modified:
                if USING_LXML:
                    tree.write(str(xliff_path), encoding='UTF-8', 
                             xml_declaration=True, pretty_print=True)
                else:
                    tree.write(xliff_path, encoding='UTF-8', 
                             xml_declaration=True, method='xml')
            
            return translated_count
            
        except Exception as e:
            self.log(f"  ❌ Error: {e}")
            return 0
    
    def process_language(self, workspace_dir: Path, lang_code: str, 
                        default_lang: str = 'en') -> int:
        """Process all XLIFF files for a language."""
        lang_folder = workspace_dir / f"{lang_code}.xcloc"
        
        if not lang_folder.exists():
            self.log(f"⚠️  Folder not found: {lang_code}.xcloc")
            return 0
        
        target_lang = LANGUAGE_MAP.get(lang_code)
        if not target_lang:
            self.log(f"⚠️  No language mapping for: {lang_code}")
            return 0
        
        if lang_code == default_lang:
            self.log(f"⏭️  Skipping {lang_code} (default language)")
            return 0
        
        self.log(f"\n{'='*60}")
        self.log(f"🌍 Processing {lang_code.upper()} ({LANGUAGE_NAMES.get(lang_code, lang_code)})")
        self.log(f"{'='*60}")
        
        xliff_files = list(lang_folder.glob("**/*.xliff"))
        
        if not xliff_files:
            self.log(f"  ⚠️  No XLIFF files found")
            return 0
        
        total_count = 0
        for xliff_file in xliff_files:
            self.log(f"\n📄 {xliff_file.name}")
            count = self.process_xliff_file(xliff_file, target_lang)
            total_count += count
            self.log(f"  ✅ Translated {count} entries")
        
        return total_count


class LocalizationApp:
    """Main GUI Application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("XLIFF Localization Translator")
        self.root.geometry("900x700")
        
        self.workspace_dir = None
        self.detected_languages = []
        self.default_language = 'en'
        self.translator = XLIFFTranslator(log_callback=self.log)
        self.is_translating = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface with cross-platform styling."""
        # Configure style for cross-platform consistency
        style = ttk.Style()
        
        # Try to use a native theme based on OS
        available_themes = style.theme_names()
        if platform.system() == "Darwin":  # macOS
            if "aqua" in available_themes:
                style.theme_use("aqua")
        elif platform.system() == "Windows":
            if "vista" in available_themes:
                style.theme_use("vista")
            elif "winnative" in available_themes:
                style.theme_use("winnative")
        else:  # Linux
            if "clam" in available_themes:
                style.theme_use("clam")
        
        # Header
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title = ttk.Label(header_frame, text="XLIFF Localization Translator for Xcode", 
                         font=('Arial', 16, 'bold'))
        title.pack()
        
        subtitle = ttk.Label(header_frame, 
                            text="Auto-detect and translate Xcode localization files (100+ languages)",
                            font=('Arial', 9))
        subtitle.pack()
        
        # Workspace selection
        workspace_frame = ttk.LabelFrame(self.root, text="Workspace", padding="10")
        workspace_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.workspace_label = ttk.Label(workspace_frame, 
                                        text="No workspace selected",
                                        foreground="gray")
        self.workspace_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(workspace_frame, text="Browse...", 
                  command=self.select_workspace).pack(side=tk.RIGHT)
        
        # Language detection
        lang_frame = ttk.LabelFrame(self.root, text="Detected Languages", padding="10")
        lang_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        # Language list
        list_frame = ttk.Frame(lang_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lang_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       selectmode=tk.MULTIPLE, height=6)
        self.lang_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lang_listbox.yview)
        
        # Default language selection
        default_frame = ttk.Frame(lang_frame)
        default_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(default_frame, text="Default Language:").pack(side=tk.LEFT)
        self.default_lang_var = tk.StringVar(value='en')
        self.default_lang_combo = ttk.Combobox(default_frame, 
                                               textvariable=self.default_lang_var,
                                               state='readonly', width=15)
        self.default_lang_combo.pack(side=tk.LEFT, padx=5)
        
        # Translation controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        self.translate_btn = ttk.Button(control_frame, text="🚀 Start Translation",
                                       command=self.start_translation,
                                       state=tk.DISABLED)
        self.translate_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="⏹ Stop",
                                   command=self.stop_translation,
                                   state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="🔄 Refresh",
                  command=self.detect_languages).pack(side=tk.LEFT, padx=5)
        
        # Progress
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X)
        
        # Log output
        log_frame = ttk.LabelFrame(self.root, text="Translation Log", padding="10")
        log_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, 
                                                  font=('Courier', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def log(self, message: str):
        """Add message to log."""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def set_status(self, message: str):
        """Update status bar."""
        self.status_bar.config(text=message)
    
    def select_workspace(self):
        """Open folder browser to select workspace."""
        folder = filedialog.askdirectory(title="Select Localization Workspace")
        if folder:
            self.workspace_dir = Path(folder)
            self.workspace_label.config(text=str(self.workspace_dir), foreground="black")
            self.detect_languages()
    
    def detect_languages(self):
        """Auto-detect available languages in workspace."""
        if not self.workspace_dir:
            messagebox.showwarning("No Workspace", "Please select a workspace first.")
            return
        
        self.log("\n🔍 Detecting languages...")
        
        # Find all .xcloc folders
        xcloc_folders = list(self.workspace_dir.glob("*.xcloc"))
        
        if not xcloc_folders:
            self.log("❌ No .xcloc folders found!")
            messagebox.showerror("Error", "No localization folders (.xcloc) found in workspace.")
            return
        
        # Extract language codes
        self.detected_languages = []
        for folder in sorted(xcloc_folders):
            lang_code = folder.name.replace('.xcloc', '')
            if lang_code in LANGUAGE_MAP:
                self.detected_languages.append(lang_code)
                lang_name = LANGUAGE_NAMES.get(lang_code, lang_code)
                self.log(f"  ✓ Found: {lang_code} ({lang_name})")
        
        # Update UI
        self.lang_listbox.delete(0, tk.END)
        for lang in self.detected_languages:
            lang_name = LANGUAGE_NAMES.get(lang, lang)
            self.lang_listbox.insert(tk.END, f"{lang} - {lang_name}")
        
        # Update default language combo
        self.default_lang_combo['values'] = self.detected_languages
        if 'en' in self.detected_languages:
            self.default_lang_var.set('en')
        elif self.detected_languages:
            self.default_lang_var.set(self.detected_languages[0])
        
        # Select all languages by default (except default)
        for i, lang in enumerate(self.detected_languages):
            if lang != self.default_lang_var.get():
                self.lang_listbox.selection_set(i)
        
        self.log(f"\n✅ Detected {len(self.detected_languages)} languages")
        self.set_status(f"Detected {len(self.detected_languages)} languages")
        self.translate_btn.config(state=tk.NORMAL)
    
    def start_translation(self):
        """Start translation process."""
        selected_indices = self.lang_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select languages to translate.")
            return
        
        selected_langs = [self.detected_languages[i] for i in selected_indices]
        default_lang = self.default_lang_var.get()
        
        # Confirm
        msg = f"Translate from {default_lang} to {len(selected_langs)} language(s)?\n\n"
        msg += "Languages: " + ", ".join(selected_langs)
        
        if not messagebox.askyesno("Confirm Translation", msg):
            return
        
        # Start translation in background thread
        self.is_translating = True
        self.translate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        thread = threading.Thread(target=self.run_translation, 
                                 args=(selected_langs, default_lang))
        thread.daemon = True
        thread.start()
    
    def run_translation(self, languages: List[str], default_lang: str):
        """Run translation (background thread)."""
        try:
            self.log("\n" + "="*60)
            self.log("🚀 STARTING TRANSLATION")
            self.log("="*60)
            
            total_translated = 0
            
            for lang in languages:
                if not self.is_translating:
                    self.log("\n⏹ Translation stopped by user")
                    break
                
                count = self.translator.process_language(
                    self.workspace_dir, lang, default_lang
                )
                total_translated += count
                time.sleep(1)
            
            self.log("\n" + "="*60)
            self.log(f"✨ COMPLETE: {total_translated} total entries translated")
            self.log("="*60 + "\n")
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Translation Complete",
                f"Successfully translated {total_translated} entries!"
            ))
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        finally:
            self.root.after(0, self.translation_finished)
    
    def stop_translation(self):
        """Stop translation process."""
        self.is_translating = False
        self.log("\n⏸ Stopping translation...")
    
    def translation_finished(self):
        """Cleanup after translation."""
        self.is_translating = False
        self.translate_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.set_status("Ready")


def main():
    """Launch the application with cross-platform support."""
    # Print startup info
    print("\n" + "="*60)
    print("XLIFF Localization Translator for Xcode")
    print("="*60)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Using: {'lxml' if USING_LXML else 'standard xml'} for XLIFF parsing")
    print("="*60 + "\n")
    
    # Check dependencies
    print("Checking dependencies...")
    try:
        from deep_translator import GoogleTranslator
        print("✓ deep-translator available")
    except ImportError:
        print("✗ deep-translator not found")
        print("  Installing now...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'deep-translator'])
        print("✓ Installation complete")
    
    print("\nLaunching GUI...\n")
    
    # Create and run the GUI
    root = tk.Tk()
    
    # Set icon if available (cross-platform)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')  # Windows
        # root.iconphoto(True, tk.PhotoImage(file='icon.png'))  # Linux/Mac
        pass
    except:
        pass
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    app = LocalizationApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
