import streamlit as st
import base64
import time
from translator import translate_text
from audio import text_to_speech
from languages import LANGUAGES

# Set page config
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="wide"
)

# Initialize session state variables if they don't exist
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "last_translation" not in st.session_state:
    st.session_state.last_translation = {"text": "", "src": "", "dest": ""}
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translate_error" not in st.session_state:
    st.session_state.translate_error = None

def on_text_change():
    """Auto-translate text as it's being typed"""
    try:
        if st.session_state.input_text.strip():
            result = translate_text(
                st.session_state.input_text,
                st.session_state.source_lang,
                st.session_state.target_lang
            )
            
            # Check if result contains an error message
            if result.startswith("Error:"):
                st.session_state.translate_error = result
                print(f"Translation error: {result}")
                # Keep previous translation if there's an error
                if "last_translation" in st.session_state and st.session_state.last_translation["text"]:
                    st.session_state.translated_text = st.session_state.last_translation["text"]
                else:
                    st.session_state.translated_text = ""
            else:
                st.session_state.translated_text = result
                st.session_state.last_translation = {
                    "text": result,
                    "src": st.session_state.source_lang,
                    "dest": st.session_state.target_lang
                }
                st.session_state.translate_error = None
        else:
            st.session_state.translated_text = ""
            st.session_state.translate_error = None
        
        # Remove any previous audio when text changes
        st.session_state.audio_path = None
    except Exception as e:
        st.session_state.translate_error = f"Error inesperado: {str(e)}"
        print(f"Translation error: {str(e)}")

def on_lang_change():
    """Re-translate when language changes"""
    on_text_change()

def generate_audio():
    """Function to generate audio from translated text"""
    if st.session_state.translated_text:
        with st.spinner("Generating audio..."):
            try:
                audio_path = text_to_speech(
                    st.session_state.translated_text,
                    st.session_state.target_lang
                )
                st.session_state.audio_path = audio_path
                return True
            except Exception as e:
                st.error(f"Audio generation error: {str(e)}")
                return False
    else:
        st.warning("No translated text to convert to speech")
        return False

def get_audio_html():
    """Return HTML for audio player with autoplay"""
    audio_file = open(st.session_state.audio_path, "rb")
    audio_bytes = audio_file.read()
    audio_file.close()
    
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay controls>
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    """
    return audio_html

def copy_to_clipboard():
    """Function to copy the translated text"""
    if st.session_state.translated_text:
        # Using JavaScript to copy to clipboard via HTML component
        copy_js = f"""
        <script>
        navigator.clipboard.writeText("{st.session_state.translated_text}");
        </script>
        """
        st.components.v1.html(copy_js, height=0)
        st.success("Copied to clipboard!")
        time.sleep(1)
        st.success("Translation copied!")

# Custom CSS to improve the appearance
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .translator-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .translator-header img {
        margin-right: 1rem;
    }
    .translation-area {
        margin-top: 1rem;
    }
    .stButton button {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App header with improved styling
st.markdown("""
<div class="translator-header">
    <img src="https://www.svgrepo.com/show/13656/earth-globe.svg" width="50" height="50" alt="Globe Icon">
    <h1>Language Translator</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("Translate text between different languages with speech functionality")

# Create two columns for source and target language selection
col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "From",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index("English"),
        key="source_lang",
        on_change=on_lang_change
    )

with col2:
    st.selectbox(
        "To",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index("Spanish"),
        key="target_lang",
        on_change=on_lang_change
    )

# Text input area for original text
st.text_area(
    "Enter text to translate",
    height=150,
    key="input_text",
    on_change=on_text_change
)

# Show error message if translation failed
if st.session_state.translate_error:
    st.error(f"Translation error: {st.session_state.translate_error}")

# Automatically show the output section
st.markdown("### Translation")

# Display translated text
st.text_area(
    "Translated text",
    value=st.session_state.translated_text,
    height=150,
    disabled=True,
    key="output_text"
)

# Action buttons in columns
col1, col2 = st.columns(2)

with col1:
    if st.button("🔊 Listen", use_container_width=True):
        success = generate_audio()
        if success:
            st.markdown(get_audio_html(), unsafe_allow_html=True)

with col2:
    if st.button("📋 Copy", use_container_width=True):
        copy_to_clipboard()

# Display audio player if audio has been generated
if st.session_state.audio_path:
    with st.expander("Audio Player", expanded=True):
        st.markdown(get_audio_html(), unsafe_allow_html=True)

# Footer with app info
st.markdown("---")
st.markdown("Powered by Streamlit, googletrans, and gTTS")
