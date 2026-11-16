import tkinter as tk
from tkinter import ttk

from ui.widgets import Card, FormDialog, ConfirmDialog, Toast
from ui.helpers import validate_date_field
from core.session import Session
from persistence.database import add_medical_history, update_medical_history, remove_medical_history

COLUMNS = ("diagnosis", "treatment", "doctor", "date", "notes")
HEADERS = {
    "diagnosis": "Diagnosis", "treatment": "Treatment", "doctor": "Attending Doctor",
    "date": "Date", "notes": "Notes",
}


class MedicalHistoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller
        self.current_patient_id = None

        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Medical Records", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="+ Add Record", style="Primary.TButton",
                   command=self.open_add_dialog).pack(side="right")

        selector_row = ttk.Frame(self, style="TFrame")
        selector_row.pack(fill="x", pady=(0, 10))
        ttk.Label(selector_row, text="Select Patient:").pack(side="left", padx=(0, 8))
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(selector_row, textvariable=self.patient_var,
                                           state="readonly", width=45)
        self.patient_combo.pack(side="left")
        self.patient_combo.bind("<<ComboboxSelected>>", lambda e: self._on_patient_selected())

        card = Card(self)
        card.pack(fill="both", expand=True)

        tree_frame = ttk.Frame(card, style="Card.TFrame")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=COLUMNS, show="headings", selectmode="browse")
        for col in COLUMNS:
            self.tree.heading(col, text=HEADERS[col])
            self.tree.column(col, anchor="center", width=140)
        self.tree.column("notes", width=200)

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

    def on_show(self):
        self._populate_patient_list()

    def refresh(self):
        self._populate_patient_list()
        self._render_history()

    def _populate_patient_list(self):
        options = [f"{p.id} - {p.name}" for p in Session.patients]
        self.patient_combo.configure(values=options)

        if self.current_patient_id is not None:
            match = next((o for o in options if o.startswith(f"{self.current_patient_id} -")), None)
            if match:
                self.patient_var.set(match)
            else:
                self.current_patient_id = None
                self.patient_var.set("")
        self._render_history()

    def select_patient(self, patient_id):
        self.current_patient_id = patient_id
        self._populate_patient_list()

    def _on_patient_selected(self):
        value = self.patient_var.get()
        if value:
            self.current_patient_id = int(value.split(" - ")[0])
        self._render_history()

    def _current_patient(self):
        if self.current_patient_id is None:
            return None
        return next((p for p in Session.patients if p.id == self.current_patient_id), None)

    def _render_history(self):
        self.tree.delete(*self.tree.get_children())
        patient = self._current_patient()
        if not patient:
            return

        for h in patient.medical_history:
            self.tree.insert("", "end", iid=str(h.id), values=(
                h.diagnosis, h.treatment, h.doctor, h.date, h.notes or ""
            ))

    def _selected_history(self):
        patient = self._current_patient()
        selection = self.tree.selection()
        if not patient or not selection:
            return None
        hid = int(selection[0])
        return next((h for h in patient.medical_history if h.id == hid), None)

    def _doctor_names(self):
        return [d.name for d in Session.doctors] or ["-"]

    def _fields(self, initial=None):
        initial = initial or {}
        return [
            {"key": "diagnosis", "label": "Diagnosis", "initial": initial.get("diagnosis", "")},
            {"key": "treatment", "label": "Treatment", "initial": initial.get("treatment", "")},
            {"key": "doctor", "label": "Attending Doctor", "type": "select",
             "options": self._doctor_names(), "initial": initial.get("doctor", self._doctor_names()[0])},
            {"key": "date", "label": "Date (DD/MM/YYYY)", "initial": initial.get("date", "")},
            {"key": "notes", "label": "Notes (optional)", "required": False,
             "initial": initial.get("notes", "")},
        ]

    def open_add_dialog(self):
        patient = self._current_patient()
        if not patient:
            Toast(self.controller, "Please select a patient first", kind="error")
            return

        FormDialog(self.controller, f"Add Medical Record - {patient.name}", self._fields(),
                   self._handle_add, validators={"date": validate_date_field})

    def open_edit_dialog(self):
        history = self._selected_history()
        if not history:
            Toast(self.controller, "Please select a record first", kind="error")
            return

        initial = {
            "diagnosis": history.diagnosis, "treatment": history.treatment,
            "doctor": history.doctor, "date": history.date, "notes": history.notes or "",
        }
        FormDialog(self.controller, "Edit Medical Record", self._fields(initial),
                   lambda values: self._handle_edit(history, values),
                   validators={"date": validate_date_field})

    def _next_history_id(self):
        all_ids = [h.id for p in Session.patients for h in p.medical_history]
        return (max(all_ids) + 1) if all_ids else 1

    def _handle_add(self, values):
        patient = self._current_patient()
        new_id = self._next_history_id()

        add_medical_history(new_id, patient.id, values["diagnosis"], values["treatment"],
                             values["doctor"], values["date"], values["notes"] or None)
        self.refresh()
        Toast(self.controller, "Medical record added successfully")

    def _handle_edit(self, history, values):
        patient = self._current_patient()

        # persistence.update_medical_history() matches the row to update by
        # (patient_id, diagnosis, date), using the SAME new values for both the
        # SET and the WHERE clause. That means it can only succeed here when
        # diagnosis and date are unchanged. If either changed, we fall back to
        # remove-old + add-new (both already-existing, untouched backend calls)
        # so the edit still saves correctly instead of silently failing.
        diagnosis_or_date_changed = (
            values["diagnosis"] != history.diagnosis or values["date"] != history.date
        )

        if diagnosis_or_date_changed:
            remove_medical_history(patient.id, history.diagnosis, history.date)
            add_medical_history(self._next_history_id(), patient.id, values["diagnosis"],
                                 values["treatment"], values["doctor"], values["date"],
                                 values["notes"] or None)
        else:
            history.treatment = values["treatment"]
            history.doctor = values["doctor"]
            history.notes = values["notes"] or None
            update_medical_history(patient.id, history)

        self.refresh()
        Toast(self.controller, "Medical record updated successfully")

    def delete_selected(self):
        history = self._selected_history()
        patient = self._current_patient()
        if not history or not patient:
            Toast(self.controller, "Please select a record first", kind="error")
            return

        def do_delete():
            remove_medical_history(patient.id, history.diagnosis, history.date)
            self.refresh()
            Toast(self.controller, "Record deleted successfully")

        ConfirmDialog(self.controller, "Delete Medical Record",
                      "Are you sure you want to delete this record?", do_delete)
