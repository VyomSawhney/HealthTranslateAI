# speech_recognition.py

from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json

def initialize_speech_recognition_models():
    models = {}
    for language_code in ['en', 'es']:
        if language_code == 'en':
            model_path = 'models/vosk/en'
        elif language_code == 'es':
            model_path = 'models/vosk/es'
        else:
            continue
        model = Model(model_path)
        models[language_code] = model  # Store the Model object, not the KaldiRecognizer
    return models

def recognize_speech(model, device_index, is_recording_callable):
    recognizer = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, device=device_index,
                               dtype='int16', channels=1, callback=callback):
            print("#" * 80)
            print('Press Stop Recording button to stop the recording')
            print("#" * 80)
            recognized_text = ''
            while is_recording_callable():
                if not q.empty():
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = recognizer.Result()
                        text = json.loads(result).get('text', '')
                        recognized_text += ' ' + text
                else:
                    sd.sleep(50)  # Wait briefly for more data
            # Process any remaining data
            while not q.empty():
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get('text', '')
                    recognized_text += ' ' + text
            # Get final result
            final_result = recognizer.FinalResult()
            text = json.loads(final_result).get('text', '')
            recognized_text += ' ' + text
            print(f"Recognized Text: {recognized_text}")
            return recognized_text.strip()
    except Exception as e:
        print(f"Error during speech recognition: {str(e)}")
        return None
