# tkinter-clock-app-python

A multi-feature desktop clock application built with **Python** and **Tkinter**. Everything lives in a single window — a sidebar lets you switch instantly between a Digital Clock, Stopwatch, Alarm, Timer, and a searchable World Clock, with no pop-up windows for individual features.

## Features

### 🕐 Digital Clock
Live 12-hour clock with AM/PM, updating every 200ms.

### ⏱️ Stopwatch
- Start / Pause / Reset controls
- Time is calculated from real timestamps rather than an incrementing counter, so there's no drift
- Keeps counting accurately even while you're viewing a different tab, and picks up exactly where it should when you switch back

### ⏰ Alarm
- Set a target time via Hour / Minute / Second / AM-PM pickers
- Checks the clock every second in the background — independent of whichever tab is currently open, so it can go off no matter what you're looking at
- Plays a chime and shows a popup when the target time is reached

### ⏳ Timer
- Set a countdown duration (Hours / Minutes / Seconds)
- Same timestamp-based accuracy as the Stopwatch
- Runs continuously in the background so it can finish and alert you regardless of which view is open
- Plays a chime and shows a popup when it reaches zero

### 🌍 World Clock
- Search and add a live clock for **any** city, region, or country
- Powered by the IANA timezone database (`zoneinfo` / `tzdata`) for accurate, DST-aware local times
- Search matches both the underlying timezone (e.g. "New York") and common country names (e.g. "Bangladesh" → Asia/Dhaka)
- Add or remove as many locations as you like

## Interface

- A sidebar on the left lists all features; clicking one swaps the content area in place — no separate windows pop up
- The active feature stays highlighted in the sidebar, with hover and click feedback on every button, so it's always clear what you're looking at and what you just pressed

## Project Structure

```
tkinter-clock-app-python/
├── main.py            # Entry point — builds the sidebar and wires up all views
├── digital_clock.py   # Digital Clock view
├── stopwatch.py        # Stopwatch view
├── alarm.py            # Alarm view
├── timer.py             # Timer view
├── worldclock.py       # World Clock view (search + add/remove locations)
└── sound.py             # Shared alert-chime helper used by Alarm and Timer
```

## Requirements

- Python 3.9 or later (for the built-in `zoneinfo` module)
- **Windows users:** the `tzdata` package must be installed separately, since Windows doesn't ship the IANA timezone database:
  ```bash
  pip install tzdata
  ```
- No other third-party dependencies — everything else uses Python's standard library (`tkinter`, `datetime`, `time`, `winsound`).

## Running the App

Clone the repository, make sure all files are in the same folder, then run:

```bash
python main.py
```

## How It Works (Technical Notes)

- **Single-window navigation:** every view is a small class that builds a `Frame`; `main.py` keeps all views alive from startup and shows/hides them with `pack()` / `pack_forget()` instead of destroying and recreating them, so state (like a running Stopwatch) isn't lost when you switch tabs.
- **Drift-free timing:** the Stopwatch and Timer compute elapsed/remaining time from `time.time()` differences rather than accumulating per-tick, so their displayed time stays accurate regardless of how the OS schedules UI updates.
- **Background-safe alerts:** the Alarm and Timer's checking loops are deliberately *not* tied to view visibility — they run for the entire lifetime of the app so they can fire while you're on a different tab.
- **Alert sound:** a short three-note ascending chime (via `winsound.Beep` on Windows) plays when an Alarm or Timer completes, instead of a single flat system beep.

## Possible Future Improvements

- Multiple simultaneous alarms
- Repeating alarms and snooze support
- Custom notification sounds
- Light/dark theme toggle
- Persisting World Clock selections between sessions

## Author

**Tahlil Al Raiyan**
GitHub: [@TahlilAlRaiyan](https://github.com/TahlilAlRaiyan)

## License

This project is available under the MIT License — add a `LICENSE` file to the repository if you'd like to formally apply it.
