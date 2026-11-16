"""
Central place for colors, fonts and ttk styling.
Keeping this separate means every page looks consistent
without repeating style code everywhere.
"""

import tkinter as tk
from tkinter import ttk

# ---- Palette -----------------------------------------------------------
BG_DARK        = "#1E2A38"   # sidebar
BG_DARK_HOVER  = "#27384B"
BG_LIGHT       = "#F4F7FB"   # page background
CARD_BG        = "#FFFFFF"
PRIMARY        = "#2E86AB"   # main accent (medical blue)
PRIMARY_DARK   = "#22688A"
ACCENT_TEAL    = "#3FBFB0"
DANGER         = "#E4572E"
WARNING        = "#F2A007"
SUCCESS        = "#2FA36B"
TEXT_DARK      = "#1E2A38"
TEXT_MUTED     = "#6B7A90"
BORDER         = "#E1E7EF"

FONT_FAMILY      = "Segoe UI"
FONT_TITLE       = (FONT_FAMILY, 20, "bold")
FONT_SUBTITLE    = (FONT_FAMILY, 11)
FONT_H2          = (FONT_FAMILY, 14, "bold")
FONT_BODY        = (FONT_FAMILY, 10)
FONT_BODY_BOLD   = (FONT_FAMILY, 10, "bold")
FONT_NAV         = (FONT_FAMILY, 11)
FONT_KPI         = (FONT_FAMILY, 26, "bold")


def setup_style(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    root.configure(bg=BG_LIGHT)

    style.configure("TFrame", background=BG_LIGHT)
    style.configure("Card.TFrame", background=CARD_BG, relief="flat")
    style.configure("Sidebar.TFrame", background=BG_DARK)

    style.configure("TLabel", background=BG_LIGHT, foreground=TEXT_DARK, font=FONT_BODY)
    style.configure("Card.TLabel", background=CARD_BG, foreground=TEXT_DARK, font=FONT_BODY)
    style.configure("Title.TLabel", background=BG_LIGHT, foreground=TEXT_DARK, font=FONT_TITLE)
    style.configure("Subtitle.TLabel", background=BG_LIGHT, foreground=TEXT_MUTED, font=FONT_SUBTITLE)
    style.configure("H2.TLabel", background=CARD_BG, foreground=TEXT_DARK, font=FONT_H2)
    style.configure("Muted.TLabel", background=CARD_BG, foreground=TEXT_MUTED, font=FONT_BODY)
    style.configure("KPI.TLabel", background=CARD_BG, foreground=PRIMARY, font=FONT_KPI)
    style.configure("Sidebar.TLabel", background=BG_DARK, foreground="#FFFFFF", font=FONT_NAV)

    # Buttons
    style.configure("Primary.TButton",
                     background=PRIMARY, foreground="#FFFFFF",
                     font=FONT_BODY_BOLD, padding=(14, 8), borderwidth=0)
    style.map("Primary.TButton",
              background=[("active", PRIMARY_DARK), ("disabled", BORDER)])

    style.configure("Danger.TButton",
                     background=DANGER, foreground="#FFFFFF",
                     font=FONT_BODY_BOLD, padding=(14, 8), borderwidth=0)
    style.map("Danger.TButton", background=[("active", "#C6431B")])

    style.configure("Ghost.TButton",
                     background=CARD_BG, foreground=TEXT_DARK,
                     font=FONT_BODY_BOLD, padding=(12, 7), borderwidth=1)
    style.map("Ghost.TButton", background=[("active", BG_LIGHT)])

    style.configure("Nav.TButton",
                     background=BG_DARK, foreground="#D7E2EE",
                     font=FONT_NAV, padding=(16, 12), borderwidth=0, anchor="w")
    style.map("Nav.TButton",
              background=[("active", BG_DARK_HOVER)],
              foreground=[("active", "#FFFFFF")])

    style.configure("NavActive.TButton",
                     background=PRIMARY, foreground="#FFFFFF",
                     font=FONT_NAV, padding=(16, 12), borderwidth=0, anchor="w")
    style.map("NavActive.TButton", background=[("active", PRIMARY)])

    # Entries
    style.configure("TEntry", padding=6, fieldbackground="#FFFFFF")
    style.configure("TCombobox", padding=6)

    # Treeview (tables)
    style.configure("Treeview",
                     background="#FFFFFF", fieldbackground="#FFFFFF",
                     foreground=TEXT_DARK, rowheight=28, font=FONT_BODY, borderwidth=0)
    style.configure("Treeview.Heading",
                     background=PRIMARY, foreground="#FFFFFF",
                     font=FONT_BODY_BOLD, padding=(8, 8), relief="flat")
    style.map("Treeview.Heading", background=[("active", PRIMARY_DARK)])
    style.map("Treeview", background=[("selected", PRIMARY)], foreground=[("selected", "#FFFFFF")])

    style.configure("TNotebook", background=BG_LIGHT, borderwidth=0)
    style.configure("TNotebook.Tab", background=BG_LIGHT, padding=(16, 8), font=FONT_BODY_BOLD)
    style.map("TNotebook.Tab", background=[("selected", CARD_BG)], foreground=[("selected", PRIMARY)])

    return style
