import tkinter as tk
import time


class DigitalClockView:
    

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="skyblue")

        self.clock_label = tk.Label(
            self.frame, font=("Helvetica", 40), bg="skyblue", fg="black"
        )
        self.clock_label.pack(expand=True, fill="both")

        self._after_id = None
        self.start()

    def start(self):
        
        self._tick()

    def stop(self):
        
        if self._after_id is not None:
            self.frame.after_cancel(self._after_id)
            self._after_id = None

    def _tick(self):
        self.clock_label.config(text=time.strftime("%I:%M:%S %p"))
        self._after_id = self.frame.after(200, self._tick)
