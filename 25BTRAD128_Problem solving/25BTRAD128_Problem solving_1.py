# Lab Exercise 3A: Simple Calculator
# A Python program implementing basic arithmetic operations (addition, subtraction, multiplication, and division) using functions.
#PYTHON CODE:
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b != 0:
        return a / b
    return "Error: Division by zero"


def format_result(result):
    """Format numbers to 2 decimals; pass error strings through unchanged."""
    if isinstance(result, (int, float)):
        return f"{result:.2f}"
    return result


def main():
    num1 = 45
    num2 = 12

    print("--- Simple Calculator ---")
    print(f"Numbers: {num1} and {num2}\n")
    print(f"Addition ({num1} + {num2}): {add(num1, num2)}")
    print(f"Subtraction ({num1} - {num2}): {subtract(num1, num2)}")
    print(f"Multiplication ({num1} * {num2}): {multiply(num1, num2)}")
    print(f"Division ({num1} / {num2}): {format_result(divide(num1, num2))}")


if __name__ == "__main__":
    main()
