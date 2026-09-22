import tkinter as tk

from digital_clock import DigitalClockView
from stopwatch import StopwatchView
from alarm import AlarmView
from timer import TimerView
from worldclock import WorldClockView


class MainApp:
    COLOR_DEFAULT = "#34495e"   
    COLOR_HOVER = "#3d5a75"     
    COLOR_SELECTED = "#1abc9c"  
    def __init__(self, root):
        self.root = root
        self.root.title("Clock App")
        self.root.geometry("500x300")

        
        sidebar = tk.Frame(root, bg=self.COLOR_DEFAULT, width=150)
        sidebar.pack(side="left", fill="y")

        self.nav_buttons = {}
        self.selected_name = None

        options = [
            ("Digital Clock", "digital_clock"),
            ("Stopwatch", "stopwatch"),
            ("Alarm", "alarm"),
            ("Timer", "timer"),
            ("World Clock", "world_clock"),
        ]

        for label, key in options:
            btn = tk.Button(
                sidebar, text=label, bg=self.COLOR_DEFAULT, fg="white",
                relief="flat", bd=0, font=("Helvetica", 12), anchor="w",
                padx=15, pady=10, cursor="hand2",
                activebackground=self.COLOR_SELECTED, activeforeground="white",
                command=lambda k=key: self.switch_view(k),
            )
            btn.pack(fill="x")
            
            btn.bind("<Enter>", lambda event, k=key: self._on_hover(k, True))
            btn.bind("<Leave>", lambda event, k=key: self._on_hover(k, False))
            self.nav_buttons[key] = btn

        
        self.content = tk.Frame(root, bg="white")
        self.content.pack(side="right", fill="both", expand=True)

        
        self.views = {
            "digital_clock": DigitalClockView(self.content),
            "stopwatch": StopwatchView(self.content),
            "alarm": AlarmView(self.content),
            "timer": TimerView(self.content),
            "world_clock": WorldClockView(self.content),
        }
        for view in self.views.values():
            view.frame.pack_forget()
            view.stop()

        self.switch_view("digital_clock")

    def _on_hover(self, key, entering):
        if key == self.selected_name:
            return  
        btn = self.nav_buttons[key]
        btn.config(bg=self.COLOR_HOVER if entering else self.COLOR_DEFAULT)

    def switch_view(self, key):
        if key == self.selected_name:
            return  

        if self.selected_name is not None:
            self.nav_buttons[self.selected_name].config(bg=self.COLOR_DEFAULT)
            self.views[self.selected_name].stop()
            self.views[self.selected_name].frame.pack_forget()

        self.selected_name = key
        self.nav_buttons[key].config(bg=self.COLOR_SELECTED)

        view = self.views[key]
        view.frame.pack(fill="both", expand=True)
        view.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

