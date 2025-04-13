import os
import tempfile
from gtts import gTTS
from languages import LANGUAGE_CODES

def text_to_speech(text, language):
    """
    Converts text to speech using gTTS
    
    Args:
        text (str): Text to convert to speech
        language (str): Language name
        
    Returns:
        str: Path to the audio file
        
    Raises:
        Exception: If text-to-speech conversion fails
    """
    try:
        # Convert language name to language code
        lang_code = LANGUAGE_CODES.get(language.lower(), 'en')
        
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()
        
        # Generate speech
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(temp_file.name)
        
        return temp_file.name
    except Exception as e:
        # Log the error for debugging
        print(f"Text-to-speech error: {str(e)}")
        # Re-raise to be handled by the caller
        raise Exception(f"Unable to generate speech: {str(e)}")
