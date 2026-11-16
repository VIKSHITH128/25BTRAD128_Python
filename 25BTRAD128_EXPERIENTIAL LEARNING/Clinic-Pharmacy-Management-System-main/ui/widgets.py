"""
Small reusable UI building blocks shared across pages:
- Card: a white rounded-looking container
- FormDialog: a generic popup form used for Add/Edit everywhere
- ConfirmDialog: yes/no confirmation before delete
- Toast: small temporary notification instead of blocking msgboxes
"""

import tkinter as tk
from tkinter import ttk

from ui import theme


class Card(ttk.Frame):
    """A white panel with padding, used to group content on every page."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, style="Card.TFrame", padding=18, **kwargs)


class KPI(ttk.Frame):
    """Small stat card used on the dashboard (title + big number)."""

    def __init__(self, parent, title, value, accent=theme.PRIMARY):
        super().__init__(parent, style="Card.TFrame", padding=16)
        bar = tk.Frame(self, bg=accent, width=4)
        bar.pack(side="left", fill="y")

        inner = ttk.Frame(self, style="Card.TFrame")
        inner.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self.value_lbl = ttk.Label(inner, text=str(value), style="KPI.TLabel")
        self.value_lbl.pack(anchor="w")
        ttk.Label(inner, text=title, style="Muted.TLabel").pack(anchor="w")

    def set_value(self, value):
        self.value_lbl.configure(text=str(value))


class Toast(tk.Toplevel):
    """A small non-blocking notification that fades away on its own."""

    def __init__(self, parent, message, kind="success"):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        color = {"success": theme.SUCCESS, "error": theme.DANGER, "info": theme.PRIMARY}.get(kind, theme.SUCCESS)

        frame = tk.Frame(self, bg=color, padx=18, pady=12)
        frame.pack()
        tk.Label(frame, text=message, bg=color, fg="white", font=theme.FONT_BODY_BOLD).pack()

        parent.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        self.update_idletasks()
        w = self.winfo_width()
        self.geometry(f"+{px + pw - w - 30}+{py + 40}")

        self.after(2200, self.destroy)


class ConfirmDialog(tk.Toplevel):
    """Simple centered yes/no confirmation dialog."""

    def __init__(self, parent, title, message, on_confirm):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=theme.CARD_BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        pad = ttk.Frame(self, style="Card.TFrame", padding=24)
        pad.pack(fill="both", expand=True)

        ttk.Label(pad, text=message, style="Card.TLabel", wraplength=320,
                  justify="center").pack(pady=(0, 18))

        btns = ttk.Frame(pad, style="Card.TFrame")
        btns.pack()

        def confirm():
            self.destroy()
            on_confirm()

        ttk.Button(btns, text="Cancel", style="Ghost.TButton", command=self.destroy).pack(side="right", padx=6)
        ttk.Button(btns, text="Confirm Delete", style="Danger.TButton", command=confirm).pack(side="right", padx=6)

        self._center_over(parent)

    def _center_over(self, parent):
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")


class FormDialog(tk.Toplevel):
    """
    Generic popup form.

    fields: list of dicts, each like:
        {"key": "name", "label": "الاسم", "type": "text"|"number"|"select"|"date",
         "options": [...] (only for select), "initial": value}

    on_submit(values_dict) is called only after all validators pass.
    validators: optional dict {key: callable(value) -> error_message_or_None}
    """

    def __init__(self, parent, title, fields, on_submit, validators=None, width=420, auto_fill=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=theme.CARD_BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.fields = fields
        self.validators = validators or {}
        self.on_submit = on_submit
        self.vars = {}
        self.error_labels = {}
        # auto_fill: {source_key: (target_key, func(value) -> str_or_None)}
        # e.g. auto-computing age from a national id once the user leaves that field.
        self.auto_fill = auto_fill or {}

        container = ttk.Frame(self, style="Card.TFrame", padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=title, style="H2.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        row = 1
        for f in fields:
            ttk.Label(container, text=f["label"], style="Card.TLabel").grid(
                row=row, column=0, sticky="w", pady=(6, 0))
            row += 1

            var = tk.StringVar(value=f.get("initial", ""))
            self.vars[f["key"]] = var

            if f.get("type") == "select":
                widget = ttk.Combobox(container, textvariable=var, values=f.get("options", []),
                                       state="readonly", width=34)
            else:
                widget = ttk.Entry(container, textvariable=var, width=36)

            widget.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 2))
            row += 1

            if f["key"] in self.auto_fill:
                widget.bind("<FocusOut>", self._make_auto_fill_handler(f["key"]))

            err = ttk.Label(container, text="", style="Card.TLabel", foreground=theme.DANGER)
            err.grid(row=row, column=0, columnspan=2, sticky="w")
            self.error_labels[f["key"]] = err
            row += 1

        btns = ttk.Frame(container, style="Card.TFrame")
        btns.grid(row=row, column=0, columnspan=2, pady=(18, 0), sticky="e")

        ttk.Button(btns, text="Cancel", style="Ghost.TButton", command=self.destroy).pack(side="right", padx=6)
        ttk.Button(btns, text="Save", style="Primary.TButton", command=self._submit).pack(side="right", padx=6)

        container.columnconfigure(0, weight=1)
        self.bind("<Return>", lambda e: self._submit())

        self._center_over(parent)

    def _center_over(self, parent):
        self.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _make_auto_fill_handler(self, source_key):
        target_key, func = self.auto_fill[source_key]

        def handler(event):
            if self.vars[target_key].get().strip():
                return  # don't override a value the user already typed
            result = func(self.vars[source_key].get().strip())
            if result is not None:
                self.vars[target_key].set(str(result))

        return handler

    def _submit(self):
        values = {k: v.get().strip() for k, v in self.vars.items()}
        has_error = False

        for key, err_label in self.error_labels.items():
            err_label.configure(text="")

        for f in self.fields:
            key = f["key"]
            value = values[key]

            if f.get("required", True) and not value:
                self.error_labels[key].configure(text="This field is required")
                has_error = True
                continue

            validator = self.validators.get(key)
            if validator and value:
                message = validator(value)
                if message:
                    self.error_labels[key].configure(text=message)
                    has_error = True

        if has_error:
            return

        self.on_submit(values)
        self.destroy()
