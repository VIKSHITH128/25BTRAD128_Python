import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.widgets import Card, KPI
from ui.helpers import expiry_status
from core.session import Session


class DashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller

        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", pady=(0, 20))
        ttk.Label(header, text="Overview", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Quick summary of clinic & pharmacy status",
                  style="Subtitle.TLabel").pack(anchor="w")

        kpi_row = ttk.Frame(self, style="TFrame")
        kpi_row.pack(fill="x")
        for i in range(4):
            kpi_row.columnconfigure(i, weight=1)

        self.kpi_patients = KPI(kpi_row, "Total Patients", 0, theme.PRIMARY)
        self.kpi_doctors = KPI(kpi_row, "Total Doctors", 0, theme.ACCENT_TEAL)
        self.kpi_medicines = KPI(kpi_row, "Medicine Types", 0, theme.SUCCESS)
        self.kpi_alerts = KPI(kpi_row, "Stock Alerts", 0, theme.WARNING)

        self.kpi_patients.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.kpi_doctors.grid(row=0, column=1, sticky="ew", padx=6)
        self.kpi_medicines.grid(row=0, column=2, sticky="ew", padx=6)
        self.kpi_alerts.grid(row=0, column=3, sticky="ew", padx=(12, 0))

        body = ttk.Frame(self, style="TFrame")
        body.pack(fill="both", expand=True, pady=(20, 0))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # Expiring / expired medicines
        expiry_card = Card(body)
        expiry_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ttk.Label(expiry_card, text="⚠️ Expiring or Expired Medicines",
                  style="H2.TLabel").pack(anchor="w", pady=(0, 10))
        self.expiry_list = tk.Listbox(expiry_card, height=10, borderwidth=0,
                                       highlightthickness=0, font=theme.FONT_BODY,
                                       activestyle="none")
        self.expiry_list.pack(fill="both", expand=True)

        # Low stock
        stock_card = Card(body)
        stock_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ttk.Label(stock_card, text="📦 Low Stock (less than 10)",
                  style="H2.TLabel").pack(anchor="w", pady=(0, 10))
        self.stock_list = tk.Listbox(stock_card, height=10, borderwidth=0,
                                      highlightthickness=0, font=theme.FONT_BODY,
                                      activestyle="none")
        self.stock_list.pack(fill="both", expand=True)

    def on_show(self):
        self.refresh()

    def refresh(self):
        self.kpi_patients.set_value(len(Session.patients))
        self.kpi_doctors.set_value(len(Session.doctors))
        self.kpi_medicines.set_value(len(Session.solid_medicines) + len(Session.liquid_medicines))

        all_meds = list(Session.solid_medicines) + list(Session.liquid_medicines)

        self.expiry_list.delete(0, tk.END)
        expiring = 0
        for med in all_meds:
            status = expiry_status(med.expiry_date)
            if status == "expired":
                self.expiry_list.insert(tk.END, f"  ⛔ {med.name} - Expired ({med.expiry_date})")
                self.expiry_list.itemconfig(tk.END, fg=theme.DANGER)
                expiring += 1
            elif status == "soon":
                self.expiry_list.insert(tk.END, f"  ⏳ {med.name} - Expires on {med.expiry_date}")
                self.expiry_list.itemconfig(tk.END, fg=theme.WARNING)
                expiring += 1
        if self.expiry_list.size() == 0:
            self.expiry_list.insert(tk.END, "  No alerts at the moment ✅")

        self.stock_list.delete(0, tk.END)
        low_stock = 0
        for med in all_meds:
            if med.quantity < 10:
                self.stock_list.insert(tk.END, f"  {med.name}: {med.quantity} units remaining")
                self.stock_list.itemconfig(tk.END, fg=theme.DANGER)
                low_stock += 1
        if self.stock_list.size() == 0:
            self.stock_list.insert(tk.END, "  Stock levels are good ✅")

        self.kpi_alerts.set_value(expiring + low_stock)
