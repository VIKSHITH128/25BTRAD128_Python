import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.widgets import Card, FormDialog, ConfirmDialog, Toast
from ui.helpers import next_id, expiry_status, validate_date_field
from core.session import Session
from persistence.database import (
    add_solid_medicine, update_solid_medicine, remove_solid_medicine_by_id,
    add_liquid_medicine, update_liquid_medicine, remove_liquid_medicine_by_id,
)

UNITS = ["ml", "L"]

SOLID_COLUMNS = ("id", "name", "purpose", "price", "quantity", "strips", "pills_per_strip", "expiry_date")
SOLID_HEADERS = {
    "id": "Code", "name": "Name", "purpose": "Purpose", "price": "Price",
    "quantity": "Quantity", "strips": "Strips", "pills_per_strip": "Pills/Strip",
    "expiry_date": "Expiry Date",
}

LIQUID_COLUMNS = ("id", "name", "purpose", "price", "quantity", "volume", "unit", "expiry_date")
LIQUID_HEADERS = {
    "id": "Code", "name": "Name", "purpose": "Purpose", "price": "Price",
    "quantity": "Quantity", "volume": "Volume", "unit": "Unit", "expiry_date": "Expiry Date",
}


class MedicinesPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller

        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Medicines", style="Title.TLabel").pack(side="left")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.solid_tab = MedicineSubPage(
            notebook, controller, kind="solid",
            columns=SOLID_COLUMNS, headers=SOLID_HEADERS,
            get_items=lambda: Session.solid_medicines,
            add_fn=add_solid_medicine, update_fn=update_solid_medicine,
            remove_fn=remove_solid_medicine_by_id,
        )
        self.liquid_tab = MedicineSubPage(
            notebook, controller, kind="liquid",
            columns=LIQUID_COLUMNS, headers=LIQUID_HEADERS,
            get_items=lambda: Session.liquid_medicines,
            add_fn=add_liquid_medicine, update_fn=update_liquid_medicine,
            remove_fn=remove_liquid_medicine_by_id,
        )

        notebook.add(self.solid_tab, text="Solid Medicines (Tablets)")
        notebook.add(self.liquid_tab, text="Liquid Medicines (Syrup/Solution)")

    def on_show(self):
        self.refresh()

    def refresh(self):
        self.solid_tab.refresh()
        self.liquid_tab.refresh()


class MedicineSubPage(ttk.Frame):
    """Shared implementation for both the solid and liquid medicine tables."""

    def __init__(self, parent, controller, kind, columns, headers, get_items, add_fn, update_fn, remove_fn):
        super().__init__(parent, style="TFrame", padding=(0, 14, 0, 0))
        self.controller = controller
        self.kind = kind
        self.columns = columns
        self.headers = headers
        self.get_items = get_items
        self.add_fn = add_fn
        self.update_fn = update_fn
        self.remove_fn = remove_fn

        toolbar = ttk.Frame(self, style="TFrame")
        toolbar.pack(fill="x", pady=(0, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())
        ttk.Entry(toolbar, textvariable=self.search_var, width=40).pack(side="left")
        ttk.Label(toolbar, text="🔍 Search by name").pack(side="left", padx=10)
        ttk.Button(toolbar, text="+ Add", style="Primary.TButton",
                   command=self.open_add_dialog).pack(side="right")

        card = Card(self)
        card.pack(fill="both", expand=True)

        tree_frame = ttk.Frame(card, style="Card.TFrame")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, anchor="center", width=110)
        self.tree.tag_configure("expired", foreground=theme.DANGER)
        self.tree.tag_configure("soon", foreground=theme.WARNING)
        self.tree.tag_configure("low_stock", background="#FFF3E0")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Delete", style="Danger.TButton",
                   command=self.delete_selected).pack(side="right", padx=6)
        ttk.Button(actions, text="Edit", style="Ghost.TButton",
                   command=self.open_edit_dialog).pack(side="right", padx=6)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()

        for med in self.get_items():
            if query and query not in med.name.lower():
                continue

            row = [getattr(med, col) for col in self.columns]
            tags = []
            status = expiry_status(med.expiry_date)
            if status in ("expired", "soon"):
                tags.append(status)
            if med.quantity < 10:
                tags.append("low_stock")

            self.tree.insert("", "end", iid=str(med.id), values=row, tags=tuple(tags))

    def _selected_item(self):
        selection = self.tree.selection()
        if not selection:
            return None
        item_id = int(selection[0])
        return next((m for m in self.get_items() if m.id == item_id), None)

    def _common_fields(self, initial):
        return [
            {"key": "name", "label": "Medicine Name", "initial": initial.get("name", "")},
            {"key": "purpose", "label": "Purpose / Usage", "initial": initial.get("purpose", "")},
            {"key": "price", "label": "Price", "initial": initial.get("price", "")},
            {"key": "quantity", "label": "Total Quantity", "initial": initial.get("quantity", "")},
        ]

    def _date_fields(self, initial):
        return [
            {"key": "production_date", "label": "Production Date (DD/MM/YYYY)",
             "initial": initial.get("production_date", "")},
            {"key": "expiry_date", "label": "Expiry Date (DD/MM/YYYY)",
             "initial": initial.get("expiry_date", "")},
            {"key": "leaflet", "label": "Medicine Leaflet (optional)", "required": False,
             "initial": initial.get("leaflet", "")},
        ]

    def _fields(self, initial=None):
        initial = initial or {}
        fields = self._common_fields(initial)

        if self.kind == "solid":
            fields += [
                {"key": "strips", "label": "Number of Strips", "initial": initial.get("strips", "")},
                {"key": "pills_per_strip", "label": "Pills per Strip",
                 "initial": initial.get("pills_per_strip", "")},
            ]
        else:
            fields += [
                {"key": "volume", "label": "Volume", "initial": initial.get("volume", "")},
                {"key": "unit", "label": "Unit", "type": "select", "options": UNITS,
                 "initial": initial.get("unit", UNITS[0])},
            ]

        return fields + self._date_fields(initial)

    def _validators(self):
        numeric = lambda v: None if v.replace(".", "", 1).isdigit() else "Must be a number"
        return {
            "price": numeric, "quantity": numeric,
            "strips": numeric, "pills_per_strip": numeric, "volume": numeric,
            "production_date": validate_date_field, "expiry_date": validate_date_field,
        }

    def open_add_dialog(self):
        FormDialog(self.controller, "Add Medicine", self._fields(), self._handle_add,
                   validators=self._validators())

    def open_edit_dialog(self):
        item = self._selected_item()
        if not item:
            Toast(self.controller, "Please select a medicine first", kind="error")
            return

        initial = {col: getattr(item, col) for col in self.columns if col != "id"}
        initial["leaflet"] = item.leaflet or ""
        FormDialog(self.controller, "Edit Medicine", self._fields(initial),
                   lambda values: self._handle_edit(item, values),
                   validators=self._validators())

    def _handle_add(self, values):
        new_id = next_id(self.get_items())

        if self.kind == "solid":
            self.add_fn(new_id, values["name"], values["purpose"], float(values["price"]),
                        float(values["quantity"]), int(values["strips"]), int(values["pills_per_strip"]),
                        values["production_date"], values["expiry_date"], values["leaflet"] or None)
        else:
            self.add_fn(new_id, values["name"], values["purpose"], float(values["price"]),
                        float(values["quantity"]), float(values["volume"]), values["unit"],
                        values["production_date"], values["expiry_date"], values["leaflet"] or None)

        self.controller.refresh_all()
        Toast(self.controller, "Medicine added successfully")

    def _handle_edit(self, item, values):
        item.name = values["name"]
        item.purpose = values["purpose"]
        item.price = float(values["price"])
        item.quantity = float(values["quantity"])
        item.production_date = values["production_date"]
        item.expiry_date = values["expiry_date"]
        item.leaflet = values["leaflet"] or None

        if self.kind == "solid":
            item.strips = int(values["strips"])
            item.pills_per_strip = int(values["pills_per_strip"])
        else:
            item.volume = float(values["volume"])
            item.unit = values["unit"]

        self.update_fn(item)
        self.controller.refresh_all()
        Toast(self.controller, "Medicine updated successfully")

    def delete_selected(self):
        item = self._selected_item()
        if not item:
            Toast(self.controller, "Please select a medicine first", kind="error")
            return

        def do_delete():
            self.remove_fn(item.id)
            self.controller.refresh_all()
            Toast(self.controller, "Medicine deleted successfully")

        ConfirmDialog(self.controller, "Delete Medicine",
                      f"Are you sure you want to delete '{item.name}'?", do_delete)
