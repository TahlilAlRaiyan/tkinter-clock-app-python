import tkinter as tk
from datetime import datetime

try:
    from zoneinfo import ZoneInfo, available_timezones
    ZoneInfo("UTC")
    ALL_ZONES = sorted(available_timezones())
except Exception:
    ZoneInfo = None
    ALL_ZONES = []

COUNTRY_ALIASES = {
    "bangladesh": "Asia/Dhaka", "india": "Asia/Kolkata", "pakistan": "Asia/Karachi",
    "nepal": "Asia/Kathmandu", "sri lanka": "Asia/Colombo", "myanmar": "Asia/Yangon",
    "thailand": "Asia/Bangkok", "vietnam": "Asia/Ho_Chi_Minh", "cambodia": "Asia/Phnom_Penh",
    "laos": "Asia/Vientiane", "malaysia": "Asia/Kuala_Lumpur", "singapore": "Asia/Singapore",
    "indonesia": "Asia/Jakarta", "philippines": "Asia/Manila", "china": "Asia/Shanghai",
    "japan": "Asia/Tokyo", "south korea": "Asia/Seoul", "north korea": "Asia/Pyongyang",
    "taiwan": "Asia/Taipei", "hong kong": "Asia/Hong_Kong", "mongolia": "Asia/Ulaanbaatar",
    "kazakhstan": "Asia/Almaty", "uzbekistan": "Asia/Tashkent", "afghanistan": "Asia/Kabul",
    "iran": "Asia/Tehran", "iraq": "Asia/Baghdad", "saudi arabia": "Asia/Riyadh",
    "uae": "Asia/Dubai", "united arab emirates": "Asia/Dubai", "qatar": "Asia/Qatar",
    "kuwait": "Asia/Kuwait", "bahrain": "Asia/Bahrain", "oman": "Asia/Muscat",
    "israel": "Asia/Jerusalem", "jordan": "Asia/Amman", "lebanon": "Asia/Beirut",
    "syria": "Asia/Damascus", "armenia": "Asia/Yerevan", "azerbaijan": "Asia/Baku",
    "georgia": "Asia/Tbilisi", "russia": "Europe/Moscow", "ukraine": "Europe/Kyiv",
    "poland": "Europe/Warsaw", "germany": "Europe/Berlin", "france": "Europe/Paris",
    "spain": "Europe/Madrid", "portugal": "Europe/Lisbon", "italy": "Europe/Rome",
    "greece": "Europe/Athens", "united kingdom": "Europe/London", "uk": "Europe/London",
    "england": "Europe/London", "ireland": "Europe/Dublin", "netherlands": "Europe/Amsterdam",
    "belgium": "Europe/Brussels", "switzerland": "Europe/Zurich", "austria": "Europe/Vienna",
    "sweden": "Europe/Stockholm", "norway": "Europe/Oslo", "denmark": "Europe/Copenhagen",
    "finland": "Europe/Helsinki", "iceland": "Atlantic/Reykjavik", "romania": "Europe/Bucharest",
    "hungary": "Europe/Budapest", "czech republic": "Europe/Prague", "czechia": "Europe/Prague",
    "slovakia": "Europe/Bratislava", "bulgaria": "Europe/Sofia", "serbia": "Europe/Belgrade",
    "croatia": "Europe/Zagreb", "slovenia": "Europe/Ljubljana", "lithuania": "Europe/Vilnius",
    "latvia": "Europe/Riga", "estonia": "Europe/Tallinn", "usa": "America/New_York",
    "united states": "America/New_York", "canada": "America/Toronto",
    "mexico": "America/Mexico_City", "brazil": "America/Sao_Paulo",
    "argentina": "America/Argentina/Buenos_Aires", "chile": "America/Santiago",
    "colombia": "America/Bogota", "peru": "America/Lima", "venezuela": "America/Caracas",
    "cuba": "America/Havana", "jamaica": "America/Jamaica", "panama": "America/Panama",
    "guatemala": "America/Guatemala", "egypt": "Africa/Cairo", "nigeria": "Africa/Lagos",
    "kenya": "Africa/Nairobi", "south africa": "Africa/Johannesburg",
    "ethiopia": "Africa/Addis_Ababa", "ghana": "Africa/Accra", "morocco": "Africa/Casablanca",
    "algeria": "Africa/Algiers", "tunisia": "Africa/Tunis", "sudan": "Africa/Khartoum",
    "uganda": "Africa/Kampala", "tanzania": "Africa/Dar_es_Salaam",
    "australia": "Australia/Sydney", "new zealand": "Pacific/Auckland",
    "fiji": "Pacific/Fiji", "hawaii": "Pacific/Honolulu",
}

ZONE_TO_COUNTRY = {}
for _name, _zone in COUNTRY_ALIASES.items():
    ZONE_TO_COUNTRY.setdefault(_zone, _name.title())


def _build_search_index():
    index = []
    for zone in ALL_ZONES:
        clean = zone.replace("_", " ").replace("/", " - ")
        country = ZONE_TO_COUNTRY.get(zone)
        display = f"{country} ({clean})" if country else clean
        searchable = display.lower()
        index.append((display, zone, searchable))
    return index


SEARCH_INDEX = _build_search_index()


class WorldClockView:
    DEFAULT_ZONES = ["Asia/Dhaka", "Europe/London", "America/New_York"]

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#6D6191")

        tk.Label(
            self.frame, text="World Clock", font=("Helvetica", 18),
            bg="white", fg="black"
        ).pack(pady=(15, 5))

        search_frame = tk.Frame(self.frame, bg="white")
        search_frame.pack(fill="x", padx=15)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, font=("Helvetica", 11)
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        self.search_entry.bind("<Return>", self._on_enter)

        add_btn = tk.Button(
            search_frame, text="Add", cursor="hand2", command=self._add_selected
        )
        add_btn.pack(side="left", padx=(6, 0))

        self.suggestions = tk.Listbox(self.frame, height=4, font=("Helvetica", 10))
        self.suggestions.pack(fill="x", padx=15, pady=(4, 8))
        self.suggestions.bind("<Double-Button-1>", lambda e: self._add_selected())

        self.current_matches = []

        list_container = tk.Frame(self.frame, bg="white")
        list_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        canvas = tk.Canvas(list_container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas, bg="white")

        self.rows_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tracked = {}

        if ZoneInfo is not None:
            for zone in self.DEFAULT_ZONES:
                self._add_zone(zone)
        else:
            tk.Label(
                self.rows_frame, text="Run: pip install tzdata",
                font=("Helvetica", 12), bg="white", fg="red"
            ).pack(pady=10)

        self._after_id = None
        self.start()

    def _on_search(self, event):
        query = self.search_var.get().strip().lower()
        self.suggestions.delete(0, tk.END)
        self.current_matches = []
        if not query:
            return
        matches = [
            (display, zone) for display, zone, searchable in SEARCH_INDEX
            if query in searchable
        ][:20]
        self.current_matches = matches
        for display, _ in matches:
            self.suggestions.insert(tk.END, display)

    def _on_enter(self, event):
        if self.suggestions.size() > 0:
            self.suggestions.selection_clear(0, tk.END)
            self.suggestions.selection_set(0)
            self._add_selected()

    def _add_selected(self):
        selection = self.suggestions.curselection()
        if not selection or not self.current_matches:
            return
        _, zone = self.current_matches[selection[0]]
        self._add_zone(zone)
        self.search_var.set("")
        self.suggestions.delete(0, tk.END)
        self.current_matches = []

    def _add_zone(self, zone_name):
        if zone_name in self.tracked or ZoneInfo is None:
            return

        row = tk.Frame(self.rows_frame, bg="white")
        row.pack(fill="x", pady=3)

        country = ZONE_TO_COUNTRY.get(zone_name)
        label_text = f"{country} ({zone_name.replace('_', ' ')})" if country else zone_name.replace("_", " ")

        tk.Label(
            row, text=label_text, font=("Helvetica", 12),
            bg="white", fg="black", anchor="w"
        ).pack(side="left", fill="x", expand=True)

        time_label = tk.Label(
            row, text="--:--:-- --", font=("Helvetica", 12, "bold"),
            bg="white", fg="#CF7713"
        )
        time_label.pack(side="left", padx=(0, 8))

        remove_btn = tk.Button(
            row, text="\u2715", fg="red", bd=0, bg="white", cursor="hand2",
            command=lambda z=zone_name: self._remove_zone(z)
        )
        remove_btn.pack(side="right")

        self.tracked[zone_name] = (row, time_label, ZoneInfo(zone_name))

    def _remove_zone(self, zone_name):
        entry = self.tracked.pop(zone_name, None)
        if entry is not None:
            entry[0].destroy()

    def start(self):
        self._tick()

    def stop(self):
        if self._after_id is not None:
            self.frame.after_cancel(self._after_id)
            self._after_id = None

    def _tick(self):
        for zone_name, (_, label, tzinfo) in self.tracked.items():
            now = datetime.now(tzinfo)
            label.config(text=now.strftime("%I:%M:%S %p"))

        self._after_id = self.frame.after(1000, self._tick)

