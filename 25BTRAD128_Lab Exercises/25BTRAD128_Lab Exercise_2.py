# =====================================================================
# Lab Exercise 5: Number Guessing Game
# =====================================================================
def lab_05():
    number_to_guess = random.randint(1, 50)
    attempts = 0
    guessed_correctly = False
 
    print("Welcome to the Number Guessing Game!")
    print("I have chosen a number between 1 and 50. Try to guess it!")
 
    while not guessed_correctly:
        try:
            user_guess = int(input("Enter your guess: "))
            attempts += 1
 
            if user_guess < 1 or user_guess > 50:
                print("Please enter a number between 1 and 50.")
            elif user_guess < number_to_guess:
                print("Too low! Try again.")
            elif user_guess > number_to_guess:
                print("Too high! Try again.")
            else:
                guessed_correctly = True
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
 
 
# =====================================================================
# Lab Exercise 6: Prime Number and Factorial
# =====================================================================
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
 
 
def get_factorial(n):
    if n < 0:
        return "Undefined (factorial does not exist for negative numbers)"
    return math.factorial(n)
 
 
def lab_06():
    print("=== Prime Number and Factorial Program ===")
    try:
        number = int(input("Enter an integer: "))
        if is_prime(number):
            print(f"Prime Status : {number} is a PRIME number.")
        else:
            print(f"Prime Status : {number} is NOT a prime number.")
        fact = get_factorial(number)
        print(f"Factorial    : {number}! = {fact}")
    except ValueError:
        print("Invalid input! Please enter a valid integer.")
 
 
# =====================================================================
# Lab Exercise 7: Fibonacci Series Using Recursion
# =====================================================================
def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
 
 
def lab_07():
    print("=== Fibonacci Series Using Recursion ===")
    try:
        terms = int(input("Enter the number of terms: "))
        if terms <= 0:
            print("Please enter a positive integer greater than 0.")
        else:
            print(f"Fibonacci series up to {terms} terms:")
            series = [fibonacci_recursive(i) for i in range(terms)]
            print(", ".join(map(str, series)))
    except ValueError:
        print("Invalid input! Please enter a valid integer.")
