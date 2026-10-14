import time
from pathlib import Path
from tkinter import messagebox
from playsound3 import PlaysoundException, playsound
from UI.ResourcePath import resource_path
from UI.ShowHelp import show_help

help_click_times = []

def handle_help_click(root):
    global help_click_times

    current_time = time.monotonic()

    help_click_times = [
        click_time for click_time in help_click_times
        if current_time - click_time <= 1.0
    ]

    help_click_times.append(current_time)

    if len(help_click_times) >= 3:
        sound_path = Path(resource_path("Seal_noises_fixed.wav"))

        try:
            playsound(str(sound_path), block=False)
        except PlaysoundException as error:
            messagebox.showerror(
                "Sound Error",
                f"Could not play the custom WAV:\n\n{error}",
                parent=root
            )
        help_click_times = []
    show_help(root)