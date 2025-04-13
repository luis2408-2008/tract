from googletrans import Translator
from languages import LANGUAGE_CODES

def translate_text(text, source_lang, target_lang):
    """
    Translates text from source language to target language
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language name
        target_lang (str): Target language name
        
    Returns:
        str: Translated text
        
    Raises:
        Exception: If translation fails
    """
    # If no text is provided, return empty string
    if not text or text.strip() == "":
        return ""
        
    try:
        # Convert language names to language codes
        source_code = LANGUAGE_CODES.get(source_lang.lower(), 'auto')
        target_code = LANGUAGE_CODES.get(target_lang.lower(), 'en')
        
        # Initialize translator
        translator = Translator()
        
        # Perform translation
        result = translator.translate(
            text, 
            src=source_code, 
            dest=target_code
        )
        
        # Return the translated text
        return result.text
    except Exception as e:
        # Log the error for debugging
        print(f"Translation error: {str(e)}")
        # Re-raise to be handled by the caller
        raise Exception(f"Unable to translate: {str(e)}")
