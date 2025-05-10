import csv
from typing import Optional
from account import Account

class AccountManager:
    """
    Handles loading, saving and searching for Account instances.
    """
    def __init__(self, filename: str):
        """
        Initializes the AccountManager
        """
        self.filename = filename
        self.accounts: list[Account] = []
        self.load_accounts()

    def load_accounts(self) -> None:
        """
        Loads account data from CSV file
        """
        try:
            with open(self.filename, mode="r", newline ="") as file:
                reader = csv.reader(file)
                next(reader)
                self.accounts = [Account.from_csv_row(row) for row in reader]
        except FileNotFoundError:
            self.accounts = []

    def save_accounts(self) -> None:
        """
        Saves all account data to the CSV file
        """
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "pin", "balance"])
            for acc in self.accounts:
                writer.writerow(acc.to_csv_row())

    def find_account(self, first_name: str, last_name: str, pin: str) -> Optional[Account]:
        """
        Searches for an account matching the first/last name, and PIN
        """
        for acc in self.accounts:
            if acc.get_full_name() == f"{first_name.title()} {last_name.title()}" and acc.validate_pin(pin):
                return acc
        return None

    def update_account(self, account: Account) -> None:
        """
        Saves current state of the account to the CSV file.
        """
        self.save_accounts()
