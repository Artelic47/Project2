from PyQt6.QtWidgets import QMainWindow, QMessageBox
from atm_window import Ui_ATM
from account_manager import AccountManager
from account import Account

class ATMWindow(QMainWindow):
    """
    The main GUI window for the ATM application
    """
    def __init__(self):
        """
        Initializes the ATM GUI window and connects all widgets to the actions.
        """
        super().__init__()
        self.ui = Ui_ATM()
        self.ui.setupUi(self)
        self.ui.lineEdit_3.setEchoMode(self.ui.lineEdit_3.EchoMode.Password)

        self.manager = AccountManager("accounts.csv")
        self.current_account: Account | None = None

        #Connect buttons
        self.ui.pushButton.clicked.connect(self.search_account)
        self.ui.pushButton_2.clicked.connect(self.process_transaction)
        self.ui.pushButton_2.clicked.connect(self.update_account)
        self.ui.pushButton_create.clicked.connect(self.create_account)
        self.ui.pushButton_3.clicked.connect(self.close)

    def search_account(self):
        """
        Searches for an account using the provided credentials and updates the GUI.
        """
        first = self.ui.lineEdit.text().strip()
        last = self.ui.lineEdit_2.text().strip()
        pin = self.ui.lineEdit_3.text().strip()

        if not first or not last or not pin.isdigit():
            self.ui.label_5.setText("Please enter valid name and numeric PIN.")
            self.ui.label_6.setText("")
            self.ui.label_8.setText("")
            return

        account = self.manager.find_account(first, last, pin)
        if account:
            self.current_account = account
            self.ui.label_5.setText(f"Welcome {account.get_full_name()}!")
            self.ui.label_6.setText("What would you like to do?")
            self.ui.label_8.setText(f"Your account balance is: ${account.get_balance():.2f}")
        else:
            self.ui.label_5.setText("Account not found or wrong PIN.")
            self.ui.label_6.setText("")
            self.ui.label_8.setText("")

    def process_transaction(self):
        """
        Processes either a deposit or withdrawal based on the selected radio button.
        """
        if self.current_account is None:
            self.ui.label_5.setText("Please search for an account first.")
            return
        try:
            amount = float(self.ui.lineEdit_4.text())
        except ValueError:
            self.ui.label_5.setText("Please enter a valid amount.")
            return

        if self.ui.radioButton.isChecked(): #Withdraw
            if self.current_account.withdraw(amount):
                self.ui.label_5.setText("Withdrawal successful.")
            else:
                self.ui.label_5.setText("Insufficient funds or invalid amount.")
        elif self.ui.radioButton_2.isChecked():
            if self.current_account.deposit(amount):
                self.ui.label_5.setText("Deposit successful.")
            else:
                self.ui.label_5.setText("Invalid deposit amount.")
        else:
            self.ui.label_5.setText("Please select an action.")

        self.ui.label_8.setText(f"Your account balance is: ${self.current_account.get_balance():.2f}")

    def create_account(self):
        """
        Creates a new account with the entered details and saves it to the file.
        """
        first = self.ui.lineEdit.text().strip()
        last = self.ui.lineEdit_2.text().strip()
        pin = self.ui.lineEdit_3.text().strip()
        amount_str = self.ui.lineEdit_4.text().strip()

        if not first or not last or not pin.isdigit() or len(pin) < 4:
            self.ui.label_5.setText("Enter valid name and 4+ digit PIN.")
            return

        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError
        except ValueError:
            self.ui.label_5.setText("Enter a valid non-negative initial deposit.")
            return

        #Check if account already exists
        if self.manager.find_account(first, last, pin):
            self.ui.label_5.setText("Account already exists.")
            return

        #Create and save new account
        new_account = Account(first, last, pin, amount)
        self.manager.accounts.append(new_account)
        self.manager.save_accounts()

        self.ui.label_5.setText(f"Account created for {new_account.get_full_name()}!")
        self.ui.label_6.setText("")
        self.ui.label_8.setText(f"Your account balance is: ${new_account.get_balance():.2f}")
        self.current_account = new_account

    def update_account(self):
        if self.current_account:
            self.manager.update_account(self.current_account)
            self.ui.label_5.setText("Account saved.")
        else:
            self.ui.label_5.setText("No account to update.")