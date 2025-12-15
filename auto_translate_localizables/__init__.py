"""
auto-translate-localizables

Automates Xcode .xcloc localization using reproducible, CI-friendly machine translation.
Built for real iOS teams.
"""

__version__ = "1.0.0"
__author__ = "Ehsan Azish"
__license__ = "MIT"

from .translator import XLIFFTranslator, PlaceholderValidator
from .language_map import LANGUAGE_MAP, get_google_translate_code, validate_language_code

__all__ = [
    "XLIFFTranslator",
    "PlaceholderValidator",
    "LANGUAGE_MAP",
    "get_google_translate_code",
    "validate_language_code",
]
