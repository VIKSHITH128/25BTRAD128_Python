# =====================================================================
# Lab Exercise 14: Bank Account System Using OOP
# =====================================================================
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
 
 
class BankAccount:
    MIN_BALANCE = 0.0
 
    def __init__(self, account_holder, account_number, initial_balance=0.0):
        self.account_holder = account_holder
        self.__account_number = account_number      # private (encapsulation)
        self.__balance = float(initial_balance)      # private (encapsulation)
        self.__transactions = []
 
    # ---- read-only access to private data ----
    @property
    def account_number(self):
        return "XXXX" + str(self.__account_number)[-4:]
 
    def get_balance(self):
        return self.__balance
 
    # ---- validation ----
    @staticmethod
    def _validate_amount(amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
 
    # ---- operations ----
    def deposit(self, amount):
        try:
            self._validate_amount(amount)
        except (TypeError, ValueError) as e:
            self.__transactions.append(("DEPOSIT", amount, "FAILED"))
            print(f"[DEPOSIT FAILED] {e}")
            return False
        self.__balance += amount
        self.__transactions.append(("DEPOSIT", amount, "SUCCESS"))
        print(f"[DEPOSIT] Rs. {amount:,.2f} credited. Balance: Rs. {self.__balance:,.2f}")
        return True
 
    def withdraw(self, amount):
        try:
            self._validate_amount(amount)
            if self.__balance - amount < self.MIN_BALANCE:
                raise InsufficientFundsError(
                    f"Insufficient balance. Available: Rs. {self.__balance:,.2f}, "
                    f"requested: Rs. {amount:,.2f}")
        except (TypeError, ValueError, InsufficientFundsError) as e:
            self.__transactions.append(("WITHDRAW", amount, "FAILED"))
            print(f"[WITHDRAWAL FAILED] {e}")
            return False
        self.__balance -= amount
        self.__transactions.append(("WITHDRAW", amount, "SUCCESS"))
        print(f"[WITHDRAWAL] Rs. {amount:,.2f} debited. Balance: Rs. {self.__balance:,.2f}")
        return True
 
    def balance_enquiry(self):
        print(f"[BALANCE] {self.account_holder}: Rs. {self.__balance:,.2f}")
 
    def summary(self):
        print("=" * 50)
        print("               BANK ACCOUNT SUMMARY")
        print("=" * 50)
        print(f"Account Holder : {self.account_holder}")
        print(f"Account Number : {self.account_number}")
        print(f"Current Balance: Rs. {self.__balance:,.2f}")
        print("-" * 50)
        print(f"{'#':<4}{'Type':<12}{'Amount':>14} {'Status'}")
        for i, (kind, amt, status) in enumerate(self.__transactions, 1):
            amt_txt = f"{amt:,.2f}" if isinstance(amt, (int, float)) else str(amt)
            print(f"{i:<4}{kind:<12}{amt_txt:>14} {status}")
        print("=" * 50)
 
 
def lab_14():
    acc = BankAccount("VIKSHITH S", "1234567890", 5000)
    acc.balance_enquiry()
    acc.deposit(2500)
    acc.withdraw(1200)
 
    print("\n--- Invalid / edge-case transactions ---")
    acc.deposit(-300)       # negative amount
    acc.withdraw(0)         # zero amount
    acc.deposit("abc")      # wrong type
    acc.withdraw(50000)     # insufficient balance
 
    print("\n--- Encapsulation check ---")
    try:
        print(acc.__balance)  # direct access blocked
    except AttributeError:
        print("[BLOCKED] Cannot access __balance directly from outside the class.")
 
    print()
    acc.summary()
 
 
# =====================================================================
# Lab Exercise 15: Library Management System
# =====================================================================
class LibraryItem:
    """Base class: common attributes for anything the library lends."""
 
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self.is_available = True
        self.issued_to = None
 
    def issue(self, member):
        if not self.is_available:
            print(f"[DENIED] '{self.title}' is already issued to {self.issued_to}.")
            return False
        self.is_available = False
        self.issued_to = member
        print(f"[ISSUED] '{self.title}' issued to {member}.")
        return True
 
    def return_item(self):
        if self.is_available:
            print(f"[INVALID] '{self.title}' was not issued.")
            return False
        print(f"[RETURNED] '{self.title}' returned by {self.issued_to}.")
        self.is_available = True
        self.issued_to = None
        return True
 
    def status(self):
        return "Available" if self.is_available else f"Issued to {self.issued_to}"
 
    def details(self):
        return f"{self.item_id:<6}{'Item':<10}{self.title:<26}{self.status()}"
 
 
class Book(LibraryItem):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title)
        self.author = author
 
    def details(self):
        return f"{self.item_id:<6}{'Book':<10}{self.title:<26}{self.status()}"
 
 
class Magazine(LibraryItem):
    def __init__(self, item_id, title, issue_no):
        super().__init__(item_id, title)
        self.issue_no = issue_no
 
    def details(self):
        return f"{self.item_id:<6}{'Magazine':<10}{self.title:<26}{self.status()}"
 
 
class Library:
    def __init__(self):
        self.items = {}
 
    def add_item(self, item):
        self.items[item.item_id] = item
        print(f"[Added] {type(item).__name__} '{item.title}' added.")
 
    def issue(self, item_id, member):
        item = self.items.get(item_id)
        if item is None:
            print(f"[ERROR] No item with ID {item_id}.")
            return
        item.issue(member)
 
    def return_item(self, item_id):
        item = self.items.get(item_id)
        if item is None:
            print(f"[ERROR] No item with ID {item_id}.")
            return
        item.return_item()
 
    def show_inventory(self):
        print("\n" + "=" * 60)
        print(f"{'ID':<6}{'Type':<10}{'Title':<26}Status")
        print("=" * 60)
        for item in self.items.values():
            print(item.details())
        print("=" * 60)
 
 
def lab_15():
    lib = Library()
    lib.add_item(Book(101, "Clean Code", "Robert C. Martin"))
    lib.add_item(Book(102, "Python Crash Course", "Eric Matthes"))
    lib.add_item(Magazine(201, "Tech Today", 45))
    lib.show_inventory()
 
    print("\n--- Issue / return operations ---")
    lib.issue(101, "Vikshith")
    lib.issue(101, "Ananya")     # already issued
    lib.return_item(102)         # never issued
    lib.issue(999, "Rahul")      # unknown ID
    lib.issue(201, "Rahul")
    lib.show_inventory()
    lib.return_item(101)
    lib.show_inventory()
 
 
# =====================================================================
# Lab Exercise 16: Dice Simulator Using Random Module
# =====================================================================
class DiceSimulator:
    def __init__(self, sides=6):
        self.sides = sides
 
    def roll(self, count=1):
        """Roll `count` dice and return a list of results."""
        return [random.randint(1, self.sides) for _ in range(count)]
 
    def roll_many(self, trials, dice=1):
        return [self.roll(dice) for _ in range(trials)]
 
    def frequency(self, trials):
        """Roll a single die `trials` times and count each face."""
        counts = Counter(self.roll()[0] for _ in range(trials))
        return {face: counts.get(face, 0) for face in range(1, self.sides + 1)}
 
 
def lab_16():
    random.seed(42)  # fixed seed -> reproducible output for the report
    die = DiceSimulator()
 
    print("5 Single Die Rolls :", [die.roll()[0] for _ in range(5)])
    print("5 Pair Dice Rolls  :", die.roll_many(5, dice=2))
 
    trials = 6000
    freq = die.frequency(trials)
    print(f"\nFrequency over {trials} rolls (expected ~{trials // 6} each)")
    print("-" * 44)
    for face, count in freq.items():
        pct = count / trials * 100
        print(f"  Face {face}: {count:>5} ({pct:5.2f}%) {'#' * int(pct)}")
    print("-" * 44)
 
    # Sum distribution for two dice (board-game style)
    sums = Counter(sum(r) for r in die.roll_many(3600, dice=2))
    print("\nTwo-dice sum distribution over 3600 rolls")
    for total in range(2, 13):
        print(f"  Sum {total:>2}: {sums[total]:>4} {'#' * (sums[total] // 20)}")
 
    print("\nObservation: faces are roughly equal (uniform); sum 7 is most likely")
    print("because 6 of the 36 combinations give it (probability 1/6).")
 
 
# =====================================================================
# Menu runner
# =====================================================================
LABS = {
    2: lab_02, 3: lab_03, 4: lab_04, 5: lab_05, 6: lab_06, 7: lab_07,
    8: lab_08, 9: lab_09, 10: lab_10, 11: lab_11, 12: lab_12, 13: lab_13,
    14: lab_14, 15: lab_15, 16: lab_16,
}
 
 
def main():
    while True:
        print("\n=== Python Lab Exercises (VIKSHITH S | 25BTRAD128) ===")
        print("Enter a lab number (2-16) to run it, or 0 to exit.")
        choice = input("Lab number: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice.isdigit() and int(choice) in LABS:
            print()
            LABS[int(choice)]()
        else:
            print("Invalid choice. Lab 1 is installation steps (no code to run).")
 
 
if __name__ == "__main__":
    main()
 
Claude finished the response
