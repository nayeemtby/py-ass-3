from admin import Admin
from user import User
from bank import Bank


def registerUser(bank: Bank):
    email = None
    name = None
    address = None
    type = None

    while type == None:
        print('Available account types:')
        print('1. Current')
        print('2. Savings')
        type = input('Enter the number of the account type you want: ')
        if type == '1':
            type = 'current'
        elif type == '2':
            type = 'savings'
        else:
            print('Invalid account type number. Try again')
            type = None

    while email == None:
        email = input('Enter your email: ')
        if email == '':
            email = None
        elif bank.isEmailInUse(email):
            print('This email is already in use')
            email = None

    while name == None:
        name = input('Enter your name: ')
        if name == '':
            name = None

    while address == None:
        address = input('Enter your address: ')
        if address == '':
            address = None

    if bank.addUser(User(type, name, email, address)):
        print('User created successfully')
    else:
        print('Failed to create user')


class AdminPortal:
    def __init__(self, bank: Bank, admin: Admin) -> None:
        self.admin: Admin = admin
        self.bank: Bank = bank

    def serve(self):
        while True:
            print('1. Create a new user')
            print('2. Delete an user')
            print('3. List registered accounts')
            print('4. Check bank balance')
            print('5. Check total provided loan')
            print('6. Toggle loan offering')
            print('7. Sign out')
            choice = input('Enter your choice: ')
            print()
            if choice == '1':
                registerUser(self.bank)
            elif choice == '2':
                self.deleteUser()
            elif choice == '3':
                self.listUsers()
            elif choice == '4':
                self.checkBalance()
            elif choice == '5':
                self.checkLoanedAmount()
            elif choice == '6':
                self.toggleLoaning()
            elif choice == '7':
                return
            else:
                print('Invalid choice')
            print()

    def deleteUser(self):
        email = input('Enter the email of the account you want to delete: ')
        if self.bank.deleteUser(self.admin, email):
            print('Account deleted successfully')
        else:
            print('Failed to delete the account')

    def listUsers(self):
        print()
        self.bank.listUsers(self.admin)

    def checkBalance(self):
        print()
        bal = self.bank.getBalance(self.admin)
        if bal is not None:
            print(f'Bank currently has {bal}')
        else:
            print('Failed to get balance')

    def checkLoanedAmount(self):
        amount = self.bank.getLoanAmount(self.admin)
        if amount is not None:
            print(f'Bank has provided {amount} in loans')
        else:
            print(f'Failed to get loan amount')

    def toggleLoaning(self):
        enabled = self.bank.toggleLoaning(self.admin)
        if enabled is None:
            print('Failed to toggle loaning')
        else:
            if enabled:
                print('Loan offering has been enabled')
            else:
                print('Loan offering has been disabled')


class UserPortal:
    def __init__(self, bank: Bank, user: User) -> None:
        self.user: User = user
        self.bank: Bank = bank

    def serve(self):
        while True:
            print('1. Deposit')
            print('2. Transfer')
            print('3. Check Balance')
            print('4. Withdraw')
            print('5. Show transaction history')
            print('6. Take loan')
            print('7. Sign out')
            choice = input('Enter your choice: ')
            print()
            if choice == '1':
                self.deposit()
            elif choice == '2':
                self.transfer()
            elif choice == '3':
                self.checkBalance()
            elif choice == '4':
                self.withdraw()
            elif choice == '5':
                self.showTransaction()
            elif choice == '6':
                self.takeLoan()
            elif choice == '7':
                return
            else:
                print('Invalid choice')
            print()

    def deposit(self):
        amount = input('Enter amount to deposit: ')
        amount = float(amount)
        if amount > 0:
            self.bank.deposit(self.user.email, amount)
        else:
            print('Invalid amount')

    def transfer(self):
        email = input('Enter destination account email: ')
        amount = input('Enter amount to transfer: ')
        amount = float(amount)
        self.bank.transfer(self.user.email, email, amount)

    def checkBalance(self):
        print(f'Your current balance is {self.user.getBalance()}')

    def withdraw(self):
        amount = input('Enter amount to withdraw: ')
        amount = float(amount)
        if amount > 0:
            self.bank.withdraw(self.user.email, amount)
        else:
            print('Invalid amount')

    def showTransaction(self):
        self.user.showTransactionHistory()

    def takeLoan(self):
        if not self.bank.canOfferLoan():
            print(
                'The Bank is not offering loans at this time. Sorry for the inconvenience.')
            return
        amount = input('Enter amount you want for loan: ')
        amount = float(amount)
        self.bank.loan(self.user.email, amount)


def userLogin(bank: Bank):
    email = input('Enter your email: ')
    user = bank.loginUser(email)
    print()
    if user is not None:
        UserPortal(bank, user).serve()
    else:
        print('User not found')


def adminLogin(bank: Bank):
    password = input('Enter admin password: ')
    admin = bank.loginAdmin(password)
    print()
    if admin is not None:
        AdminPortal(bank, admin).serve()
    else:
        print('Wrong password')


def repl(bank: Bank):
    while True:
        print('1. User Login')
        print('2. User Register')
        print('3. Admin Login')
        print('4. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            userLogin(bank)
        elif choice == '2':
            registerUser(bank)
        elif choice == '3':
            adminLogin(bank)
        elif choice == '4':
            return
        else:
            print('Invalid choice')
        print()
