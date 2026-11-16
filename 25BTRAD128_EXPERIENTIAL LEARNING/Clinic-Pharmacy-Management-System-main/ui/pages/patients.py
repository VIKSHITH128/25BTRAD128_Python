import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.widgets import Card, FormDialog, ConfirmDialog, Toast
from ui.helpers import (
    next_id, calc_age_from_national_id, validate_email_field,
    validate_phone_field, validate_national_id_field,
)
from core.session import Session
from persistence.database import add_patient, update_patient, remove_patient_by_id

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
GENDERS = ["Male", "Female"]

COLUMNS = ("id", "name", "age", "gender", "phone", "email", "blood_type")
HEADERS = {
    "id": "National ID", "name": "Name", "age": "Age", "gender": "Gender",
    "phone": "Phone", "email": "Email", "blood_type": "Blood Type",
}


class PatientsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller

        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Patients", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="+ Add Patient", style="Primary.TButton",
                   command=self.open_add_dialog).pack(side="right")

        toolbar = ttk.Frame(self, style="TFrame")
        toolbar.pack(fill="x", pady=(0, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())
        ttk.Entry(toolbar, textvariable=self.search_var, width=40).pack(side="left")
        ttk.Label(toolbar, text="🔍 Search by name or national ID").pack(side="left", padx=10)

        card = Card(self)
        card.pack(fill="both", expand=True)

        tree_frame = ttk.Frame(card, style="Card.TFrame")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=COLUMNS, show="headings", selectmode="browse")
        for col in COLUMNS:
            self.tree.heading(col, text=HEADERS[col])
            self.tree.column(col, anchor="center", width=130)
        self.tree.column("email", width=180)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="View Medical History", style="Ghost.TButton",
                   command=self.open_history).pack(side="right", padx=(6, 0))
        ttk.Button(actions, text="Delete", style="Danger.TButton",
                   command=self.delete_selected).pack(side="right", padx=6)
        ttk.Button(actions, text="Edit", style="Ghost.TButton",
                   command=self.open_edit_dialog).pack(side="right", padx=6)

    def on_show(self):
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()

        for p in Session.patients:
            if query and query not in p.name.lower() and query not in str(p.id):
                continue
            self.tree.insert("", "end", iid=str(p.id), values=(
                p.id, p.name, p.age, p.gender, p.phone, p.email, p.blood_type
            ))

    def _selected_patient(self):
        selection = self.tree.selection()
        if not selection:
            return None
        pid = int(selection[0])
        return next((p for p in Session.patients if p.id == pid), None)

    def _fields(self, initial=None):
        initial = initial or {}
        return [
            {"key": "id", "label": "National ID (14 digits)", "initial": initial.get("id", "")},
            {"key": "name", "label": "Full Name", "initial": initial.get("name", "")},
            {"key": "age", "label": "Age", "initial": initial.get("age", "")},
            {"key": "gender", "label": "Gender", "type": "select", "options": GENDERS,
             "initial": initial.get("gender", GENDERS[0])},
            {"key": "phone", "label": "Phone Number", "initial": initial.get("phone", "")},
            {"key": "email", "label": "Email Address", "initial": initial.get("email", "")},
            {"key": "lic_no", "label": "Card/File Number", "required": False,
             "initial": initial.get("lic_no", "")},
            {"key": "blood_type", "label": "Blood Type", "type": "select", "options": BLOOD_TYPES,
             "initial": initial.get("blood_type", BLOOD_TYPES[0])},
        ]

    def _validators(self):
        return {
            "id": validate_national_id_field,
            "email": validate_email_field,
            "phone": validate_phone_field,
            "age": lambda v: None if v.isdigit() and 0 < int(v) < 120 else "Invalid age",
        }

    def open_add_dialog(self):
        FormDialog(
            self.controller, "Add New Patient", self._fields(), self._handle_add,
            validators=self._validators(),
            auto_fill={"id": ("age", calc_age_from_national_id)},
        )

    def open_edit_dialog(self):
        patient = self._selected_patient()
        if not patient:
            Toast(self.controller, "Please select a patient first", kind="error")
            return

        initial = {
            "id": patient.id, "name": patient.name, "age": patient.age,
            "gender": patient.gender, "phone": patient.phone, "email": patient.email,
            "lic_no": patient.lic_no, "blood_type": patient.blood_type,
        }
        FormDialog(
            self.controller, "Edit Patient Details", self._fields(initial),
            lambda values: self._handle_edit(patient, values),
            validators=self._validators(),
        )

    def _handle_add(self, values):
        new_id = int(values["id"])
        if any(p.id == new_id for p in Session.patients):
            Toast(self.controller, "National ID already registered", kind="error")
            return

        add_patient(new_id, values["name"], int(values["age"]), values["gender"],
                    values["phone"], values["email"], values["lic_no"] or "-", values["blood_type"])
        self.controller.refresh_all()
        Toast(self.controller, "Patient added successfully")

    def _handle_edit(self, patient, values):
        patient.name = values["name"]
        patient.age = int(values["age"])
        patient.gender = values["gender"]
        patient.phone = values["phone"]
        patient.email = values["email"]
        patient.lic_no = values["lic_no"] or "-"
        patient.blood_type = values["blood_type"]

        update_patient(patient)
        self.controller.refresh_all()
        Toast(self.controller, "Patient updated successfully")

    def delete_selected(self):
        patient = self._selected_patient()
        if not patient:
            Toast(self.controller, "Please select a patient first", kind="error")
            return

        def do_delete():
            remove_patient_by_id(patient.id)
            self.controller.refresh_all()
            Toast(self.controller, "Patient deleted successfully")

        ConfirmDialog(self.controller, "Delete Patient",
                      f"Are you sure you want to delete patient '{patient.name}'?\nTheir medical history will also be removed.",
                      do_delete)

    def open_history(self):
        patient = self._selected_patient()
        if not patient:
            Toast(self.controller, "Please select a patient first", kind="error")
            return
        self.controller.show_page("history")
        self.controller.pages["history"].select_patient(patient.id)
