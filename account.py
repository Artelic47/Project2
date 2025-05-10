class Account:
    """
    Represents bank account with basic functionality for deposit
    withdrawal and pin validation.
    """
    def __init__(self, first_name: str, last_name: str, pin: str, balance: float):
        """
        Initializes an account instance.
        """
        self.__first_name = first_name.title()
        self.__last_name = last_name.title()
        self.__pin = pin
        self.__balance = balance

    def get_full_name(self) -> str:
        """
        Returns full name of account holder
        """
        return f"{self.__first_name} {self.__last_name}"

    def get_balance(self) -> float:
        """
        Returns current balance of the account
        """
        return self.__balance

    def validate_pin(self, pin: str) -> bool:
        """
        Validates if the pin provided matches the account's PIN
        """
        return self.__pin == pin

    def deposit(self, amount: float) -> bool:
        """
        Deposits specified amount into account.
        """
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws the specified amount from account.
        """
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def to_csv_row(self) -> list[str]:
        """
        converts account data to a CSV row format
        """
        return [self.__first_name, self.__last_name, self.__pin, f"{self.__balance:.2f}"]

    @classmethod
    def from_csv_row(cls, row: list[str]) -> 'Account':
        """
        Creates an account from a CSV row
        """
        first_name, last_name, pin, balance = row
        return cls(first_name, last_name, pin, float(balance))