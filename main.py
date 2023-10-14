
from admin import Admin
from repl import repl
from bank import Bank


def main():
    admin = Admin('123')
    bank = Bank(admin)
    repl(bank)


main()
