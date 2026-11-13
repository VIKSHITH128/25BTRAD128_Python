# Student grading automation.
# Code: 
def calculate_grade(score):
    """Return letter grade and pass/fail status based on score."""
    if score >= 90:
        return "A", "Pass"
    elif score >= 80:
        return "B", "Pass"
    elif score >= 70:
        return "C", "Pass"
    elif score >= 60:
        return "D", "Pass"
    else:
        return "F", "Fail"


def read_int(prompt, minimum=1):
    """Keep asking until the user enters a whole number >= minimum."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f" Please enter a number of at least {minimum}.")
                continue
            return value
        except ValueError:
            print(" Invalid input! Please enter a whole number.")


def read_score(prompt):
    """Keep asking until the user enters a number between 0 and 100."""
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            print(" Score must be between 0 and 100.")
        except ValueError:
            print(" Invalid input! Please enter a numeric score.")


def read_name(prompt):
    """Keep asking until the user enters a non-empty name."""
    while True:
        name = input(prompt).strip()
        if name:
            return name
        print(" Name cannot be empty.")


def main():
    print("=== Student Grading Automation System ===")
    students = []

    num_students = read_int("Enter total number of students: ")

    for i in range(1, num_students + 1):
        print(f"\nStudent {i}:")
        name = read_name(" Enter name: ")
        score = read_score(" Enter score (0-100): ")
        grade, status = calculate_grade(score)
        students.append({
            "name": name,
            "score": score,
            "grade": grade,
            "status": status,
        })

    # Display results
    print("\n" + "=" * 45)
    print(f"{'Name':<15} | {'Score':<8} | {'Grade':<6} | {'Status':<6}")
    print("=" * 45)

    total_score = 0
    for student in students:
        print(
            f"{student['name']:<15} | {student['score']:<8.2f} | "
            f"{student['grade']:<6} | {student['status']:<6}"
        )
        total_score += student["score"]

    print("-" * 45)
    class_average = total_score / len(students) if students else 0
    print(f"Class Average: {class_average:.2f}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled. Exiting.")
