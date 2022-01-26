from dataclasses import dataclass
from typing import List, Any
from os import path
import sys

ACCOUNT_PATH = "./accounts/"
FIRST_ACC_NO = 1001
DEFAULT_ACC_TYPE = "debit"
FIRST_CUST_ID = 1111


@dataclass()
class Transaction:
    source: str
    destination: str
    amount: float
    time_Stamp: Any


class Account:

    def __init__(self, balance=0.0, acc_no=None, acc_type=DEFAULT_ACC_TYPE):
        self.balance: float = balance

        self.account_number: int = acc_no

        self.account_type: str = acc_type
        self.transactions: List[Transaction] = []

    def deposit(self, amount: float) -> float:
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if self.balance < amount:
            return 0.0
        else:
            self.balance -= amount
            return self.balance

    def show_account(self):
        print(repr(self))

    def __repr__(self):
        return f'Account("{self.account_number}","{self.account_type}","{self.balance}")'


class Customer:

    def __init__(self, name: str, pnr: str, ids: int):
        self.customer_id: int = ids
        self.name: str = name
        self.pnr: str = pnr
        self.accounts: List[Account] = []
        self.check_accounts()

    def get_accounts(self):
        with open(ACCOUNT_PATH + str(self.customer_id) + ".txt", 'r') as file:
            lines = file.readlines()

            # Create account objects of the data that exists
        for line in lines:

            acc = line.strip().split(':')
            # print(acc[0], acc[1], acc[2], "HELLO") # DEBUG
            account = Account(balance=float(acc[0]), acc_no=int(acc[2]), acc_type=DEFAULT_ACC_TYPE) #FUSK
            self.accounts.append(account)
        # print(self.accounts) # DEBUG

    def check_accounts(self):
        if path.isfile(ACCOUNT_PATH + str(self.customer_id) + ".txt"):
            self.get_accounts()

    def add_account(self, customer, acc_no: int) -> int:
        """
        Adds an account and
        :param acc_no: int Account number
        :type customer: Customer
        :return: int account number
        """
        new_account = Account(acc_no=acc_no)

        # Select file mode
        if not path.isfile(ACCOUNT_PATH + str(customer.customer_id) + ".txt"):
            print("There was no file")
            mode = 'wt'
        else:
            print("File already exists")
            mode = 'at'

        with open(ACCOUNT_PATH + str(customer.customer_id) + ".txt", mode) as file:
            file.writelines(str(new_account.balance) + ":" + str(new_account.account_type) + ":" +
                            str(new_account.account_number) + "\n")

        customer.accounts.append(new_account)
        print(customer.accounts)

        return new_account.account_number

    def end_account(self, acc_no: int) -> float:
        # print("Customer.end_account", acc_no)  # DEBUG
        balance = 0.0
        for obj in self.accounts:
            # print(obj.account_number, "NEW")  # DEBUG
            if obj.account_number == acc_no:
                balance = obj.balance

        # END THE ACCOUNT HERE!!!
        return balance



    def __repr__(self):
        return f'("{self.customer_id}","{self.name}",{self.pnr}")'


class Bank:
    def __init__(self):
        self.customers = []
        self.last_account: int = FIRST_ACC_NO
        self.last_customer: int = FIRST_CUST_ID
        self._init()
        self._load()

    def _init(self):
        # Create or read a state file for saving/loading the state of the bank
        if not path.isfile("./state.txt"):
            with open('state.txt', 'w') as state_file:
                state_file.writelines(str(FIRST_ACC_NO) + "," + str(FIRST_CUST_ID))
        else:
            with open('state.txt', 'r') as state_file:
                state = state_file.readline().split(',')
            self.last_account = int(state[0])
            self.last_customer = int(state[1])

    def _load(self):
        """
        Reads in all customers from a text file to a list.
        If the file is empty the user will be forced to add
        at least one customer before the bank can be used.
        """
        customers = []

        # Check if the bank has any customers
        line_count = 0
        with open('bank.txt', 'r') as file:
            lines = file.readlines()

        # Create customer object of the data that/if exists
        for line in lines:
            line_count += 1
            cust = line.strip().split(':')

            customer = Customer(name=cust[0], pnr=cust[1], ids=cust[2])
            self.customers.append(customer)

        # If the file is empty, create at least one customer and create a state file
        if line_count < 1:
            print("This bank has no customers, please add one or more to use the bank.")

            self.new_customer_menu()
            self.show_main_menu()
        else:
            # print("\nThe bank has {} customers.\n".format(line_count))
            self.show_main_menu()

    def get_customers(self):
        """
        Get all customers that are loaded from  file
        :return: Customers
        """
        print("\n** All customers in the bank **")

        for i, customer in enumerate(self.customers):
            print(i + 1, customer.name, customer.pnr, customer.customer_id)

        self.customers_menu()

        return self.customers

    @staticmethod
    def customer_exists(pnr: str) -> bool:
        """
        Checks if the customer is already in system
        :param pnr: str security number
        :return: bool
        """
        for line in open('bank.txt').readlines():
            cust = line.strip().split(':')
            if str(cust[1]) == pnr:
                return True

        return False

    def add_customer(self, name: str, pnr: str) -> bool:
        """
        Adds a customer to the bank.txt file. Returns True on success False if not.
        :param name: str
        :param pnr: str
        :return: bool
        """
        # Check if security no is already registered in bank
        if self.customer_exists(pnr):
            print("The customer is already a client")
            return False

        else:
            # Create a new customer:
            new_customer = Customer(name, pnr, self.last_customer)
            self.last_customer = self.last_customer + 1

            # Serialize and save the new customer
            with open('bank.txt', 'at') as file:
                file.writelines(str(new_customer.name) + ":" + new_customer.pnr + ":" + str(new_customer.customer_id) +
                                "\n")

            # Update the customers
            self.customers.append(new_customer)

            # Update state file
            self.update_data_source()
            return True

    def get_customer(self, pnr):
        """
        Returns information about a specific customer
        :param pnr: <string>
        :return: List?
        """
        pass

    def change_customer_name(self, name, pnr):
        """
        Changes the customer name on a specific pnr.
        :param name: <string> new name
        :param pnr: <string> existing customer
        :return: bool
        """

        return False

    def remove_customer(self, pnr=None, row=None):
        """
        Removes a specific customer from the text file.
        :param row: <int> Removes customer by row
        :param pnr: <string> Removes customer by pnr.

        :return: list<string> all accounts removed and total funds that will be paid out.
        """
        if pnr:
            print("Delete by pnr")  # DEBUG

        elif row:
            print("Delete by row", row)  # DEBUG


        else:
            print("Nothing to delete")  # DEBUG

    def manage_customer(self, pos):
        """
        Gets the specific customer by row number
        :param pos: <int> The row number of the customer
        :return: <Customer>
        """

        customer = self.customers[pos]
        print()
        print("* Customer information *")
        print("Customer name: {} \t\t\t Customer id: {}".format(customer.name, customer.customer_id))
        print("Security number: {}".format(customer.pnr))
        print()
        print("Accounts:")

        # Load accounts
        account_file = ACCOUNT_PATH + str(customer.customer_id) + ".txt"
        if path.isfile(account_file):
            # print("THERE WAS AN ACCOUNT FILE", account_file)
            for i, line in enumerate(open(account_file).readlines()):
                acc = line.strip().split(':')
                print(str(i+1) + ". Account number:", str(acc[2]) + "\t\t" + "Balance:", str(acc[0]) + "\t" + "Type:" +
                      str(acc[1]))
        else:
            print("No accounts registered!")

        self.customer_menu(customer)

    def add_account(self, pnr: str) -> int:
        """
        Adds a account to existing customer
        :param pnr: str
        :return: int account number if success, -1 if not.
        """

        # Find the customer object that needs to bee changed
        try:
            ret = 0
            for cust in self.customers:
                if cust.pnr == str(pnr):
                    acc_no = cust.add_account(cust, self.last_account)
                    ret = self.last_account
                    self.last_account += 1
                    print(acc_no)

            self.update_data_source()
            return ret
        except:
            print("Something went wrong!")
            return -1

    def update_data_source(self):
        with open('state.txt', 'w') as state_file:
            state_file.writelines(str(self.last_account) + "," + str(self.last_customer))

    def show_main_menu(self):
        print("Welcome to your simple and fast bank system from NBI")
        print("Select one of the following options to enter our service:")
        print()
        print("Main menu:")
        print("1. Add a new customer\t\t 2. View all customers")
        print("3. View a customer(pnr)\t\t 9. Quit NBI Bank app!")

        menu_val = int(input("Enter (1-4): "))

        if menu_val == 1:
            self.new_customer_menu()
        elif menu_val == 2:
            self.get_customers()
        elif menu_val == 3:
            print(menu_val)
        elif menu_val == 4:
            print(menu_val)
        elif menu_val == 9:
            print("God bye :)")
            sys.exit(0)
        else:
            print("Wrong input")
            self.show_main_menu()

    def new_customer_menu(self):
        print()
        print("New customer menu:")
        print()

        name = input("Enter the customers name: ")
        pnr = input("Enter customers security no: ")
        ret = self.add_customer(name, pnr)

        if ret:
            print("Customer created")
            self.show_main_menu()
        else:
            print("Customer already a client of the bank")
            self.show_main_menu()

    def customers_menu(self):
        print()
        print("Customers menu:")
        print("1. Manage a customer\t\t 2. Remove a customer")
        print("3. Back to main menu")
        print()
        menu_val = int(input("Enter (1-3): "))

        if menu_val == 1:
            self.manage_customer(int(input("Enter row number: ")) - 1)
        elif menu_val == 2:
            self.remove_customer(row=int(input("Enter row number: ")) - 1)
        elif menu_val == 3:
            pass
        else:
            print("Wrong input")
            self.customers_menu()

    def customer_menu(self, customer: Customer):
        # print(customer.pnr)  # DEBUG
        print()
        print("1. Change customer name \t\t\t 2. Create an account")
        print("3. Delete an account \t\t\t\t 4. Make a withdraw")
        print("5. Make a deposit \t\t\t\t\t9. Back to main menu")
        menu_val = int(input("Enter (1-9): "))

        if menu_val == 1:
            new_name = input("Please enter a new name: ")
            ret = self.change_customer_name(new_name, customer)

            if ret:
                print("Success", customer.pnr, new_name)
            else:
                print("Something went wrong!", customer.pnr, new_name)

        elif menu_val == 2:  # Create account
            self.add_account(customer.pnr)

        elif menu_val == 3:  # Delete account
            print(customer.accounts)
            acc_no = int(input("Enter account number: "))
            balance = customer.end_account(acc_no)
            print("Total out: " + str(balance))

        elif menu_val == 4:  # Withdraw
            acc_no = int(input("Enter account number: "))
            amount = int(input("Enter amount: "))

        elif menu_val == 5:  # Deposit
            pass

        elif menu_val == 9:
            self.show_main_menu()

        else:
            print("Wrong input")
            self.customer_menu(customer)

