# ui.py

import tkinter as tk
from tkinter import ttk
import sounddevice as sd

class TranslatorUI:
    def __init__(self, master):
        self.master = master
        master.title("Local AI Translator")

        # Create Notebook (Tab control)
        self.notebook = ttk.Notebook(master)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Create Frames for each tab
        self.translate_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.translate_frame, text='Translate')
        self.notebook.add(self.settings_frame, text='Settings')

        # Adjust grid weights
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.translate_frame.columnconfigure(1, weight=1)

        # Translation Tab UI
        self._create_translation_tab()

        # Settings Tab UI
        self._create_settings_tab()

        # Status Label
        self.status_label = ttk.Label(master, text="Ready")
        self.status_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    def _create_translation_tab(self):
        # Source Language
        self.src_lang_label = ttk.Label(self.translate_frame, text="Source Language:")
        self.src_lang_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.src_lang = tk.StringVar(value='en')
        self.src_lang_menu = ttk.Combobox(
            self.translate_frame, textvariable=self.src_lang, values=['en', 'es'], state='readonly'
        )
        self.src_lang_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Target Language
        self.tgt_lang_label = ttk.Label(self.translate_frame, text="Target Language:")
        self.tgt_lang_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.tgt_lang = tk.StringVar(value='es')
        self.tgt_lang_menu = ttk.Combobox(
            self.translate_frame, textvariable=self.tgt_lang, values=['en', 'es'], state='readonly'
        )
        self.tgt_lang_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Start and Stop Buttons
        self.start_button = ttk.Button(
            self.translate_frame, text="Start Recording", command=self.start_translation
        )
        self.start_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.stop_button = ttk.Button(
            self.translate_frame, text="Stop Recording", command=self.stop_translation, state='disabled'
        )
        self.stop_button.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Output Text
        self.output_text = tk.Text(self.translate_frame, height=10, width=50)
        self.output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def _create_settings_tab(self):
        # Input Device Selection
        self.input_device_label = ttk.Label(self.settings_frame, text="Input Device:")
        self.input_device_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.input_devices = self._get_input_devices()
        self.input_device_var = tk.StringVar()

        # Get default input device
        default_input_index = sd.default.device[0]
        default_input_device = sd.query_devices(default_input_index)['name']

        self.input_device_menu = ttk.Combobox(
            self.settings_frame, textvariable=self.input_device_var,
            values=[device['name'] for device in self.input_devices], state='readonly'
        )
        self.input_device_menu.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Select the default input device
        if default_input_device in [device['name'] for device in self.input_devices]:
            self.input_device_menu.set(default_input_device)
        else:
            self.input_device_menu.current(0)

        # Output Device Selection
        self.output_device_label = ttk.Label(self.settings_frame, text="Output Device:")
        self.output_device_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.output_devices = self._get_output_devices()
        self.output_device_var = tk.StringVar()

        # Get default output device
        default_output_index = sd.default.device[1]
        default_output_device = sd.query_devices(default_output_index)['name']

        self.output_device_menu = ttk.Combobox(
            self.settings_frame, textvariable=self.output_device_var,
            values=[device['name'] for device in self.output_devices], state='readonly'
        )
        self.output_device_menu.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Select the default output device
        if default_output_device in [device['name'] for device in self.output_devices]:
            self.output_device_menu.set(default_output_device)
        else:
            self.output_device_menu.current(0)

        # TTS Speed Adjustment
        self.tts_speed_label = ttk.Label(self.settings_frame, text="TTS Speed:")
        self.tts_speed_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.tts_speed_var = tk.DoubleVar(value=1.0)  # Default speed is 1.0 (normal speed)
        self.tts_speed_scale = ttk.Scale(
            self.settings_frame, variable=self.tts_speed_var, from_=0.5, to=2.0, orient='horizontal', length=200
        )
        self.tts_speed_scale.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        self.tts_speed_value_label = ttk.Label(self.settings_frame, textvariable=self.tts_speed_var)
        self.tts_speed_value_label.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        # Apply Button
        self.apply_button = ttk.Button(
            self.settings_frame, text="Apply", command=self.apply_settings
        )
        self.apply_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def _get_input_devices(self):
        devices = sd.query_devices()
        input_devices = [device for device in devices if device['max_input_channels'] > 0]
        return input_devices

    def _get_output_devices(self):
        devices = sd.query_devices()
        output_devices = [device for device in devices if device['max_output_channels'] > 0]
        return output_devices

    def apply_settings(self):
        # In main.py, we will handle updating settings when this method is called
        pass

    def start_translation(self):
        pass  # To be implemented in main.py

    def stop_translation(self):
        pass  # To be implemented in main.py
