import os

DATABASE_NAME = "clinic_pharmacy.db"

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    DATABASE_NAME
)

APP_NAME = "Clinic & Pharmacy Management System"

DATE_FORMAT = "%d/%m/%Y"