from datetime import datetime
from util import describeDateTime


class Transaction:
    def __init__(self, amount: float, transactionReason: str) -> None:
        self.amount = amount
        self.transactionReason = transactionReason
        self.at = datetime.now()

    def describe(self) -> str:
        type = 'Credit'
        if self.amount < 0:
            type = 'Debit'
        return f'{describeDateTime(self.at)}: {type} {abs(self.amount)} Because it was {self.transactionReason}'


class User:
    def __init__(self, type, name, email, address) -> None:
        self.id = email+':'+name
        self.type: str = type
        self.name: str = name
        self.email: str = email
        self.address: str = address
        self.loanGranted: int = 0

        self.__balance: float = 0
        self.__transactions: list[Transaction] = []

    def getBalance(self):
        return self.__balance

    def appendTransaction(self, transaction: Transaction):
        self.__transactions.append(transaction)

    def showTransactionHistory(self):
        if len(self.__transactions)==0:
            print('No transaction was made')
            return

        for tr in self.__transactions:
            print(tr.describe())

    def deposit(self, amount: float):
        self.__balance += amount
        self.appendTransaction(Transaction(amount, 'Deposited'))

    def withdraw(self, amount: float):
        if amount > self.__balance:
            print('Withdrawal Amount Exceeded')
            return
        self.__balance -= amount
        self.appendTransaction(Transaction(-amount, 'Withdrawn'))

    def loanIn(self, amount: float):
        self.__balance += amount
        self.loanGranted += 1
        self.appendTransaction(Transaction(amount, 'Loaned'))

    def transfer(self, amount: float):
        self.__balance += amount
        self.appendTransaction(Transaction(amount, 'Transfered'))
