from abc import ABCMeta, abstractmethod

class Medicine(metaclass=ABCMeta):

    __medications_quantity = 0

    def __init__(self, id, name, purpose, price, quantity, production_date, expiry_date, leaflet=None):
        self._id                         = id
        self._name                       = name
        self._purpose                    = purpose
        self._price                      = price
        self._quantity                   = quantity
        self._leaflet                    = leaflet
        self._production_date            = production_date
        self._expiry_date                = expiry_date
        Medicine.__medications_quantity += 1
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def purpose(self):
        return self._purpose
    
    @purpose.setter
    def purpose(self, purpose):
        self._purpose = purpose

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, price):
        self._price = price

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    @property
    def leaflet(self):
        return self._leaflet
    
    @leaflet.setter
    def leaflet(self, leaflet):
        self._leaflet = leaflet

    @property
    def production_date(self):
        return self._production_date
    
    @production_date.setter
    def production_date(self, production_date):
        self._production_date = production_date

    @property
    def expiry_date(self):
        return self._expiry_date
    
    @expiry_date.setter
    def expiry_date(self, expiry_date):
        self._expiry_date = expiry_date

    @classmethod
    @abstractmethod
    def full_quantity(cls):
        pass

class SolidMedicine(Medicine):

    __solid_medications_quantity = 0

    def __init__(self, id, name, purpose, price, quantity, strips, pills_per_strip, production_date, expiry_date, leaflet=None):
        super().__init__(id, name, purpose, price, quantity, production_date, expiry_date, leaflet)

        self._strips                                = strips
        self._pills_per_strip                       = pills_per_strip
        SolidMedicine.__solid_medications_quantity += 1

    @property
    def strips(self):
        return self._strips
    
    @strips.setter
    def strips(self, strips):
        self._strips = strips
    
    @property
    def pills_per_strip(self):
        return self._pills_per_strip
    
    @pills_per_strip.setter
    def pills_per_strip(self, pills_per_strip):
        self._pills_per_strip = pills_per_strip

    @classmethod
    def full_quantity(cls):
        return cls.__solid_medications_quantity
    
    @classmethod
    def remove_solid_medicine(cls, solid_medicine_id):
        from core.session import Session

        for solid_medicine in Session.solid_medicines:
            if solid_medicine.id == solid_medicine_id:
                cls.__solid_medications_quantity -= 1
                Session.solid_medicines.remove(solid_medicine)
                break

class LiquidMedicine(Medicine):

    __liquid_medications_quantity = 0
    
    def __init__(self, id, name, purpose, price, quantity,volume, unit, production_date, expiry_date, leaflet=None):
        super().__init__(id, name, purpose, price, quantity, production_date, expiry_date, leaflet)

        self._volume                                  = volume
        self._unit                                    = unit
        LiquidMedicine.__liquid_medications_quantity +=1

    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, volume):
        self._volume = volume

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @classmethod
    def full_quantity(cls):
        return cls.__liquid_medications_quantity
    
    @classmethod
    def remove_liquid_medicine(cls, liquid_medicine_id):
        from core.session import Session

        for liquid_medicines in Session.liquid_medicines:
            if liquid_medicines.id == liquid_medicine_id:
                cls.__liquid_medications_quantity -= 1
                Session.liquid_medicines.remove(liquid_medicines)
                break

class MedicalHistory:

    def __init__(self, id, patient_id, diagnosis, treatment, doctor, date, notes=None):
        self._id         = id
        self._patient_id = patient_id 
        self._diagnosis  = diagnosis
        self._treatment  = treatment
        self._doctor     = doctor
        self._date       = date
        self._notes      = notes
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        

    @property
    def patient_id(self):
        return self._patient_id
    
    @patient_id.setter
    def patient_id(self, patient_id):
        self._patient_id = patient_id

    @property
    def diagnosis(self):
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, diagnosis):
        self._diagnosis = diagnosis

    @property
    def treatment(self):
        return self._treatment

    @treatment.setter
    def treatment(self, treatment):
        self._treatment = treatment

    @property
    def doctor(self):
        return self._doctor

    @doctor.setter
    def doctor(self, doctor):
        self._doctor = doctor

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

class Person(metaclass=ABCMeta):

    def __init__(self, id, name, age, gender, phone, email, lic_no):

        self._id      = id
        self._name    = name
        self._age     = age
        self._gender  = gender
        self._phone   = phone
        self._email    = email
        self._lic_no  = lic_no

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, age):
        self._age = age

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email

    @property 
    def lic_no(self):
        return self._lic_no
    
    @lic_no.setter
    def lic_no(self, lic_no):
        self._lic_no = lic_no

    @classmethod
    @abstractmethod
    def count(cls):
        pass   

class Doctor(Person):

    __doctors_count = 0

    def __init__(self, id, name, age, gender, phone, email, lic_no, department, salary):
        super().__init__(id, name, age, gender, phone, email, lic_no)

        self._salary            = salary
        self._department        = department
        Doctor.__doctors_count += 1

    @property
    def salary(self):
        return self._salary
    
    @salary.setter
    def salary(self, salary):
        self._salary = salary

    @property
    def department(self):
        return self._department
    
    @department.setter
    def department(self, department):
        self._department = department

    @classmethod
    def count(cls):
        return cls.__doctors_count

    @classmethod
    def remove_doctor(cls, doctor_id):
        from core.session import Session

        for doctor in Session.doctors:
            if doctor.id == doctor_id:
                cls.__doctors_count -= 1
                Session.doctors.remove(doctor)
                break
 
class Patient(Person):

    __patients_count = 0

    def __init__(self, id, name, age, gender, phone, email, lic_no, blood_type):
        super().__init__(id, name, age, gender, phone, email, lic_no)

        self._blood_type                            = blood_type
        Patient.__patients_count                   += 1
        self._medical_history: list[MedicalHistory] = []

    @property
    def blood_type(self):
        return self._blood_type

    @blood_type.setter
    def blood_type(self, blood_type):
        self._blood_type = blood_type

    @property
    def medical_history(self):
        return self._medical_history

    @medical_history.setter
    def medical_history(self, medical_history: list[MedicalHistory]):
        self._medical_history = medical_history

    def add_medical_history(self, medical_history: MedicalHistory):
        self._medical_history.append(medical_history)

    def remove_medical_history(self, medical_history: MedicalHistory):
        self._medical_history.remove(medical_history)

    def clear_medical_history(self):
        self._medical_history.clear()

    @classmethod
    def count(cls):
        return cls.__patients_count
    
    @classmethod
    def remove_patient(cls, patient_id):
        from core.session import Session

        for patient in Session.patients:
            if patient.id == patient_id:
                cls.__patients_count -= 1
                Session.patients.remove(patient)
                break
