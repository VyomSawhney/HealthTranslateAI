# text_to_speech.py

import threading
import pyttsx3

def speak_text(text, language_code, tts_speed=1.0):
    threading.Thread(target=_speak_text, args=(text, language_code, tts_speed)).start()

def _speak_text(text, language_code, tts_speed):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Map language codes to voice IDs (Adjust based on available voices)
    language_voice_map = {
        'en': 'english',
        'es': 'spanish',
    }

    selected_voice = None
    for voice in voices:
        if language_voice_map[language_code] in voice.name.lower():
            selected_voice = voice.id
            break

    if selected_voice:
        engine.setProperty('voice', selected_voice)
    else:
        print(f"No voice found for language code: {language_code}")

    # Set speech rate
    default_rate = engine.getProperty('rate')  # Get the default rate
    engine.setProperty('rate', int(default_rate * tts_speed))

    # Speak the text directly
    engine.say(text)
    engine.runAndWait()
