# =====================================================================
# Lab Exercise 8: Contact Book Using Lists and Dictionaries
# =====================================================================
class ContactBook:
    def __init__(self):
        self.contacts = []
 
    def add_contact(self, name, phone, email, category):
        contact = {"name": name, "phone": phone, "email": email, "category": category}
        self.contacts.append(contact)
        print(f"[SUCCESS] Added '{name}' ({category})")
 
    def search_contact(self, query):
        print(f"\n--- Searching for: '{query}' ---")
        found = [c for c in self.contacts
                 if query.lower() in c['name'].lower() or query in c['phone']]
        if found:
            for c in found:
                print(f"Name: {c['name']} | Phone: {c['phone']} | "
                      f"Email: {c['email']} | Category: {c['category']}")
        else:
            print("No matching contact found.")
 
    def update_contact(self, name, new_phone):
        for c in self.contacts:
            if c['name'].lower() == name.lower():
                c['phone'] = new_phone
                print(f"\n[UPDATED] Updated phone for '{name}' -> {new_phone}")
                return
        print(f"\n[NOT FOUND] Cannot update. '{name}' does not exist.")
 
    def delete_contact(self, name):
        for c in self.contacts:
            if c['name'].lower() == name.lower():
                self.contacts.remove(c)
                print(f"[DELETED] Contact '{name}' removed successfully.")
                return
        print(f"[NOT FOUND] Cannot delete. '{name}' does not exist.")
 
    def display_contacts(self):
        print("\n======================= CONTACT DIRECTORY =======================")
        print(f"{'Name':<16} | {'Phone':<12} | {'Email':<20} | {'Category':<10}")
        print("-" * 65)
        for c in self.contacts:
            print(f"{c['name']:<16} | {c['phone']:<12} | {c['email']:<20} | "
                  f"{c['category']:<10}")
        print("=================================================================")
 
 
def lab_08():
    cb = ContactBook()
    cb.add_contact("Alice Smith", "9876543210", "alice@corp.com", "Work")
    cb.add_contact("Bob Jones", "9123456789", "bob@gmail.com", "Personal")
    cb.add_contact("Charlie Brown", "9988776655", "charlie@tech.org", "Work")
    cb.display_contacts()
    cb.search_contact("Alice")
    cb.update_contact("Bob Jones", "9000000001")
    cb.delete_contact("Charlie Brown")
    cb.display_contacts()
 
    # Negative test cases
    cb.search_contact("Zed")
    cb.update_contact("Zed", "1111111111")
    cb.delete_contact("Zed")
 
 
# =====================================================================
# Lab Exercise 9: Student Grading System
# =====================================================================
def compute_grade(score):
    if score >= 90:
        return 'S', 'Outstanding'
    elif score >= 80:
        return 'A', 'Excellent'
    elif score >= 70:
        return 'B', 'Good'
    elif score >= 60:
        return 'C', 'Average'
    elif score >= 50:
        return 'D', 'Pass'
    else:
        return 'F', 'Fail'
 
 
def generate_academic_report(students_data):
    report = {}
    total = 0
    for name, marks in students_data.items():
        grade, remark = compute_grade(marks)
        report[name] = {'Marks': marks, 'Grade': grade, 'Remark': remark}
        total += marks
    avg = total / len(students_data)
 
    print("=" * 62)
    print("      DEPARTMENT OF CSE-AIDE - ACADEMIC REPORT CARD      ")
    print("=" * 62)
    print(f"{'Student Name':<18} | {'Marks':<6} | {'Grade':<6} | {'Performance':<12}")
    print("-" * 62)
    for name, data in report.items():
        print(f"{name:<18} | {data['Marks']:<6} | {data['Grade']:<6} | "
              f"{data['Remark']:<12}")
    print("-" * 62)
    print(f"Class Total Students : {len(students_data)}")
    print(f"Class Average Marks  : {avg:.2f} / 100")
    print("=" * 62)
 
 
def lab_09():
    student_records = {
        "Vikshith S": 95,
        "Ananya Rao": 84,
        "Rahul Sharma": 67,
        "Sneha Patel": 52,
        "David Miller": 42,
    }
    generate_academic_report(student_records)
 
 
# =====================================================================
# Lab Exercise 10: Frequency Counter Using Dictionaries
# =====================================================================
def word_frequency_counter(text):
    clean_words = re.findall(r'\b\w+\b', text.lower())
    freq_dict = {}
    for word in clean_words:
        freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict
 
 
def list_frequency_counter(item_list):
    freq_dict = {}
    for item in item_list:
        freq_dict[item] = freq_dict.get(item, 0) + 1
    return freq_dict
 
 
def lab_10():
    feedback = ("The Python lab was practical. The Python exercises were helpful "
                "and practical for learning.")
    survey_data = ["Satisfied", "Very Satisfied", "Satisfied", "Neutral",
                   "Very Satisfied", "Satisfied"]
 
    print("--- WORD FREQUENCY ANALYSIS ---")
    w_freq = word_frequency_counter(feedback)
    for word, count in sorted(w_freq.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"'{word}': {count} time(s)")
 
    print("\n--- SURVEY RESPONSE FREQUENCY ---")
    s_freq = list_frequency_counter(survey_data)
    for response, count in s_freq.items():
        bar = "█" * (count * 3)
        print(f"{response:<15} : {bar} ({count})")
