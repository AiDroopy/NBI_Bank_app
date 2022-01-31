from dataclasses import dataclass
from typing import List, Any
from os import path, mkdir
import sys

DEFAULT_ROOT_DIR = "./banks/"
DEFAULT_BANK_NAME = 'bank'

FIRST_CUST_ID = 1111

FIRST_ACC_NO = 1001
DEFAULT_ACC_TYPE = "debit"
ACCOUNT_DIR = "accounts"

# GLOBALS
bank_name: str

@dataclass()
class Transaction:  # TODO FIXA OM TID FINNS
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
        if float(self.balance) > amount:
            self.balance -= amount
            return self.balance
        else:
            print("Not enough funds!!! ")
            return self.balance

    def show_account(self):
        print(repr(self))

    def __str__(self):
        return f'Account("{self.balance}","{self.account_type}","{self.account_number}")'

    def __repr__(self):
        return f'"{self.balance}","{self.account_type}","{self.account_number}"'


class Customer:

    def __init__(self, name: str, pnr: str, ids: int):
        self.customer_id: int = ids
        self.name: str = name
        self.pnr: str = pnr
        self.accounts: List[Account] = []
        global bank_name
        self.bank_name = bank_name
        self.acc_path = DEFAULT_ROOT_DIR + self.bank_name + "/" + ACCOUNT_DIR + "/"
        # print(self.bank_name)  # DEBUG
        self.check_accounts()

    def get_accounts(self):  # TODO FIXA FUSKET
        if path.isfile(self.acc_path + str(self.customer_id) + ".txt"):
            with open(self.acc_path + str(self.customer_id) + ".txt", 'r') as file:
                lines = file.readlines()

                # Create account objects of the data that exist
            for line in lines:
                acc = line.strip().split(':')
                # print(acc[0], acc[1], acc[2], "HELLO") # DEBUG
                account = Account(balance=float(acc[0]), acc_no=int(acc[2]), acc_type=DEFAULT_ACC_TYPE)  # FUSK
                self.accounts.append(account)
            # print(self.accounts) # DEBUG

    def check_accounts(self):
        if path.isfile(self.acc_path + str(self.customer_id) + ".txt"):
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
        if not path.isfile(self.acc_path + str(customer.customer_id) + ".txt"):
            mode = 'wt'
        else:
            mode = 'at'

        with open(self.acc_path + str(customer.customer_id) + ".txt", mode) as file:
            file.writelines(str(new_account.balance) + ":" + str(new_account.account_type) + ":" +
                            str(new_account.account_number) + "\n")

        customer.accounts.append(new_account)

        return new_account.account_number

    def get_account(self, acc_no: int) -> Account:
        temp = 0
        for acc in self.accounts:
            temp = int(acc.account_number)
            # print("TEMP no", temp)  # DEBUG
            if temp == acc_no:
                # print("Account number: {} found!".format(temp))  # DEBUG
                return acc

    def end_account(self, acc_no: int) -> float:  # TODO Works!

        with open(self.acc_path + str(self.customer_id) + ".txt", 'r') as r_file:
            lines = r_file.readlines()

            for line in lines:
                list_line = line.strip().split(':')
                str_line = line.strip()

                tmp_acc = int(list_line[2])
                ret_balance = float(list_line[0])

                if tmp_acc == acc_no:
                    with open(self.acc_path + str(self.customer_id) + ".txt", 'w') as w_file:
                        for lin in lines:
                            if lin.strip() != str_line:
                                w_file.write(lin)

                    return ret_balance

    def withdraw_account(self, acc_no: int, amount: float) -> float:  # TODO KOLLA PIPEN
        # print("Customer_withdraw_account", acc_no, amount)  # DEBUG
        account = self.get_account(acc_no)
        new_balance = account.withdraw(amount)
        account.balance = new_balance

        return new_balance

    def deposit_account(self, acc_no: int, amount: float) -> float:  # TODO KOLLA PIPEN
        print()
        # print("Customer deposit account", acc_no)  # DEBUG
        account = self.get_account(acc_no)

        # print("Got account: " + repr(account))  # DEBUG
        account.balance = account.deposit(amount)
        # print("Account balance: " + str(account.balance))

        return account.balance

    def __repr__(self):
        return f'("{self.customer_id}","{self.name}",{self.pnr}")'

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


class Bank:

    def __init__(self, name: str = DEFAULT_BANK_NAME):
        self.customers = []
        self.last_account: int = FIRST_ACC_NO
        self.last_customer: int = FIRST_CUST_ID
        self.name = name

        self.file_path = DEFAULT_ROOT_DIR + name + "/" + name + ".txt"
        self.acc_path = DEFAULT_ROOT_DIR + self.name + "/" + ACCOUNT_DIR + "/"
        global bank_name
        bank_name = name
        self._init()
        self._load()

    def _init(self):
        """
        Sets bank name globaly
        Checks if there is a state file or creates it.
        Creates a state file for savinging the state of the bank
        :return: None
        """
        if not path.isfile(self.file_path):
            mkdir(DEFAULT_ROOT_DIR + self.name)
            mkdir(self.acc_path)
            with open(self.file_path, 'w') as bank_file:
                bank_file.close()

        # Create or read a state file for saving/loading the state of the bank
        if not path.isfile(DEFAULT_ROOT_DIR + self.name + "./state.txt"):
            with open(DEFAULT_ROOT_DIR + self.name + '/state.txt', 'w') as state_file:
                state_file.writelines(str(FIRST_ACC_NO) + "," + str(FIRST_CUST_ID) + "," + self.name)
        else:
            with open(DEFAULT_ROOT_DIR + self.name + '/state.txt', 'r') as state_file:
                state = state_file.readline().split(',')
            self.last_account = int(state[0])
            self.last_customer = int(state[1])

    def _load(self):  # TODO ÄNDRA VILLKORSHANTERING (path.isfile ...)
        """
        Reads in all customers from a text file to a list.
        If the file is empty the user will be forced to add
        at least one customer before the bank can be used.
        """
        
        # Check if the bank has any customers
        line_count = 0

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        # Create customer object of the data that/if exists
        for line in lines:
            line_count += 1
            cust = line.strip().split(':')

            customer = Customer(name=cust[0], pnr=cust[1], ids=int(cust[2]))
            self.customers.append(customer)

        # If the file is empty, create at least one customer and create a state file
        if line_count < 1:
            print("This bank has no customers, please add one or more to use the bank.")

            self.new_customer_menu()
            self.get_customers()
            self.customers_menu()
        else:
            # print("\nThe bank has {} customers.\n".format(line_count))
            self.get_customers()
            self.customers_menu()


    def get_customers(self) -> List[Customer]:
        """
        Get all customers that are loaded from  file
        :return: Customers
        """
        print("\n** All customers in the bank **")

        for i, customer in enumerate(self.customers):
            print(i + 1, customer.name, customer.pnr, customer.customer_id)

        self.customers_menu()

        return self.customers

    def customer_exists(self, pnr: str, ) -> bool:
        """
        Checks if the customer is already in system
        :param pnr: str security number
        :return: bool
        """
        for customer in self.customers:
            if customer.pnr == pnr:
                return True
            else:
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
            with open(self.file_path, 'at') as file:
                file.writelines(str(new_customer.name) + ":" + new_customer.pnr + ":" + str(new_customer.customer_id) +
                                "\n")

            # Update the customers
            self.customers.append(new_customer)

            # Update state file
            self.update_state_source()
            return True

    def get_customer(self, pnr: str) -> Customer:
        """
        Returns a customer object from security number
        :param pnr: str Security number
        :return: Customer
        """

        temp = ''
        for cust in self.customers:
            temp = cust.pnr
            # print("TEMP cust_id", temp, pnr)  # DEBUG
            if int(temp) == int(pnr):
                # print("Customer id: {} found!".format(temp))  # DEBUG
                return cust

    def change_customer_name(self, name: str, pnr: str) -> bool:  # TODO ALLT <---
        """
        Changes the customer name on a specific pnr
        Returns true on success

        :param name: str (New name)
        :param pnr: str (Existing customer)
        :return: bool
        """

        # print("fun: change_customer_name")  # DEBUG
        customer = self.get_customer(pnr)

        # print("Old name: " + customer.name)  #  DEBUG

        customer.name = name
        # print("New name: " + customer.name)  # DEBUG
        ret = self.update_customer_source(customer.pnr)
        return ret

    def remove_customer(self, pnr: str) -> str:  # TODO FÄRDIGSTÄLL ÄNDRA RETURN TILL SPECs
        """
        Removes a specific customer from the text file

        :param pnr: <string> Removes customer by pnr
        :return: list<string> all accounts removed and total funds that will be paid out
        """

        # End all accounts
        cust = self.get_customer(pnr)

        # Create a list of account numbers to close
        acc_list = []
        for acc in cust.accounts:
            acc_list.append(int(acc.account_number))

        # Delete all accounts in acc_list
        sum_balance = 0.0
        for acc_no in acc_list:
            sum_balance += cust.end_account(acc_no)
            print("Account {} deleted".format(acc_no))

        print("All account closed!")
        print("Total out: " + str(sum_balance))

        # Update the file without the removed customer
        with open(self.file_path, 'r') as r_file:
            lines = r_file.readlines()

            for line in lines:
                list_line = line.strip().split(':')  # Get lists
                str_line = line.strip()  # Gets string versions for compare

                tmp_pnr = list_line[1]
                ret_name = list_line[0]

                if int(tmp_pnr) == int(pnr):
                    with open(self.file_path, 'w') as w_file:
                        for lin in lines:
                            if lin.strip() != str_line:
                                w_file.write(lin)

                    return acc_list, sum_balance

    def manage_customer(self, pos: int):  # TODO LÄGG TILL ARGUMENT FÖR BÄTTRE MENYHANTERING
        """
        Gets the specific customer by row number
        :param pos: <int> The row number of the customer
        """

        customer = self.customers[pos]
        print()
        print("* Customer information *")
        print("Customer name: {} \t\t\t Customer id: {}".format(customer.name, customer.customer_id))
        print("Security number: {}".format(customer.pnr))
        print()
        print("Accounts:")

        # Load accounts
        account_file = self.acc_path + str(customer.customer_id) + ".txt"
        if path.isfile(account_file):

            for i, line in enumerate(open(account_file).readlines()):

                acc = line.strip().split(':')
                # print(acc)  # DEBUG
                print(str(i + 1) + ". Account number:", str(acc[2]) + "\t\t" + "Balance:",
                      str(acc[0]) + "\t\t\t" + "Type:" +
                      str(acc[1]))

        else:
            print("No accounts registered!")

        self.customer_menu(customer)

    def add_account(self, pnr: str) -> int:  # TODO DOING Something went wrong create account
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

            self.update_state_source()
            return ret
        except:
            print("Something went wrong!!!!")
            return -1

    def update_state_source(self):
        with open(DEFAULT_ROOT_DIR + self.name + '/state.txt', 'w') as state_file:
            state_file.writelines(str(self.last_account) + "," + str(self.last_customer))

    def update_account_source(self, customer: Customer) -> bool:
        cust_no = customer.customer_id
        # Update the file with new balance
        with open(self.acc_path + str(customer.customer_id) + ".txt", 'w') as w_file:
            for acc in customer.accounts:
                print(str(acc.balance) + ":" + acc.account_type + ":" + str(acc.account_number) + "\n")
                w_file.write(str(acc.balance) + ":" + acc.account_type + ":" + str(acc.account_number) + "\n")

        # print("WRITTEN TO DISK")  # DEBUG
        return True

    def update_customer_source(self, pnr):
        # print("fun update_customer_source")  # DEBUG
        with open(self.file_path, 'w') as file:
            for customer in self.customers:
                file.writelines(str(customer.name) + ":" + customer.pnr + ":" + str(customer.customer_id) +
                                "\n")
        return True

    def main_menu(self):  # TODO SLÅ IHOP MED CUSTOMERS_MENU
        print("Welcome to your simple and fast bank system from NBI")
        print("Select one of the following options to enter our service:")
        print()
        print("Main menu:")
        print("1. View all customers")
        print("9. Quit NBI Bank app!")

        menu_val = int(input("Enter (1-4): "))

        if menu_val == 1:
            self.get_customers()
        elif menu_val == 9:
            print("God bye :)")
            sys.exit(0)
        else:
            print("Wrong input")
            self.main_menu()

    def new_customer_menu(self):
        print()
        print("New customer menu:")
        print()

        name = input("Enter the customers name: ")
        pnr = input("Enter customers security no: ")
        ret = self.add_customer(name, pnr)

        if ret:
            print("Customer created")
            self.get_customers()
            self.customers_menu()
        else:
            print("Customer already a client of the bank")
            self.main_menu()

    def customers_menu(self):
        print()
        print("Customers menu:")
        print("1. Manage a customer\t\t 2. Remove a customer")
        print("3. Add a customer")
        print()
        menu_val = int(input("Enter (1-3): "))

        if menu_val == 1:
            self.manage_customer(int(input("Enter row number: ")) - 1)
        elif menu_val == 2:
            acc_list, total_out = self.remove_customer(input("Enter Security number: "))
            print("CUSTOMER DELETED")
            print("Accounts deleted: " + str(acc_list))
            print("Total amount out: ", str(total_out))
            self.customers = []
            self._load()

            #self.get_customers()
            #self.customers_menu()
        elif menu_val == 3:
            self.new_customer_menu()
        else:
            print("Wrong input")
            self.customers_menu()

    def customer_menu(self, customer: Customer):
        # print(customer.pnr)  # DEBUG
        print()
        print("1. Change customer name \t\t\t 2. Create an account")
        print("3. Delete an account \t\t\t\t 4. Make a withdraw")
        print("5. Make a deposit \t\t\t\t\t 9. Go back")
        menu_val = int(input("Enter (1-9): "))

        if menu_val == 1:  # Change customer name
            new_name = input("Please enter a new name: ")
            ret = self.change_customer_name(new_name, customer.pnr)

            if ret:
                print("Success", customer.pnr, new_name)
                # Reload customers
                self.customers = []
                self._load()

            else:
                print("Name did not change", customer.pnr, new_name)

        elif menu_val == 2:  # Create account
            ret = self.add_account(customer.pnr)
            print("Account {} created".format(ret))
            self.customer_menu(customer)

        elif menu_val == 3:  # Delete account
            print(customer.accounts)
            acc_no = int(input("Enter account number: "))
            balance = customer.end_account(acc_no)
            print("Account closed, total out: " + str(balance))

        elif menu_val == 4:  # Withdraw
            acc_no = int(input("Enter account number: "))
            amount = float(input("Enter amount: "))
            new_balance = customer.withdraw_account(acc_no, amount)

            self.update_account_source(customer)

            self.main_menu()

        elif menu_val == 5:  # Deposit
            acc_no = int(input("Enter account number: "))
            amount = float(input("Enter amount: "))
            new_balance = customer.deposit_account(acc_no, amount)

            self.update_account_source(customer)

            self.main_menu()

        elif menu_val == 9:
            self.get_customers()
            self.customers_menu()

            # print("God bye :)")
            # sys.exit(0)

        else:
            print("Wrong input")
            self.customer_menu(customer)


if __name__ == '__main__':
    print("Usage: bank = nbi.Bank(bank_name: str) or use as what ever :)")
