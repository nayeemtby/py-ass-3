from user import User
from admin import Admin

userNotRegistered = 'No user registered with this email'


class Bank:
    def __init__(self, admin: Admin) -> None:
        self.__users: dict[str, User] = {}
        self.__admin = admin
        self.__loanAmount: float = 0
        self.__balance: float = 0
        self.__canOfferLoan: bool = True

    def addUser(self, user: User) -> bool:
        if self.isEmailInUse(user.email):
            print('An user with the same email already exists')
            return False
        self.__users[user.email] = user
        return True

    def isEmailInUse(self, email: str) -> bool:
        return email in self.__users.keys()

    def loginUser(self, email) -> User | None:
        return self.__users.get(email)

    def loginAdmin(self, password) -> Admin | None:
        if self.__admin.authenticate(password):
            return self.__admin

    def deleteUser(self, admin: Admin, email: str) -> bool:
        if admin is self.__admin and email in self.__users.keys():
            self.__users.pop(email)
            return True
        return False

    def getLoanAmount(self, admin: Admin) -> float | None:
        if admin is self.__admin:
            return self.__loanAmount

    def getBalance(self, admin: Admin) -> float | None:
        if admin is self.__admin:
            return self.__balance

    def canOfferLoan(self) -> bool:
        return self.__canOfferLoan

    def listUsers(self, admin: Admin):
        if admin is self.__admin:
            for user in self.__users.values():
                print(f'Email: {user.email}')
                print(f'Name: {user.name}')
                print(f'Balance: {user.getBalance()}')
                print()

    def toggleLoaning(self, admin: Admin) -> bool | None:
        if admin is self.__admin:
            self.__canOfferLoan = self.__canOfferLoan == False
            return self.__canOfferLoan

    def deposit(self, email: str, amount: float):
        user = self.__users.get(email)
        if user is None:
            print(userNotRegistered)
            return
        user.deposit(amount)
        self.__balance += amount

    def withdraw(self, email: str, amount: float) -> float | None:
        user = self.__users.get(email)
        if user is None:
            print(userNotRegistered)
            return
        if amount > user.getBalance():
            print('Withdrawal amount exceeded')
            return
        if amount > self.__balance:
            print('Bank is bankrupt')
            return
        user.withdraw(amount)
        self.__balance -= amount
        return amount

    def loan(self, email: str, amount: float):
        if not self.__canOfferLoan:
            print(
                'The Bank is not offering loans at this time. Sorry for the inconvenience.')
            return
        user = self.__users.get(email)
        if user is None:
            print(userNotRegistered)
            return
        if user.loanGranted >= 2:
            print('User has exhausted their loan request quota')
            return
        if amount > self.__balance:
            print('The bank cannot provide this amount of loan at this time')
            return
        self.__balance -= amount
        self.__loanAmount += amount
        user.loanIn(amount)

    def transfer(self, email: str, toEmail: str, amount: float):
        user = self.__users.get(email)
        toUser = self.__users.get(toEmail)
        if user is None or toUser is None:
            print(userNotRegistered)
            return
        if user.getBalance() < amount:
            print('No enough funds')
            return
        user.transfer(-amount)
        toUser.transfer(amount)
