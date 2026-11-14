
import json
import os
from datetime import datetime

FILE = "hospital_data.json"

# Doctor details
doctors = {
    "D101": {"name": "Dr. Arun", "speciality": "Cardiology", "fee": 800},
    "D102": {"name": "Dr. Priya", "speciality": "Neurology", "fee": 1000},
    "D103": {"name": "Dr. Rahul", "speciality": "General Medicine", "fee": 500},
    "D104": {"name": "Dr. Sneha", "speciality": "Dermatology", "fee": 600}
}

# Load saved hospital data
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as file:
            return json.load(file)

    return {
        "patients": [],
        "appointments": [],
        "bills": [],
        "patient_count": 0,
        "token_count": 0
    }


data = load_data()


# Save data automatically
def save_data():
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)


# Generate unique patient ID
def generate_patient_id():
    data["patient_count"] += 1
    return "PAT" + str(1000 + data["patient_count"])


# Generate unique token
def generate_token():
    data["token_count"] += 1
    return "TKN" + str(data["token_count"]).zfill(3)


# Register patient
def register_patient():
    print("\n========== PATIENT REGISTRATION ==========")

    name = input("Enter patient name: ")
    age = input("Enter age: ")
    gender = input("Enter gender: ")
    phone = input("Enter phone number: ")
    disease = input("Enter health problem: ")

    if not name.strip() or not age.isdigit() or not phone.isdigit():
        print("Invalid details! Please try again.")
        return

    patient_id = generate_patient_id()
    token = generate_token()

    patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "disease": disease,
        "token": token,
        "date": datetime.now().strftime("%d-%m-%Y")
    }

    data["patients"].append(patient)
    save_data()

    print("\nPatient registered successfully!")
    print("Patient ID:", patient_id)
    print("Unique Token:", token)


# Display doctors
def show_doctors():
    print("\n========== AVAILABLE DOCTORS ==========")

    for doctor_id, doctor in doctors.items():
        print("\nDoctor ID:", doctor_id)
        print("Name:", doctor["name"])
        print("Specialization:", doctor["speciality"])
        print("Consultation Fee: Rs.", doctor["fee"])


# Book appointment
def book_appointment():
    print("\n========== APPOINTMENT BOOKING ==========")

    patient_id = input("Enter patient ID: ").upper()

    patient = next(
        (p for p in data["patients"] if p["id"] == patient_id),
        None
    )

    if patient is None:
        print("Patient not found!")
        return

    show_doctors()

    doctor_id = input("\nEnter doctor ID: ").upper()

    if doctor_id not in doctors:
        print("Invalid doctor ID!")
        return

    appointment_date = input("Enter appointment date (DD-MM-YYYY): ")

    try:
        date = datetime.strptime(appointment_date, "%d-%m-%Y")
        if date.date() < datetime.now().date():
            print("Please select today or a future date.")
            return
    except ValueError:
        print("Invalid date format!")
        return

    appointment = {
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "doctor_id": doctor_id,
        "doctor_name": doctors[doctor_id]["name"],
        "date": appointment_date,
        "token": patient["token"],
        "status": "Confirmed"
    }

    data["appointments"].append(appointment)
    save_data()

    print("\nAppointment booked successfully!")
    print("Patient:", patient["name"])
    print("Doctor:", doctors[doctor_id]["name"])
    print("Date:", appointment_date)
    print("Token:", patient["token"])


# Search patient
def search_patient():
    print("\n========== PATIENT SEARCH ==========")

    keyword = input("Enter patient ID or name: ").lower()

    results = [
        p for p in data["patients"]
        if keyword in p["id"].lower()
        or keyword in p["name"].lower()
    ]

    if not results:
        print("No patient found!")
        return

    for patient in results:
        print("\nPatient ID:", patient["id"])
        print("Name:", patient["name"])
        print("Age:", patient["age"])
        print("Gender:", patient["gender"])
        print("Phone:", patient["phone"])
        print("Disease:", patient["disease"])
        print("Token:", patient["token"])


# View all patients
def view_patients():
    print("\n========== ALL PATIENTS ==========")

    if not data["patients"]:
        print("No patient records available.")
        return

    for p in data["patients"]:
        print(
            p["id"], "|",
            p["name"], "|",
            p["disease"], "|",
            "Token:", p["token"]
        )


# Medical records
def add_medical_record():
    print("\n========== MEDICAL RECORDS ==========")

    patient_id = input("Enter patient ID: ").upper()

    patient = next(
        (p for p in data["patients"] if p["id"] == patient_id),
        None
    )

    if patient is None:
        print("Patient not found!")
        return

    diagnosis = input("Enter doctor's diagnosis: ")
    treatment = input("Enter treatment details: ")
    medicines = input("Enter prescribed medicines: ")

    patient["medical_record"] = {
        "diagnosis": diagnosis,
        "treatment": treatment,
        "medicines": medicines,
        "date": datetime.now().strftime("%d-%m-%Y")
    }

    save_data()
    print("Medical record saved successfully!")


# Generate bill
def generate_bill():
    print("\n========== BILLING SYSTEM ==========")

    patient_id = input("Enter patient ID: ").upper()

    patient = next(
        (p for p in data["patients"] if p["id"] == patient_id),
        None
    )

    if patient is None:
        print("Patient not found!")
        return

    show_doctors()

    doctor_id = input("\nEnter doctor ID: ").upper()

    if doctor_id not in doctors:
        print("Invalid doctor ID!")
        return

    treatment_fee = input("Enter additional treatment fee: ")

    try:
        treatment_fee = float(treatment_fee)
        if treatment_fee < 0:
            raise ValueError
    except ValueError:
        print("Enter a valid non-negative amount!")
        return

    consultation_fee = doctors[doctor_id]["fee"]
    total = consultation_fee + treatment_fee

    bill = {
        "bill_id": "BILL" + str(len(data["bills"]) + 1001),
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "consultation_fee": consultation_fee,
        "treatment_fee": treatment_fee,
        "total": total,
        "date": datetime.now().strftime("%d-%m-%Y")
    }

    data["bills"].append(bill)
    save_data()

    print("\n========== HOSPITAL BILL ==========")
    print("Bill ID:", bill["bill_id"])
    print("Patient:", patient["name"])
    print("Consultation Fee: Rs.", consultation_fee)
    print("Treatment Fee: Rs.", treatment_fee)
    print("----------------------------------")
    print("TOTAL AMOUNT: Rs.", total)
    print("==================================")


# Emergency registration
def emergency_patient():
    print("\n========== EMERGENCY REGISTRATION ==========")

    name = input("Enter patient name: ")
    age = input("Enter age: ")
    phone = input("Enter phone number: ")
    condition = input("Enter emergency condition: ")

    if not name.strip() or not age.isdigit() or not phone.isdigit():
        print("Invalid patient details!")
        return

    patient_id = generate_patient_id()
    token = generate_token()

    patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": "Not specified",
        "phone": phone,
        "disease": condition,
        "token": token,
        "priority": "EMERGENCY",
        "date": datetime.now().strftime("%d-%m-%Y")
    }

    data["patients"].append(patient)
    save_data()

    print("\nEMERGENCY PATIENT REGISTERED!")
    print("Patient ID:", patient_id)
    print("Priority: HIGH")
    print("Emergency Token:", token)
    print("Please contact hospital emergency staff immediately.")


# Dashboard
def dashboard():
    print("\n========== HOSPITAL DASHBOARD ==========")

    total_patients = len(data["patients"])
    total_appointments = len(data["appointments"])
    total_bills = len(data["bills"])
    revenue = sum(b["total"] for b in data["bills"])

    emergency_count = sum(
        1 for p in data["patients"]
        if p.get("priority") == "EMERGENCY"
    )

    print("Total Patients:", total_patients)
    print("Total Appointments:", total_appointments)
    print("Total Bills:", total_bills)
    print("Emergency Patients:", emergency_count)
    print("Total Revenue: Rs.", revenue)


# Main menu
def main():

    while True:

        print("\n" + "=" * 48)
        print("          HOSPITAL MANAGEMENT SYSTEM")
        print("=" * 48)

        print("1.  Register New Patient")
        print("2.  View All Patients")
        print("3.  Search Patient")
        print("4.  View Available Doctors")
        print("5.  Book Appointment")
        print("6.  Add Medical Records")
        print("7.  Generate Patient Bill")
        print("8.  Emergency Patient Registration")
        print("9.  Hospital Dashboard")
        print("10. Exit")

        print("=" * 48)

        choice = input("Enter your choice: ")

        if choice == "1":
            register_patient()

        elif choice == "2":
            view_patients()

        elif choice == "3":
            search_patient()

        elif choice == "4":
            show_doctors()

        elif choice == "5":
            book_appointment()

        elif choice == "6":
            add_medical_record()

        elif choice == "7":
            generate_bill()

        elif choice == "8":
            emergency_patient()

        elif choice == "9":
            dashboard()

        elif choice == "10":
            print("\nThank you for using our Hospital Management System!")
            print("Program closed successfully.")
            break

        else:
            print("Invalid choice! Please select between 1 and 10.")


# Start application
if __name__ == "__main__":
    main()
