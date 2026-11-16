import sqlite3
from config import DATABASE_PATH
from core.models import *
from core.session import *

def execute_query(query: str, params: tuple = ()):

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:

            cursor = connection.cursor()
            cursor.execute(query, params)

            command = query.strip().split()[0].upper()

            if command == "SELECT":
                return cursor.fetchall()

            elif command == "INSERT":
                return cursor.lastrowid

            elif command in ("UPDATE", "DELETE"):
                return cursor.rowcount

            return True

    except sqlite3.Error:
        raise

def create_data_tables():

    solid_medicine_query = """
                           CREATE TABLE IF NOT EXISTS solid_medicines (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            purpose TEXT,
                            price REAL,
                            quantity REAL,
                            strips INTEGER,
                            pills_per_strip INTEGER,
                            production_date TEXT,
                            expiry_date TEXT,
                            leaflet TEXT
                        )
                            """
    
    liquid_medicine_query = """
                        CREATE TABLE IF NOT EXISTS liquid_medicines (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            purpose TEXT,
                            price REAL,
                            quantity REAL,
                            volume REAL,
                            unit TEXT,
                            production_date TEXT,
                            expiry_date TEXT,
                            leaflet TEXT
                        )
                        """
    
    patient_query = """
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    phone TEXT,
                    email TEXT,
                    lic_no TEXT,
                    blood_type TEXT
                )
                """
    
    doctor_query = """
               CREATE TABLE IF NOT EXISTS doctors (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   age INTEGER,
                   gender TEXT,
                   phone TEXT,
                   email TEXT,
                   lic_no TEXT,
                   department TEXT,
                   salary REAL
               )
               """
    
    medical_history_query = """
                        CREATE TABLE IF NOT EXISTS medical_history (
                            id INTEGER PRIMARY KEY,
                            patient_id INTEGER,
                            diagnosis TEXT,
                            treatment TEXT,
                            doctor TEXT,
                            date TEXT,
                            notes TEXT,
                            FOREIGN KEY (patient_id) REFERENCES patients(id)
                        )
                        """
    
    queries = (
                patient_query,
                doctor_query,
                solid_medicine_query,
                liquid_medicine_query,
                medical_history_query,
            )

    for query in queries:
        execute_query(query)

def add_solid_medicine(id, name, purpose, price,
                       quantity, strips, pills_per_strip,
                       production_date, expiry_date, leaflet=None):
    
    Session.solid_medicines.append(SolidMedicine(id, name, purpose, price,
                                                 quantity, strips, pills_per_strip,
                                                 production_date, expiry_date, leaflet))

    query = """
            INSERT INTO solid_medicines (
                id,
                name,
                purpose,
                price,
                quantity,
                strips,
                pills_per_strip,
                production_date,
                expiry_date,
                leaflet
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    return execute_query(query,
                        (id, name, purpose, price,
                         quantity, strips, pills_per_strip,
                         production_date, expiry_date, leaflet))
    
def add_liquid_medicine(id, name, purpose, price, 
                        quantity,volume, unit, 
                        production_date, expiry_date, leaflet=None):
    
    Session.liquid_medicines.append(LiquidMedicine(id, name, purpose, price, 
                                                   quantity,volume, unit, 
                                                   production_date, expiry_date, leaflet))
    
    query = """
            INSERT INTO liquid_medicines (
                id,
                name,
                purpose,
                price,
                quantity,
                volume,
                unit,
                production_date,
                expiry_date,
                leaflet
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    return execute_query(query,
                        (id, name, purpose, price, 
                         quantity,volume, unit, 
                         production_date, expiry_date, leaflet))

def get_solid_medicines():

    solid_medicines_list = []
    solid_medicines_data = execute_query("SELECT * FROM solid_medicines")

    for solid_medicine in solid_medicines_data:

        solid_medicines_list.append(SolidMedicine(
            solid_medicine[0],
            solid_medicine[1],
            solid_medicine[2],
            solid_medicine[3],
            solid_medicine[4],
            solid_medicine[5],
            solid_medicine[6],
            solid_medicine[7],
            solid_medicine[8],
            solid_medicine[9]
        ))

    return solid_medicines_list

def get_liquid_medicines():

    liquid_medicines_list = []
    liquid_medicines_data = execute_query("SELECT * FROM liquid_medicines")

    for liquid_medicine in liquid_medicines_data:

        liquid_medicines_list.append(LiquidMedicine(
            liquid_medicine[0],
            liquid_medicine[1],
            liquid_medicine[2],
            liquid_medicine[3],
            liquid_medicine[4],
            liquid_medicine[5],
            liquid_medicine[6],
            liquid_medicine[7],
            liquid_medicine[8],
            liquid_medicine[9]
        ))

    return liquid_medicines_list
    
def is_solid_medicine_exists(solid_medicine):
    return solid_medicine in Session.solid_medicines

def is_liquid_medicine_exists(liquid_medicine):
    return liquid_medicine in Session.liquid_medicines

def update_solid_medicine(udpated_medicine : SolidMedicine):

    for i, solid_medicine in enumerate(Session.solid_medicines):
        if solid_medicine.id == udpated_medicine.id:
            Session.solid_medicines[i] = udpated_medicine
            break

    query = """
            UPDATE solid_medicines
            SET 
                name            = ?,
                purpose         = ?,
                price           = ?,
                quantity        = ?,
                strips          = ?,
                pills_per_strip = ?,
                production_date = ?,
                expiry_date     = ?,
                leaflet         = ?
            WHERE id            = ?
            """

    return execute_query(query,
                        (udpated_medicine.name,
                         udpated_medicine.purpose,
                         udpated_medicine.price, 
                         udpated_medicine.quantity,
                         udpated_medicine.strips,
                         udpated_medicine.pills_per_strip, 
                         udpated_medicine.production_date,
                         udpated_medicine.expiry_date,
                         udpated_medicine.leaflet,
                         udpated_medicine.id))

def update_liquid_medicine(udpated_medicine : LiquidMedicine):

    for i, liquid_medicine in enumerate(Session.liquid_medicines):
        if liquid_medicine.id == udpated_medicine.id:
            Session.liquid_medicines[i] = udpated_medicine
            break

    query = """
            UPDATE liquid_medicines
            SET 
                name            = ?,
                purpose         = ?,
                price           = ?,
                quantity        = ?,
                volume          = ?,
                unit            = ?,
                production_date = ?,
                expiry_date     = ?,
                leaflet         = ?
            WHERE id            = ?
            """

    return execute_query(query,
                        (udpated_medicine.name,
                         udpated_medicine.purpose,
                         udpated_medicine.price, 
                         udpated_medicine.quantity,
                         udpated_medicine.volume,
                         udpated_medicine.unit, 
                         udpated_medicine.production_date,
                         udpated_medicine.expiry_date,
                         udpated_medicine.leaflet,
                         udpated_medicine.id))

def remove_solid_medicine_by_id(solid_medicine_id):

    query = """
            DELETE FROM solid_medicines
            WHERE id = ?
            """
    
    result = execute_query(query, (solid_medicine_id,))

    if result:
        SolidMedicine.remove_solid_medicine(solid_medicine_id)

    return result

def remove_liquid_medicine_by_id(liquid_medicine_id):
    
    query = """
            DELETE FROM liquid_medicines
            WHERE id = ?
            """
    
    result = execute_query(query, (liquid_medicine_id,))

    if result:
        LiquidMedicine.remove_liquid_medicine(liquid_medicine_id)

    return result

def add_doctor(id, name, age, gender,
               phone, email, lic_no,
               department, salary):

    Session.doctors.append(
        Doctor(
            id,
            name,
            age,
            gender,
            phone,
            email,
            lic_no,
            department,
            salary
        )
    )

    query = """
            INSERT INTO doctors (
                id,
                name,
                age,
                gender,
                phone,
                email,
                lic_no,
                department,
                salary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    return execute_query(
        query,
        (
            id,
            name,
            age,
            gender,
            phone,
            email,
            lic_no,
            department,
            salary
        )
    )

def get_doctors():

    doctors_list = []
    doctors_data = execute_query("SELECT * FROM doctors")

    for doctor in doctors_data:

        doctors_list.append(
            Doctor(
                doctor[0],
                doctor[1],
                doctor[2],
                doctor[3],
                doctor[4],
                doctor[5],
                doctor[6],
                doctor[7],
                doctor[8]
            )
        )

    return doctors_list

def is_doctor_exists(doctor):
    return doctor in Session.doctors

def update_doctor(updated_doctor: Doctor):

    for i, doctor in enumerate(Session.doctors):
        if doctor.id == updated_doctor.id:
            Session.doctors[i] = updated_doctor
            break

    query = """
            UPDATE doctors
            SET
                name       = ?,
                age        = ?,
                gender     = ?,
                phone      = ?,
                email      = ?,
                lic_no     = ?,
                department = ?,
                salary     = ?
            WHERE id = ?
            """

    return execute_query(
        query,
        (
            updated_doctor.name,
            updated_doctor.age,
            updated_doctor.gender,
            updated_doctor.phone,
            updated_doctor.email,
            updated_doctor.lic_no,
            updated_doctor.department,
            updated_doctor.salary,
            updated_doctor.id
        )
    )

def remove_doctor_by_id(doctor_id):

    query = """
            DELETE FROM doctors
            WHERE id = ?
            """

    result = execute_query(query, (doctor_id,))

    if result:
        Doctor.remove_doctor(doctor_id)

    return result

def add_medical_history(id, patient_id,
                        diagnosis, treatment,
                        doctor, date, notes=None):

    query = """
            INSERT INTO medical_history (
                id,
                patient_id,
                diagnosis,
                treatment,
                doctor,
                date,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

    result = execute_query(
        query,
        (
            id,
            patient_id,
            diagnosis,
            treatment,
            doctor,
            date,
            notes
        )
    )

    if result:

        for patient in Session.patients:
            if patient.id == patient_id:
                patient.add_medical_history(
                    MedicalHistory(
                        id,
                        patient_id,
                        diagnosis,
                        treatment,
                        doctor,
                        date,
                        notes
                    )
                )
                break

    return result

def get_medical_history(patient_id):

    query = """
            SELECT
                id,
                patient_id,
                diagnosis,
                treatment,
                doctor,
                date,
                notes
            FROM medical_history
            WHERE patient_id = ?
            """

    history_list = []

    history_data = execute_query(query, (patient_id,))

    for history in history_data:

        history_list.append(
            MedicalHistory(
                history[0],
                history[1],
                history[2],
                history[3],
                history[4],
                history[5],
                history[6]
            )
        )

    return history_list

def update_medical_history(patient_id, updated_history: MedicalHistory):

    query = """
            UPDATE medical_history
            SET
                diagnosis = ?,
                treatment = ?,
                doctor    = ?,
                date      = ?,
                notes     = ?
            WHERE
                patient_id = ?
                AND diagnosis = ?
                AND date = ?
            """

    result = execute_query(
        query,
        (
            updated_history.diagnosis,
            updated_history.treatment,
            updated_history.doctor,
            updated_history.date,
            updated_history.notes,
            patient_id,
            updated_history.diagnosis,
            updated_history.date
        )
    )

    if result:

        for patient in Session.patients:
            if patient.id == patient_id:
                for i, history in enumerate(patient.medical_history):
                    if (history.diagnosis == updated_history.diagnosis and
                        history.date == updated_history.date):
                        patient.medical_history[i] = updated_history
                        break

    return result

def remove_medical_history(patient_id,
                           diagnosis,
                           date):

    query = """
            DELETE FROM medical_history
            WHERE
                patient_id = ?
                AND diagnosis = ?
                AND date = ?
            """

    result = execute_query(
        query,
        (
            patient_id,
            diagnosis,
            date
        )
    )

    if result:

        for patient in Session.patients:
            if patient.id == patient_id:
                for history in patient.medical_history:
                    if (history.diagnosis == diagnosis and
                        history.date == date):
                        patient.remove_medical_history(history)
                        break

    return result

def link_medical_histories():

    for patient in Session.patients:

        patient.clear_medical_history()

        medical_histories = get_medical_history(patient.id)

        for medical_history in medical_histories:
            patient.add_medical_history(medical_history)

def add_patient(id, name, age, gender,
                phone, email, lic_no,
                blood_type):

    Session.patients.append(
        Patient(
            id,
            name,
            age,
            gender,
            phone,
            email,
            lic_no,
            blood_type
        )
    )

    query = """
            INSERT INTO patients (
                id,
                name,
                age,
                gender,
                phone,
                email,
                lic_no,
                blood_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

    return execute_query(
        query,
        (
            id,
            name,
            age,
            gender,
            phone,
            email,
            lic_no,
            blood_type
        )
    )

def get_patients():

    patients_list = []
    patients_data = execute_query("SELECT * FROM patients")

    for patient in patients_data:

        patients_list.append(
            Patient(
                patient[0],
                patient[1],
                patient[2],
                patient[3],
                patient[4],
                patient[5],
                patient[6],
                patient[7]
            )
        )

    return patients_list

def is_patient_exists(patient):
    return patient in Session.patients

def update_patient(updated_patient: Patient):

    for i, patient in enumerate(Session.patients):
        if patient.id == updated_patient.id:
            Session.patients[i] = updated_patient
            break

    query = """
            UPDATE patients
            SET
                name       = ?,
                age        = ?,
                gender     = ?,
                phone      = ?,
                email      = ?,
                lic_no     = ?,
                blood_type = ?
            WHERE id = ?
            """

    return execute_query(
        query,
        (
            updated_patient.name,
            updated_patient.age,
            updated_patient.gender,
            updated_patient.phone,
            updated_patient.email,
            updated_patient.lic_no,
            updated_patient.blood_type,
            updated_patient.id
        )
    )

def remove_patient_by_id(patient_id):

    query = """
            DELETE FROM patients
            WHERE id = ?
            """

    result = execute_query(query, (patient_id,))

    if result:
        Patient.remove_patient(patient_id)

    return result

