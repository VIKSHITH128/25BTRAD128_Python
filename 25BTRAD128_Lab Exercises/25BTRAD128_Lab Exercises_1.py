# =====================================================================
# Lab Exercise 1: Installing Python, VS Code / PyCharm, Jupyter Notebook
# =====================================================================
# Windows
#   Step 1: Download the installer from python.org/downloads using Chrome
#   Step 2: Run the installer, tick "Add python.exe to PATH", click Install Now
#   Step 3: Verify with:  python --version   (e.g. Python 3.13.x)
# VS Code
#   - Install from the official website, open a folder with:  code .
#   - Install the Python extension, enable File -> Auto Save
 
 
# =====================================================================
# Lab Exercise 2: Write and Execute a Basic Python Program
# =====================================================================
def lab_02():
    print("Hello, World!")
    print("Welcome to Python Programming.")
 
 
# =====================================================================
# Lab Exercise 3: Variables, Operators, and Input/Output
# =====================================================================
def lab_03():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
 
    next_year_age = age + 1
    double_age = age * 2
 
    print(f"\nHello, {name}!")
    print(f"You are currently {age} years old.")
    print(f"Next year, you will be {next_year_age} years old.")
    print(f"Twice your age is {double_age}.")
 
 
# =====================================================================
# Lab Exercise 4: Simple Calculator and Area Calculation
# =====================================================================
def lab_04():
    # Part A: Simple Calculator
    print("=== Simple Calculator ===")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
 
    addition = num1 + num2
    subtraction = num1 - num2
    multiplication = num1 * num2
    division = num1 / num2 if num2 != 0 else "Cannot divide by zero"
 
    print(f"Addition: {num1} + {num2} = {addition}")
    print(f"Subtraction: {num1} - {num2} = {subtraction}")
    print(f"Multiplication: {num1} * {num2} = {multiplication}")
    print(f"Division: {num1} / {num2} = {division}")
 
    # Part B: Area Calculations
    print("\n=== Area Calculations ===")
    length = float(input("Enter rectangle length: "))
    width = float(input("Enter rectangle width: "))
    area_rectangle = length * width
    print(f"Area of Rectangle: {area_rectangle:.2f}")
 
    radius = float(input("Enter circle radius: "))
    area_circle = math.pi * (radius ** 2)
    print(f"Area of Circle: {area_circle:.2f}")
