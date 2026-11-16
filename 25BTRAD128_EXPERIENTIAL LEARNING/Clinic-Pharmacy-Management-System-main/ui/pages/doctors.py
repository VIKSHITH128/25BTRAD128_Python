import tkinter as tk
from tkinter import ttk

from ui.widgets import Card, FormDialog, ConfirmDialog, Toast
from ui.helpers import calc_age_from_national_id, validate_email_field, validate_phone_field, validate_national_id_field
from core.session import Session
from persistence.database import add_doctor, update_doctor, remove_doctor_by_id

GENDERS = ["Male", "Female"]
DEPARTMENTS = ["Internal Medicine", "Surgery", "Pediatrics", "Obstetrics & Gynecology", "Dentistry", "Orthopedics", "Dermatology", "Cardiology", "Ophthalmology", "ENT"]

COLUMNS = ("id", "name", "age", "gender", "department", "phone", "salary")
HEADERS = {
    "id": "National ID", "name": "Name", "age": "Age", "gender": "Gender",
    "department": "Department", "phone": "Phone", "salary": "Salary",
}


class DoctorsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="TFrame")
        self.controller = controller

        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Doctors", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="+ Add Doctor", style="Primary.TButton",
                   command=self.open_add_dialog).pack(side="right")

        toolbar = ttk.Frame(self, style="TFrame")
        toolbar.pack(fill="x", pady=(0, 10))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh())
        ttk.Entry(toolbar, textvariable=self.search_var, width=40).pack(side="left")
        ttk.Label(toolbar, text="🔍 Search by name or department").pack(side="left", padx=10)

        card = Card(self)
        card.pack(fill="both", expand=True)

        tree_frame = ttk.Frame(card, style="Card.TFrame")
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=COLUMNS, show="headings", selectmode="browse")
        for col in COLUMNS:
            self.tree.heading(col, text=HEADERS[col])
            self.tree.column(col, anchor="center", width=130)

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
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()

        for d in Session.doctors:
            if query and query not in d.name.lower() and query not in d.department.lower():
                continue
            self.tree.insert("", "end", iid=str(d.id), values=(
                d.id, d.name, d.age, d.gender, d.department, d.phone, d.salary
            ))

    def _selected_doctor(self):
        selection = self.tree.selection()
        if not selection:
            return None
        did = int(selection[0])
        return next((d for d in Session.doctors if d.id == did), None)

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
            {"key": "lic_no", "label": "License/Syndicate Number", "required": False,
             "initial": initial.get("lic_no", "")},
            {"key": "department", "label": "Department", "type": "select", "options": DEPARTMENTS,
             "initial": initial.get("department", DEPARTMENTS[0])},
            {"key": "salary", "label": "Salary", "initial": initial.get("salary", "")},
        ]

    def _validators(self):
        return {
            "id": validate_national_id_field,
            "email": validate_email_field,
            "phone": validate_phone_field,
            "age": lambda v: None if v.isdigit() and 0 < int(v) < 120 else "Invalid age",
            "salary": lambda v: None if v.replace(".", "", 1).isdigit() else "Salary must be a number",
        }

    def open_add_dialog(self):
        FormDialog(
            self.controller, "Add New Doctor", self._fields(), self._handle_add,
            validators=self._validators(),
            auto_fill={"id": ("age", calc_age_from_national_id)},
        )

    def open_edit_dialog(self):
        doctor = self._selected_doctor()
        if not doctor:
            Toast(self.controller, "Please select a doctor first", kind="error")
            return

        initial = {
            "id": doctor.id, "name": doctor.name, "age": doctor.age, "gender": doctor.gender,
            "phone": doctor.phone, "email": doctor.email, "lic_no": doctor.lic_no,
            "department": doctor.department, "salary": doctor.salary,
        }
        FormDialog(
            self.controller, "Edit Doctor Details", self._fields(initial),
            lambda values: self._handle_edit(doctor, values),
            validators=self._validators(),
        )

    def _handle_add(self, values):
        new_id = int(values["id"])
        if any(d.id == new_id for d in Session.doctors):
            Toast(self.controller, "National ID already registered", kind="error")
            return

        add_doctor(new_id, values["name"], int(values["age"]), values["gender"],
                   values["phone"], values["email"], values["lic_no"] or "-",
                   values["department"], float(values["salary"]))
        self.controller.refresh_all()
        Toast(self.controller, "Doctor added successfully")

    def _handle_edit(self, doctor, values):
        doctor.name = values["name"]
        doctor.age = int(values["age"])
        doctor.gender = values["gender"]
        doctor.phone = values["phone"]
        doctor.email = values["email"]
        doctor.lic_no = values["lic_no"] or "-"
        doctor.department = values["department"]
        doctor.salary = float(values["salary"])

        update_doctor(doctor)
        self.controller.refresh_all()
        Toast(self.controller, "Doctor updated successfully")

    def delete_selected(self):
        doctor = self._selected_doctor()
        if not doctor:
            Toast(self.controller, "Please select a doctor first", kind="error")
            return

        def do_delete():
            remove_doctor_by_id(doctor.id)
            self.controller.refresh_all()
            Toast(self.controller, "Doctor deleted successfully")

        ConfirmDialog(self.controller, "Delete Doctor",
                      f"Are you sure you want to delete doctor '{doctor.name}'?", do_delete)
