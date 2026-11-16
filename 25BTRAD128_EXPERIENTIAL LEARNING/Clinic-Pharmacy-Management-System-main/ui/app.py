import tkinter as tk
from tkinter import ttk

from ui import theme
from config import APP_NAME

from ui.pages.dashboard import DashboardPage
from ui.pages.patients import PatientsPage
from ui.pages.doctors import DoctorsPage
from ui.pages.medicines import MedicinesPage
from ui.pages.medical_history import MedicalHistoryPage


NAV_ITEMS = [
    ("dashboard", "🏠  Dashboard", DashboardPage),
    ("patients", "🧑‍🤝‍🧑  Patients", PatientsPage),
    ("doctors", "🩺  Doctors", DoctorsPage),
    ("medicines", "💊  Medicines", MedicinesPage),
    ("history", "📋  Medical Records", MedicalHistoryPage),
]


class ClinicPharmacyApp(tk.Tk):
    """Root window: dark sidebar for navigation + a swappable content area."""

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1180x720")
        self.minsize(1000, 640)

        theme.setup_style(self)

        self.pages = {}
        self.nav_buttons = {}
        self.active_key = None

        self._build_layout()
        self.show_page("dashboard")

    def _build_layout(self):
        root = ttk.Frame(self, style="TFrame")
        root.pack(fill="both", expand=True)

        # --- Sidebar ---
        sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=theme.BG_DARK)
        brand.pack(fill="x", pady=(24, 16), padx=16)
        tk.Label(brand, text="🏥", bg=theme.BG_DARK, fg="white",
                 font=(theme.FONT_FAMILY, 26)).pack(anchor="w")
        tk.Label(brand, text="Clinic & Pharmacy", bg=theme.BG_DARK, fg="white",
                 font=(theme.FONT_FAMILY, 13, "bold")).pack(anchor="w", pady=(6, 0))
        tk.Label(brand, text="Clinic & Pharmacy System", bg=theme.BG_DARK, fg="#8DA3BD",
                 font=(theme.FONT_FAMILY, 9)).pack(anchor="w")

        ttk.Separator(sidebar).pack(fill="x", padx=16, pady=(0, 8))

        for key, label, _ in NAV_ITEMS:
            btn = ttk.Button(sidebar, text=label, style="Nav.TButton",
                              command=lambda k=key: self.show_page(k))
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[key] = btn

        # --- Content area ---
        content_outer = ttk.Frame(root, style="TFrame")
        content_outer.pack(side="left", fill="both", expand=True)

        self.content = ttk.Frame(content_outer, style="TFrame", padding=28)
        self.content.pack(fill="both", expand=True)

        for key, _, page_cls in NAV_ITEMS:
            page = page_cls(self.content, self)
            page.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.pages[key] = page

    def show_page(self, key):
        if self.active_key == key:
            self.pages[key].on_show()
            return

        if self.active_key:
            self.nav_buttons[self.active_key].configure(style="Nav.TButton")

        self.nav_buttons[key].configure(style="NavActive.TButton")
        self.pages[key].tkraise()
        self.pages[key].on_show()
        self.active_key = key

    def refresh_all(self):
        """Called after any data change so every page reflects the latest state."""
        for page in self.pages.values():
            if hasattr(page, "refresh"):
                page.refresh()


if __name__ == "__main__":
    # Allows running the UI directly for quick manual testing without main.py
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from persistence.database import create_data_tables, get_patients, get_doctors, get_solid_medicines, get_liquid_medicines, link_medical_histories
    from core.session import Session

    create_data_tables()
    Session.patients = get_patients()
    Session.doctors = get_doctors()
    Session.solid_medicines = get_solid_medicines()
    Session.liquid_medicines = get_liquid_medicines()
    link_medical_histories()

    ClinicPharmacyApp().mainloop()
