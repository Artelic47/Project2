import sys
from PyQt6.QtWidgets import QApplication
from gui import ATMWindow

def main():
    app = QApplication(sys.argv)
    window = ATMWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

