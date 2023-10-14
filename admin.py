class Admin:
    def __init__(self, password: str) -> None:
        self.__password = password

    def authenticate(self, password):
        return self.__password == password
