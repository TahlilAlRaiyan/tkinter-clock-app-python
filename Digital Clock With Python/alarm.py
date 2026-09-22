import tkinter as tk
from tkinter import messagebox
import time

from sound import play_alert_sound


class AlarmView:
    
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#E8BCBC")

        self.alarm_time = None   
        self.triggered = False   
        self._checker_id = None

        tk.Label(
            self.frame, text="Set Alarm", font=("Helvetica", 20),
            bg="white", fg="black"
        ).pack(pady=(30, 10))

        
        picker_frame = tk.Frame(self.frame, bg="white")
        picker_frame.pack(pady=10)

        self.hour_var = tk.StringVar(value="07")
        self.minute_var = tk.StringVar(value="00")
        self.second_var = tk.StringVar(value="00")
        self.period_var = tk.StringVar(value="AM")

        hours = [f"{h:02}" for h in range(1, 13)]
        minutes_and_seconds = [f"{n:02}" for n in range(60)]

        tk.OptionMenu(picker_frame, self.hour_var, *hours).grid(row=0, column=0, padx=3)
        tk.Label(picker_frame, text=":", bg="white", font=("Helvetica", 14)).grid(row=0, column=1)
        tk.OptionMenu(picker_frame, self.minute_var, *minutes_and_seconds).grid(row=0, column=2, padx=3)
        tk.Label(picker_frame, text=":", bg="white", font=("Helvetica", 14)).grid(row=0, column=3)
        tk.OptionMenu(picker_frame, self.second_var, *minutes_and_seconds).grid(row=0, column=4, padx=3)
        tk.OptionMenu(picker_frame, self.period_var, "AM", "PM").grid(row=0, column=5, padx=(10, 0))

        
        btn_frame = tk.Frame(self.frame, bg="white")
        btn_frame.pack(pady=15)

        self.set_btn = tk.Button(
            btn_frame, text="Set Alarm", width=10, font=("Helvetica", 11),
            cursor="hand2", command=self.set_alarm
        )
        self.set_btn.grid(row=0, column=0, padx=8)

        self.cancel_btn = tk.Button(
            btn_frame, text="Cancel", width=10, font=("Helvetica", 11),
            cursor="hand2", command=self.cancel_alarm, state="disabled"
        )
        self.cancel_btn.grid(row=0, column=1, padx=8)

        
        self.status_label = tk.Label(
            self.frame, text="No alarm set", font=("Helvetica", 12),
            bg="white", fg="#555555"
        )
        self.status_label.pack(pady=(10, 0))

        
        self._check_alarm()

    def set_alarm(self):
        hour_12 = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        second = int(self.second_var.get())
        period = self.period_var.get()

        
        hour_24 = hour_12 % 12
        if period == "PM":
            hour_24 += 12

        self.alarm_time = f"{hour_24:02}:{minute:02}:{second:02}"
        self.triggered = False

        self.status_label.config(
            text=f"Alarm set for {self.hour_var.get()}:{self.minute_var.get()}:"
                 f"{self.second_var.get()} {period}",
            fg="#1abc9c",
        )
        self.set_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")

    def cancel_alarm(self):
        self.alarm_time = None
        self.triggered = False
        self.status_label.config(text="No alarm set", fg="#555555")
        self.set_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def _check_alarm(self):
        if self.alarm_time is not None and not self.triggered:
            if time.strftime("%H:%M:%S") == self.alarm_time:
                self.triggered = True
                self._ring()

        self._checker_id = self.frame.after(1000, self._check_alarm)

    def _ring(self):
        play_alert_sound(self.frame)
        messagebox.showinfo("Alarm", "\u23f0 Time's up!")
        self.cancel_alarm()  

    
    def start(self):
        pass

    def stop(self):
        pass
