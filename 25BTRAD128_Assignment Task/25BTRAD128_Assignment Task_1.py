# Task 1: Print name, department and college on separate lines
print("Name: VIKSHITH S")
print("Department: CSE-AIDE-B")
print("College: Your College Name Here")  # <-- replace with your college name
 
# Task 2: Print the pattern
print("*******")
print("*******")
print("*******")
 
# Task 3: Single print() statement
print("Python is Easy")
 
# Task 4: Number pattern

for i in range(1, 6):
    for j in range(1, i + 1):
        print(j, end="")
    print()
 
# Task 5: Using \n
print("Computer\nScience\nEngineering")
 
# Task 6: Using \t
print("Name\tAge\tCity")
 
# Task 7: Single-line comment explaining the purpose of the program
# This program prints a welcome message to the screen
print("Welcome to Python Programming!")
 
# Task 8: Multi-line comments
"""
This is a multi-line comment.
It is written using triple quotes and can span several lines.
It is used to explain larger blocks of code.
"""
print("This program uses a multi-line comment.")
 
# Task 9: Three comments and three print statements
# Comment 1: Print the first message
print("Learning Python is fun.")
# Comment 2: Print the second message
print("Comments make code easier to understand.")
# Comment 3: Print the third message
print("Practice makes perfect.")
 
# Task 10: Variable called name
name = "VIKSHITH S"
print(name)
 
# Task 11: Three variables

a = 10
b = 20
c = 30
print(a)
print(b)
print(c)
 
# Task 12: Convert string "100" to integer
text_value = "100"
int_value = int(text_value)
print("Value:", int_value)
print("Data type:", type(int_value))
 
# Task 13: Convert integer 25 to float
num = 25
float_value = float(num)
print("Value:", float_value)
print("Data type:", type(float_value))
 
# Task 14: Accept age and display it
age = int(input("Enter your age: "))
print("Your age is:", age)
 
# Task 15: Sum of two integers
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
print("Sum =", num1 + num2)
 
# Task 16: Student details using f-string
student_name = input("Enter student name: ")
student_age = int(input("Enter age: "))
cgpa = float(input("Enter CGPA: "))
print(f"My name is {student_name}. I am {student_age} years old and my CGPA is {cgpa}.")
 
# Task 17: Celsius to Fahrenheit
celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = (celsius * 9 / 5) + 32
print(f"{celsius}°C = {fahrenheit:.2f}°F")
 
# Task 18: Even or odd
number = int(input("Enter number: "))
if number % 2 == 0:
    print(f"{number} is Even")
else:
    print(f"{number} is Odd")
 
Claude finished the response
