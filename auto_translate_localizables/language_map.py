"""
Explicit language mapping with validation.
Maps Xcode locale codes to Google Translate language codes.
"""

from typing import Optional


# Explicit language mapping: Xcode locale -> Google Translate code
# This prevents Google auto-guess surprises
LANGUAGE_MAP = {
    # A-E
    'af': 'af',      # Afrikaans
    'sq': 'sq',      # Albanian
    'am': 'am',      # Amharic
    'ar': 'ar',      # Arabic
    'hy': 'hy',      # Armenian
    'az': 'az',      # Azerbaijani
    'eu': 'eu',      # Basque
    'be': 'be',      # Belarusian
    'bn': 'bn',      # Bengali
    'bs': 'bs',      # Bosnian
    'bg': 'bg',      # Bulgarian
    'ca': 'ca',      # Catalan
    'ceb': 'ceb',    # Cebuano
    'ny': 'ny',      # Chichewa
    'zh-Hans': 'zh-CN',  # Chinese (Simplified)
    'zh-Hant': 'zh-TW',  # Chinese (Traditional)
    'co': 'co',      # Corsican
    'hr': 'hr',      # Croatian
    'cs': 'cs',      # Czech
    'da': 'da',      # Danish
    'nl': 'nl',      # Dutch
    'en': 'en',      # English
    'eo': 'eo',      # Esperanto
    'et': 'et',      # Estonian
    'tl': 'tl',      # Filipino
    'fi': 'fi',      # Finnish
    'fr': 'fr',      # French
    'fy': 'fy',      # Frisian
    
    # F-L
    'gl': 'gl',      # Galician
    'ka': 'ka',      # Georgian
    'de': 'de',      # German
    'el': 'el',      # Greek
    'gu': 'gu',      # Gujarati
    'ht': 'ht',      # Haitian Creole
    'ha': 'ha',      # Hausa
    'haw': 'haw',    # Hawaiian
    'he': 'he',      # Hebrew
    'iw': 'iw',      # Hebrew (old code)
    'hi': 'hi',      # Hindi
    'hmn': 'hmn',    # Hmong
    'hu': 'hu',      # Hungarian
    'is': 'is',      # Icelandic
    'ig': 'ig',      # Igbo
    'id': 'id',      # Indonesian
    'ga': 'ga',      # Irish
    'it': 'it',      # Italian
    'ja': 'ja',      # Japanese
    'jw': 'jw',      # Javanese
    'kn': 'kn',      # Kannada
    'kk': 'kk',      # Kazakh
    'km': 'km',      # Khmer
    'ko': 'ko',      # Korean
    'ku': 'ku',      # Kurdish
    'ky': 'ky',      # Kyrgyz
    'lo': 'lo',      # Lao
    'la': 'la',      # Latin
    'lv': 'lv',      # Latvian
    'lt': 'lt',      # Lithuanian
    'lb': 'lb',      # Luxembourgish
    'mk': 'mk',      # Macedonian
    'mg': 'mg',      # Malagasy
    'ms': 'ms',      # Malay
    'ml': 'ml',      # Malayalam
    'mt': 'mt',      # Maltese
    
    # M-Z
    'mi': 'mi',      # Maori
    'mr': 'mr',      # Marathi
    'mn': 'mn',      # Mongolian
    'my': 'my',      # Myanmar (Burmese)
    'ne': 'ne',      # Nepali
    'no': 'no',      # Norwegian
    'nb': 'no',      # Norwegian Bokmål -> Norwegian
    'or': 'or',      # Odia
    'ps': 'ps',      # Pashto
    'fa': 'fa',      # Persian
    'pl': 'pl',      # Polish
    'pt': 'pt',      # Portuguese
    'pt-BR': 'pt',   # Portuguese (Brazil) -> Portuguese
    'pt-PT': 'pt',   # Portuguese (Portugal) -> Portuguese
    'pa': 'pa',      # Punjabi
    'ro': 'ro',      # Romanian
    'ru': 'ru',      # Russian
    'sm': 'sm',      # Samoan
    'gd': 'gd',      # Scots Gaelic
    'sr': 'sr',      # Serbian
    'st': 'st',      # Sesotho
    'sn': 'sn',      # Shona
    'sd': 'sd',      # Sindhi
    'si': 'si',      # Sinhala
    'sk': 'sk',      # Slovak
    'sl': 'sl',      # Slovenian
    'so': 'so',      # Somali
    'es': 'es',      # Spanish
    'es-419': 'es',  # Spanish (Latin America) -> Spanish
    'es-US': 'es',   # Spanish (US) -> Spanish
    'es-MX': 'es',   # Spanish (Mexico) -> Spanish
    'su': 'su',      # Sundanese
    'sw': 'sw',      # Swahili
    'sv': 'sv',      # Swedish
    'tg': 'tg',      # Tajik
    'ta': 'ta',      # Tamil
    'te': 'te',      # Telugu
    'th': 'th',      # Thai
    'tr': 'tr',      # Turkish
    'uk': 'uk',      # Ukrainian
    'ur': 'ur',      # Urdu
    'ug': 'ug',      # Uyghur
    'uz': 'uz',      # Uzbek
    'vi': 'vi',      # Vietnamese
    'cy': 'cy',      # Welsh
    'xh': 'xh',      # Xhosa
    'yi': 'yi',      # Yiddish
    'yo': 'yo',      # Yoruba
    'zu': 'zu',      # Zulu
}


# Friendly language names for display
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
    'ha': 'Hausa', 'haw': 'Hawaiian', 'he': 'Hebrew', 'hi': 'Hindi',
    'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo',
    'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
    'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer',
    'ko': 'Korean', 'ku': 'Kurdish', 'ky': 'Kyrgyz', 'lo': 'Lao',
    'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
    'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
    'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian',
    'my': 'Myanmar', 'ne': 'Nepali', 'no': 'Norwegian', 'nb': 'Norwegian Bokmål',
    'or': 'Odia', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish',
    'pt': 'Portuguese', 'pt-BR': 'Portuguese (Brazil)', 'pt-PT': 'Portuguese (Portugal)',
    'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan',
    'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona',
    'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian',
    'so': 'Somali', 'es': 'Spanish', 'es-419': 'Spanish (Latin America)',
    'es-US': 'Spanish (US)', 'es-MX': 'Spanish (Mexico)', 'su': 'Sundanese',
    'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil',
    'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian',
    'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese',
    'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu',
}


def get_google_translate_code(xcode_locale: str) -> Optional[str]:
    """
    Get Google Translate language code for Xcode locale.
    
    Args:
        xcode_locale: Xcode locale code (e.g., 'zh-Hans', 'en', 'pt-BR')
        
    Returns:
        Google Translate language code or None if not supported
    """
    return LANGUAGE_MAP.get(xcode_locale)


def validate_language_code(lang_code: str) -> bool:
    """
    Validate that a language code is supported.
    
    Args:
        lang_code: Language code to validate
        
    Returns:
        True if supported, False otherwise
    """
    return lang_code in LANGUAGE_MAP


def get_language_name(lang_code: str) -> str:
    """
    Get friendly language name for display.
    
    Args:
        lang_code: Language code
        
    Returns:
        Friendly name or the code itself if not found
    """
    return LANGUAGE_NAMES.get(lang_code, lang_code.upper())
