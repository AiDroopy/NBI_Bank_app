from dataclasses import dataclass
from typing import List, Any
from os import path
from itertools import count

ACCOUNT_PATH = "./accounts/"


@dataclass()
class Transaction:
    source: str
    destination: str
    amount: float
    time_Stamp: Any


class Account:
    _account_counter = count(1001, 1)

    def __init__(self):
        self.account_number: int = next(self._account_counter)
        self.balance: float = 0.0
        self.account_type: str = "debit"
        self.transactions: List[Transaction] = None

    def deposit(self, amount, source='ATM'):
        self.balance += amount
        return self.balance

    def withdraw(self, amount, destination='ATM'):
        self.balance -= amount
        return self.balance

    def show_account(self):
        print(repr(self))

    def __repr__(self):
        return f'Account("{self.account_number}","{self.account_type}",{self.balance}")'


class Customer:
    _customer_counter = count(1111, 1)

    def __init__(self, name, pnr, ids=None):
        if not ids:
            self.customer_id: str = str(next(self._customer_counter))
        else:
            self.customer_id = ids

        self.name: str = name
        self.pnr: str = pnr
        self.accounts: List[Account] = []

    def __repr__(self):
        return f'("{self.customer_id}","{self.name}",{self.pnr}")'

    def add_account(self, customer):
        """

        :type customer: Customer
        """
        new_account = Account()

        if not path.isfile(ACCOUNT_PATH + str(customer.customer_id) + ".txt"):
            print("There was no file")
            mode = 'wt'
        else:
            print("File already exists")
            mode = 'at'

        with open(ACCOUNT_PATH + str(new_account.account_number), mode) as file:
            file.writelines(str(new_account.account_number) + ":" + str(new_account.account_type) + ":" +
                            str(new_account.balance) + "\n")

        customer.accounts.append(new_account)
        print(customer.accounts)

        return new_account.account_number


class Bank:
    def __init__(self):
        self.customers = []
        self._load()

    def show_main_menu(self):
        print("Welcome to your simple and fast bank system from NBI")
        print("Select one of the following options to enter our service:")
        print()
        print("1. Add a new customer\t\t 2. View all customers")
        print("3. View a customer (pnr)  9. Quit NBI Bank app!")

        menu_val = int(input("Enter (1-4): "))

        if menu_val == 1:
            self.new_customer_menu()

        elif menu_val == 2:
            self.get_customers()

        elif menu_val == 3:
            print(menu_val)
        elif menu_val == 4:
            print(menu_val)
        else:
            print("Wrong input")
            self.show_main_menu()

    def customers_menu(self):
        print()
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

        # Create customer object of the data that exists
        for line in lines:
            line_count += 1
            cust = line.strip().split(':')
            # print(cust)
            customer = Customer(name=cust[0], pnr=cust[1], ids=cust[2])
            self.customers.append(customer)

        # If the file is empty, create at least one customer
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

    def new_customer_menu(self):
        name = input("Enter the customers name: ")
        pnr = input("Enter customers security no: ")
        ret = self.add_customer(name, pnr)

        if ret:
            print("Customer created")
            self.show_main_menu()
        else:
            print("Customer already a client of the bank")
            self.show_main_menu()

    def add_customer(self, name, pnr):
        """
        Adds a customer to the bank.txt file. Returns True on success False if not.
        :param name: <string>
        :param pnr: <string>
        :return: bool
        """

        # Create a new customer:
        new_customer = Customer(name, pnr)

        # Serialize and save the new customer
        with open('bank.txt', 'at') as file:
            file.writelines(str(new_customer.name) + ":" + new_customer.pnr + ":" + new_customer.customer_id + "\n")

        # Update the customers
        self.customers.append(new_customer)
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
            print("Delete by pnr")

        elif row:
            print("Delete by row")

        else:
            print("Nothing to delete")

    def add_account(self, pnr):
        """
        Adds a account to existing customer
        :param pnr: <String>
        :return: <int> account number if success, -1 if not.
        """

        # Find the customer object that needs to bee changed

        for cust in self.customers:
            if cust.pnr == str(pnr):
                acc_no = cust.add_account(cust)
                print(acc_no)

        return  # new_account.account_number

    def update_data_source(self):
        with open('bank2.txt', 'w', encoding='utf-8') as file:
            for elem in self.customers:
                file.write('{} {}\n'.format(elem[0], ' '.join(str(i) for i in elem[1])))

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
        self.customer_menu(customer)

    def customer_menu(self, customer):
        print(customer.pnr)
        print("1. Change customer name \t\t\t 2. Create an account")
        print("2. Delete an account \t\t\t\t 4. View transactions")
        print("9. Back to main menu")
        menu_val = int(input("Enter (1-9): "))

        if menu_val == 1:
            new_name = input("Please enter a new name: ")
            ret = self.change_customer_name(new_name, customer)

            if ret:
                print("Success", customer.pnr, new_name)
            else:
                print("Something went wrong!", customer.pnr, new_name)

        elif menu_val == 2:
            self.add_account(customer.pnr)

        elif menu_val == 3:
            pass

        elif menu_val == 4:
            pass

        elif menu_val == 9:
            self.show_main_menu()

        else:
            print("Wrong input")
            self.customer_menu(customer)
