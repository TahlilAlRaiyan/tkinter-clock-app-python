import tkinter as tk
from tkinter import messagebox
import time

from sound import play_alert_sound


class TimerView:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#6541D1")

        self.running = False
        self.remaining = 0.0     
        self.end_time = None     

        tk.Label(
            self.frame, text="Timer", font=("Helvetica", 20),
            bg="white", fg="black"
        ).pack(pady=(20, 5))

        
        self.time_label = tk.Label(
            self.frame, text="00:00:00", font=("Helvetica", 36),
            bg="white", fg="black"
        )
        self.time_label.pack(pady=(0, 15))

        
        picker_frame = tk.Frame(self.frame, bg="white")
        picker_frame.pack()

        spin_opts = dict(width=3, font=("Helvetica", 14), justify="center", format="%02.0f")

        self.hour_spin = tk.Spinbox(picker_frame, from_=0, to=23, **spin_opts)
        self.hour_spin.grid(row=0, column=0, padx=3)
        tk.Label(picker_frame, text=":", bg="white", font=("Helvetica", 14)).grid(row=0, column=1)
        self.minute_spin = tk.Spinbox(picker_frame, from_=0, to=59, **spin_opts)
        self.minute_spin.grid(row=0, column=2, padx=3)
        tk.Label(picker_frame, text=":", bg="white", font=("Helvetica", 14)).grid(row=0, column=3)
        self.second_spin = tk.Spinbox(picker_frame, from_=0, to=59, **spin_opts)
        self.second_spin.grid(row=0, column=4, padx=3)

        self._spinboxes = (self.hour_spin, self.minute_spin, self.second_spin)

        
        btn_frame = tk.Frame(self.frame, bg="white")
        btn_frame.pack(pady=15)

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

        
        self._tick()

    def toggle(self):
        if self.running:
            
            self.remaining = max(0.0, self.end_time - time.time())
            self.running = False
            self.start_pause_btn.config(text="Start")
        else:
            if self.remaining <= 0:
                
                total = self._read_duration()
                if total <= 0:
                    return  
                self.remaining = total
                self._set_spinboxes_state("disabled")

            self.end_time = time.time() + self.remaining
            self.running = True
            self.start_pause_btn.config(text="Pause")

    def reset(self):
        self.running = False
        self.remaining = 0.0
        self.end_time = None
        self.start_pause_btn.config(text="Start")
        self._set_spinboxes_state("normal")
        self._update_label(0)

    def _read_duration(self):
        try:
            h = int(self.hour_spin.get())
            m = int(self.minute_spin.get())
            s = int(self.second_spin.get())
        except ValueError:
            return 0
        return h * 3600 + m * 60 + s

    def _set_spinboxes_state(self, state):
        for spin in self._spinboxes:
            spin.config(state=state)

    def _tick(self):
        if self.running:
            remaining_now = self.end_time - time.time()
            if remaining_now <= 0:
                self.running = False
                self.remaining = 0.0
                self._update_label(0)
                self._on_complete()
            else:
                self._update_label(remaining_now)
        else:
            self._update_label(self.remaining)

        self.frame.after(200, self._tick)

    def _update_label(self, seconds_left):
        total_seconds = max(0, int(seconds_left + 0.5))  
        hours, rem = divmod(total_seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def _on_complete(self):
        self.start_pause_btn.config(text="Start")
        self._set_spinboxes_state("normal")
        play_alert_sound(self.frame)
        messagebox.showinfo("Timer", "\u23f0 Time's up!")

    
    def start(self):
        pass

    def stop(self):
        pass
