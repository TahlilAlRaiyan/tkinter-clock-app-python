_CHIME_NOTES = [523, 659, 784]   
_NOTE_DURATION_MS = 150


def play_alert_sound(widget=None):
    
    try:
        import winsound
        for freq in _CHIME_NOTES:
            winsound.Beep(freq, _NOTE_DURATION_MS)
    except ImportError:
        if widget is not None:
            for _ in range(3):
                widget.bell()
