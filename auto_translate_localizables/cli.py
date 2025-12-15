"""
Command-line interface for auto-translate-xcloc.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

from . import __version__
from .translator import XLIFFTranslator
from .language_map import LANGUAGE_MAP, get_language_name


def print_summary(results: dict):
    """Print translation summary."""
    print(f"\n{'='*60}")
    print(f"TRANSLATION SUMMARY")
    print(f"{'='*60}\n")
    
    total_translations = 0
    total_errors = 0
    
    for lang_code, files in results.items():
        lang_translated = 0
        lang_errors = 0
        
        for filename, (translated, errors) in files.items():
            lang_translated += translated
            lang_errors += errors
        
        total_translations += lang_translated
        total_errors += lang_errors
        
        status = "✓" if lang_errors == 0 else "⚠"
        print(f"[{status}] {lang_code:8} -> {lang_translated:4} translated, {lang_errors:4} errors")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_translations} entries translated")
    print(f"       {total_errors} errors")
    print(f"{'='*60}\n")


def list_languages():
    """List all supported languages."""
    print("\n🌍 Supported Languages\n")
    print(f"{'Code':<12} {'Language':<25} {'Google Code':<12}")
    print("-" * 50)
    
    for code, google_code in sorted(LANGUAGE_MAP.items()):
        name = get_language_name(code)
        print(f"{code:<12} {name:<25} {google_code:<12}")
    
    print(f"\nTotal: {len(LANGUAGE_MAP)} languages supported\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Automate Xcode .xcloc localization with machine translation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate all languages in workspace
  auto-translate-xcloc --workspace /path/to/localization
  
  # Dry run to see what would be translated
  auto-translate-xcloc --workspace /path/to/localization --dry-run
  
  # Only translate missing strings
  auto-translate-xcloc --workspace /path/to/localization --only-missing
  
  # Translate specific languages only
  auto-translate-xcloc --workspace /path/to/localization --only de fr es
  
  # Skip certain languages
  auto-translate-xcloc --workspace /path/to/localization --skip en ar
  
  # Fail on placeholder mismatches (CI mode)
  auto-translate-xcloc --workspace /path/to/localization --fail-on-placeholder-mismatch
  
  # List all supported languages
  auto-translate-xcloc --list-languages

For more information: https://github.com/EhsanAzish80/Auto-Translate-localizables
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'auto-translate-xcloc {__version__}'
    )
    
    parser.add_argument(
        '--workspace', '-w',
        type=str,
        help='Path to localization workspace (directory containing .xcloc folders)'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Perform dry run without saving changes'
    )
    
    parser.add_argument(
        '--only-missing', '-m',
        action='store_true',
        help='Only translate missing strings (skip existing translations)'
    )
    
    parser.add_argument(
        '--skip', '-s',
        nargs='+',
        default=['en'],
        help='Language codes to skip (default: en)'
    )
    
    parser.add_argument(
        '--only', '-o',
        nargs='+',
        help='Only process these language codes'
    )
    
    parser.add_argument(
        '--fail-on-placeholder-mismatch',
        action='store_true',
        help='Exit with error if placeholder validation fails (useful for CI)'
    )
    
    parser.add_argument(
        '--list-languages', '-l',
        action='store_true',
        help='List all supported languages and exit'
    )
    
    args = parser.parse_args()
    
    # Handle --list-languages
    if args.list_languages:
        list_languages()
        return 0
    
    # Validate workspace argument
    if not args.workspace:
        parser.error("--workspace is required (or use --list-languages)")
    
    workspace_path = Path(args.workspace).expanduser().resolve()
    
    if not workspace_path.exists():
        print(f"❌ Error: Workspace not found: {workspace_path}", file=sys.stderr)
        return 1
    
    if not workspace_path.is_dir():
        print(f"❌ Error: Workspace is not a directory: {workspace_path}", file=sys.stderr)
        return 1
    
    # Check for .xcloc folders
    xcloc_folders = list(workspace_path.glob("*.xcloc"))
    if not xcloc_folders:
        print(f"❌ Error: No .xcloc folders found in {workspace_path}", file=sys.stderr)
        print("\nExpected structure:", file=sys.stderr)
        print("  workspace/", file=sys.stderr)
        print("    ├── en.xcloc/", file=sys.stderr)
        print("    ├── de.xcloc/", file=sys.stderr)
        print("    └── fr.xcloc/", file=sys.stderr)
        return 1
    
    # Create translator
    translator = XLIFFTranslator(
        workspace_dir=str(workspace_path),
        fail_on_placeholder_mismatch=args.fail_on_placeholder_mismatch
    )
    
    try:
        if args.only:
            # Process only specified languages
            results = {}
            for lang_code in args.only:
                if lang_code not in LANGUAGE_MAP:
                    print(f"⚠️  Warning: Unknown language code: {lang_code}")
                    continue
                
                lang_results = translator.process_language_folder(
                    lang_code,
                    dry_run=args.dry_run,
                    only_missing=args.only_missing
                )
                if lang_results:
                    results[lang_code] = lang_results
        else:
            # Process all languages
            results = translator.process_all_languages(
                skip_languages=args.skip,
                dry_run=args.dry_run,
                only_missing=args.only_missing
            )
        
        # Print summary
        print_summary(results)
        
        # Check for errors
        if translator.errors:
            print(f"\n⚠️  {len(translator.errors)} validation errors occurred:")
            for error in translator.errors[:10]:  # Show first 10
                print(f"  • {error['file']}: {error['error']}")
            
            if len(translator.errors) > 10:
                print(f"  ... and {len(translator.errors) - 10} more")
            
            if args.fail_on_placeholder_mismatch:
                return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Translation interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
