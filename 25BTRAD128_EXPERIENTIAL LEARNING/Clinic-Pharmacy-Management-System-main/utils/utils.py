import os
from datetime import datetime

def print_header(head):
    print("#" * 50)
    print(head.center(50))
    print("#" * 50)

def get_birth_date_from_id(id) -> datetime:

    string_id = str(id)
    year      = ("19" if string_id[0] == "2" else "20") + string_id[1:3]
    month     = string_id[3:5]
    day       = string_id[5:7]

    return datetime.strptime(day + month + year , "%d%m%Y").date()

def read_int(msg):

    while True:

        try:

            return int(input(msg))
        
        except ValueError:

            print("Invalid Number Please Try Again.")

def read_int_in_range(fromNum, toNum) -> int :
    number = int(read_int(f"Please Enter Number Between {fromNum} and {toNum}: "))

    while(number < fromNum or number > toNum):
        print(f"Invalid Number Please Enter Number Between {fromNum} and {toNum}.")

        number = int(read_int(f"Please Enter Number Between {fromNum} and {toNum}: "))

    return number

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

