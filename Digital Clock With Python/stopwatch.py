import tkinter as tk
import time


class StopwatchView:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#734141")

        self.running = False
        self.elapsed = 0.0       
        self.start_time = None   

        self.time_label = tk.Label(
            self.frame, text="00:00:00.0", font=("Helvetica", 40), bg="white", fg="black")
        self.time_label.pack(expand=True)

        btn_frame = tk.Frame(self.frame, bg="white")
        btn_frame.pack(pady=20)

        self.start_pause_btn = tk.Button(
            btn_frame, text="Start", width=10, font=("Helvetica", 11),
            cursor="hand2", command=self.toggle
        )
        self.start_pause_btn.grid(row=0, column=0, padx=8)

        reset_btn = tk.Button(
            btn_frame, text="Reset", width=10, font=("Helvetica", 11),
            cursor="hand2", command=self.reset
        )
        reset_btn.grid(row=0, column=1, padx=8)

        self.start()

    def toggle(self):
        if self.running:
            self.elapsed += time.time() - self.start_time
            self.running = False
            self.start_pause_btn.config(text="Start")
        else:
            self.start_time = time.time()
            self.running = True
            self.start_pause_btn.config(text="Pause")

    def reset(self):
        self.running = False
        self.elapsed = 0.0
        self.start_time = None
        self.start_pause_btn.config(text="Start")
        self.time_label.config(text="00:00:00.0")

    def start(self):
        
        self._tick()

    def stop(self):
        
        if self._after_id is not None:
            self.frame.after_cancel(self._after_id)
            self._after_id = None

    def _tick(self):
        current = self.elapsed
        if self.running:
            current += time.time() - self.start_time

        hours, rem = divmod(current, 3600)
        minutes, sec_full = divmod(rem, 60)
        seconds = int(sec_full)
        tenths = int((sec_full - seconds) * 10)

        self.time_label.config(
            text=f"{int(hours):02}:{int(minutes):02}:{seconds:02}.{tenths}"
        )
        self._after_id = self.frame.after(100, self._tick)
