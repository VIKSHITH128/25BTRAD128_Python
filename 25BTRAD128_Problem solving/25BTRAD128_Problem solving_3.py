#Problem 1: Attendance Tracker
class AttendanceTracker:
    def __init__(self):
        # Format: {'Student Name': ['P', 'A', 'P', ...]}
        self.records = {}

    def add_student(self, name):
        if name not in self.records:
            self.records[name] = []
            print(f"[ADDED] Student '{name}' registered.")
        else:
            print(f"[SKIPPED] '{name}' already exists.")

    def record_attendance(self, name, status):
        status = status.upper()
        if name not in self.records:
            print(f"[ERROR] Unknown student '{name}'.")
        elif status not in ["P", "A"]:
            print(f"[ERROR] Invalid status '{status}' (use P or A).")
        else:
            self.records[name].append(status)

    def percentage(self, name):
        log = self.records[name]
        return (log.count("P") / len(log) * 100) if log else 0.0

    def display_report(self, threshold=75.0):
        print("=" * 64)
        print("ATTENDANCE REPORT")
        print("=" * 64)
        print(f"{'Student':<16}{'Present':>8}{'Total':>7}{'Percent':>10}   Status")
        print("-" * 64)

        defaulters = []
        for name, log in self.records.items():
            pct = self.percentage(name)
            flag = "OK" if pct >= threshold else "SHORTAGE"
            if flag == "SHORTAGE":
                defaulters.append(name)
            print(f"{name:<16}{log.count('P'):>8}{len(log):>7}{pct:>9.1f}%   {flag}")

        print("-" * 64)
        if defaulters:
            print(f"Students below {threshold:.0f}%: {', '.join(defaulters)}")
        else:
            print(f"All students meet the {threshold:.0f}% requirement.")
        print("=" * 64)


if __name__ == "__main__":
    tracker = AttendanceTracker()
    for s in ["Vikshith", "Ananya", "Rahul", "Meera"]:
        tracker.add_student(s)

    data = {
        "Vikshith": "PPPPPPPPAP",
        "Ananya":   "PPPAPPPPPP",
        "Rahul":    "PAPAAPPAAP",
        "Meera":    "PPAPPAPPPP",
    }
    for name, marks in data.items():
        for m in marks:
            tracker.record_attendance(name, m)

    # Deliberate bad inputs to demonstrate error handling
    tracker.record_attendance("Ghost", "P")
    tracker.record_attendance("Rahul", "X")
    tracker.record_attendance("Rahul", "p")  # lowercase is accepted as "P"

    print()
    tracker.display_report()
