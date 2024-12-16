import os
import gettext
from fastapi import Request

# Supported languages
SUPPORTED_LANGUAGES = ["en", "fr"]
DEFAULT_LANGUAGE = "en"

# Locate the locales directory (adjust path as needed)
LOCALES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "locales")

# A dictionary to hold translation objects
translations = {
    lang: gettext.translation("messages", LOCALES_DIR, languages=[lang], fallback=True)
    for lang in SUPPORTED_LANGUAGES
}

def get_preferred_language(request: Request) -> str:
    """
    Determine the preferred language of the user.
    For example, we can check a query parameter 'lang',
    or use the Accept-Language header.
    """
    # Try query parameter first
    lang = request.query_params.get("lang")
    if lang and lang in SUPPORTED_LANGUAGES:
        return lang

    # Fallback to Accept-Language header
    accept_lang = request.headers.get("Accept-Language", "")
    for supported in SUPPORTED_LANGUAGES:
        if supported in accept_lang:
            return supported

    # Default
    return DEFAULT_LANGUAGE

def translate_message(msg: str, lang: str) -> str:
    """
    Translate a given message using the chosen language.
    """
    return translations.get(lang, translations[DEFAULT_LANGUAGE]).gettext(msg)

def _(request: Request, msg: str) -> str:
    """
    Shortcut function to translate messages within route handlers.
    """
    lang = request.state.language if hasattr(request.state, 'language') else DEFAULT_LANGUAGE
    return translate_message(msg, lang)
