# =====================================================================
# Lab Exercise 11: Log File Reader Program
# =====================================================================
def analyze_log_file(filename):
    keywords = {"ERROR": 0, "WARNING": 0, "INFO": 0}
 
    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' not found.")
        return
    if os.path.getsize(filename) == 0:
        print(f"[WARNING] Log file '{filename}' is empty.")
        return
 
    try:
        with open(filename, "r") as file:
            for line in file:
                upper_line = line.upper()
                for key in keywords:
                    if key in upper_line:
                        keywords[key] += 1
 
        print("\n" + "=" * 45)
        print("           LOG FILE ANALYSIS REPORT")
        print("=" * 45)
        print(f"File Name: {filename}")
        print("-" * 45)
        for key, count in keywords.items():
            print(f"  {key:<10} Count: {count}")
        print("-" * 45)
        print(f"  Total Identified Events: {sum(keywords.values())}")
        print("=" * 45)
    except Exception as e:
        print(f"[CRITICAL] Error reading file: {e}")
 
 
def lab_11():
    sample_log = "app_activity.log"
    content = """2026-03-28 08:00:12 [INFO] Application started.
2026-03-28 08:12:45 [WARNING] High memory usage (85%).
2026-03-28 08:15:30 [ERROR] Database connection failed.
2026-03-28 08:16:01 [WARNING] Retrying DB connection.
2026-03-28 08:16:15 [INFO] Database connected successfully.
2026-03-28 08:22:10 [ERROR] Disk space full.
"""
    with open(sample_log, "w") as f:
        f.write(content)
    analyze_log_file(sample_log)
 
    # Edge cases: missing and empty files
    analyze_log_file("missing.log")
    open("empty.log", "w").close()
    analyze_log_file("empty.log")
 
 
# =====================================================================
# Lab Exercise 12: Student Data Manager Using Files
# =====================================================================
FILE_NAME = "student_records.txt"
 
 
def read_all():
    """Return list of [usn, name, dept, cgpa] records from the file."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return [line.strip().split("|") for line in file if line.strip()]
 
 
def write_all(records):
    with open(FILE_NAME, "w") as file:
        for rec in records:
            file.write("|".join(rec) + "\n")
 
 
def valid_cgpa(cgpa):
    try:
        return 0.0 <= float(cgpa) <= 10.0
    except ValueError:
        return False
 
 
def add_student(usn, name, dept, cgpa):
    if not usn.strip() or not name.strip():
        print("[INVALID] USN and Name cannot be empty.")
        return
    if not valid_cgpa(cgpa):
        print(f"[INVALID] CGPA '{cgpa}' must be a number between 0 and 10.")
        return
    if any(r[0].upper() == usn.upper() for r in read_all()):
        print(f"[DUPLICATE] USN {usn} already exists.")
        return
    with open(FILE_NAME, "a") as file:
        file.write(f"{usn}|{name}|{dept}|{cgpa}\n")
    print(f"Record for {name} ({usn}) saved successfully.")
 
 
def display_all():
    records = read_all()
    if not records:
        print("No records found.")
        return
    print("\n" + "=" * 55)
    print(f"{'USN':<14} {'NAME':<18} {'DEPT':<12} {'CGPA':<6}")
    print("=" * 55)
    for usn, name, dept, cgpa in records:
        print(f"{usn:<14} {name:<18} {dept:<12} {cgpa:<6}")
    print("=" * 55)
 
 
def search_student(target_usn):
    for usn, name, dept, cgpa in read_all():
        if usn.upper() == target_usn.upper():
            print(f"\n[FOUND] USN: {usn} | Name: {name} | Dept: {dept} | CGPA: {cgpa}")
            return
    print(f"\n[NOT FOUND] No student record for USN: {target_usn}")
 
 
def update_cgpa(target_usn, new_cgpa):
    if not valid_cgpa(new_cgpa):
        print(f"[INVALID] CGPA '{new_cgpa}' must be a number between 0 and 10.")
        return
    records = read_all()
    for rec in records:
        if rec[0].upper() == target_usn.upper():
            old = rec[3]
            rec[3] = str(new_cgpa)
            write_all(records)
            print(f"[UPDATED] {rec[1]}: CGPA {old} -> {new_cgpa}")
            return
    print(f"[NOT FOUND] Cannot update. USN {target_usn} does not exist.")
 
 
def lab_12():
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)  # start from a clean file for the demo
    add_student("25BTRAD128", "VIKSHITH S", "CSE-AIDE-B", "9.25")
    add_student("25BTRAD130", "ANANYA SHARMA", "CSE-AIDE-B", "8.90")
    add_student("25BTRAD131", "ROHAN K", "CSE-AIDE-B", "12.5")    # invalid CGPA
    add_student("25BTRAD128", "VIKSHITH S", "CSE-AIDE-B", "9.25")  # duplicate
    display_all()
    search_student("25BTRAD128")
    search_student("25BTRAD999")
    update_cgpa("25BTRAD130", "9.10")
    display_all()
 
 
# =====================================================================
# Lab Exercise 13: CSV-Based Payroll Management System
# =====================================================================
def process_payroll(filename):
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found.")
        return
 
    print("\n" + "=" * 75)
    print("                    ORGANIZATION PAYROLL SUMMARY REPORT")
    print("=" * 75)
    print(f"{'ID':<8} {'Name':<15} {'Dept':<10} {'Basic':<9} {'Gross':<10} "
          f"{'Deductions':<11} {'Net Pay':<10}")
    print("-" * 75)
 
    tot_gross = tot_net = 0.0
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                basic = float(row["BasicSalary"])
                allowance = float(row["Allowances"])
            except (ValueError, KeyError):
                print(f"[SKIPPED] Invalid data for {row.get('EmpID', '?')}")
                continue
 
            gross = basic + allowance
            tax_ded = gross * 0.10   # 10% Tax
            pf_ded = basic * 0.12    # 12% PF
            tot_ded = tax_ded + pf_ded
            net = gross - tot_ded
 
            tot_gross += gross
            tot_net += net
            print(f"{row['EmpID']:<8} {row['Name']:<15} {row['Department']:<10} "
                  f"{basic:<9.0f} {gross:<10.2f} {tot_ded:<11.2f} {net:<10.2f}")
 
    print("-" * 75)
    print(f"  TOTAL GROSS PAYOUT : Rs. {tot_gross:,.2f}")
    print(f"  TOTAL NET DISBURSED: Rs. {tot_net:,.2f}")
    print("=" * 75)
 
 
def lab_13():
    sample_csv = "payroll_data.csv"
    data = [
        ["EmpID", "Name", "Department", "BasicSalary", "Allowances"],
        ["EMP001", "Vikshith S", "CSE-AIDE", "75000", "15000"],
        ["EMP002", "Rahul Verma", "ECE", "55000", "10000"],
    ]
    with open(sample_csv, "w", newline="") as f:
        csv.writer(f).writerows(data)
    process_payroll(sample_csv)
