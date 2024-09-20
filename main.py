# main.py

import tkinter as tk
from ui import TranslatorUI
from speech_recognition import initialize_speech_recognition_models, recognize_speech
from translation import load_translation_models, translate_text
from text_to_speech import speak_text
import threading


class TranslatorApp(TranslatorUI):
    def __init__(self, master):
        super().__init__(master)
        # Initialize models
        self.speech_rec_models = initialize_speech_recognition_models()
        self.translation_models = load_translation_models()
        self.is_recording = False
        self.recognized_text = ""
        self.audio_queue = []
        self.recording_thread = None

        # Initialize selected input device
        self.selected_input_device = self.get_input_device_index()

        # Initialize TTS speed
        self.tts_speed = self.tts_speed_var.get()

    def apply_settings(self):
        # Update selected input device based on user selection
        self.selected_input_device = self.get_input_device_index()
        # Update TTS speed
        self.tts_speed = self.tts_speed_var.get()
        self._update_status("Settings applied.")

    def get_input_device_index(self):
        input_device_name = self.input_device_var.get()
        input_device = next((device for device in self.input_devices if device['name'] == input_device_name), None)
        input_device_index = self.input_devices.index(input_device) if input_device else sd.default.device[0]
        return input_device_index

    def start_translation(self):
        if self.is_recording:
            return
        self.is_recording = True
        self._update_status("Recording...")
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

        # Run recording in a separate thread
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def stop_translation(self):
        if not self.is_recording:
            return
        self.is_recording = False
        self._update_status("Processing...")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

        # Wait for the recording thread to finish
        if self.recording_thread is not None:
            self.recording_thread.join()

        # Run translation in a separate thread
        threading.Thread(target=self._translate).start()

    def _record_audio(self):
        src_lang = self.src_lang.get()
        model = self.speech_rec_models.get(src_lang)
        if model is None:
            self._update_output_text("Speech recognition model not found.")
            self.is_recording = False
            return

        self.recognized_text = recognize_speech(model, self.selected_input_device, lambda: self.is_recording)
        self.is_recording = False

    def _translate(self):
        src_lang = self.src_lang.get()
        tgt_lang = self.tgt_lang.get()

        if not self.recognized_text:
            self._update_output_text("Could not recognize speech.")
            self._update_status("Ready")
            return

        # Step 2: Translation
        tokenizer_model = self.translation_models.get((src_lang, tgt_lang))
        if tokenizer_model is None:
            self._update_output_text("Translation model not found.")
            self._update_status("Ready")
            return

        tokenizer, model = tokenizer_model
        translated_text = translate_text(self.recognized_text, tokenizer, model)

        # Display Translated Text
        self._update_output_text(translated_text)

        # Step 3: Text-to-Speech
        speak_text(translated_text, tgt_lang, self.tts_speed)
        self._update_status("Ready")

    def _update_status(self, message):
        self.status_label.after(0, self.status_label.config, {'text': message})

    def _update_output_text(self, text):
        # Update the UI in the main thread
        self.output_text.after(0, self._insert_text, text)

    def _insert_text(self, text):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
