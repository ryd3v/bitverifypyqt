from hashlib import sha256

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QHBoxLayout

from bech32_utils import decode  # Make sure to have bech32_utils.py in the same directory

digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')


def check_base58(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]


def is_valid_bitcoin_address(address):
    try:
        # Validate P2PKH and P2SH addresses
        if address[0] in ['1', '3']:
            return check_base58(address)

        # Validate Bech32 addresses
        elif address[:3] == 'bc1':
            hrp, data = decode('bc', address)
            return hrp is not None and data is not None

        else:
            return False
    except Exception as e:
        return False


# Function to show popup
def show_popup(is_valid):
    msg = QMessageBox()
    if is_valid:
        msg.setWindowTitle("Valid Address")
        msg.setText("The Bitcoin address is valid.")
    else:
        msg.setWindowTitle("Invalid Address")
        msg.setText("The Bitcoin address is not valid.")

    # Update the stylesheet for buttons in QMessageBox
    msg.setStyleSheet("QPushButton { min-width: 100px; }")

    msg.exec()


is_dark_mode = True


# Function to toggle the theme
def toggle_theme():
    global is_dark_mode
    if is_dark_mode:
        app.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                height: 30px;
                background-color: #3b82f6;
            }
            QLineEdit {
                border-radius: 10px;
                height: 30px;
            }
        """)  # Light mode with custom styles
    else:
        app.setStyleSheet("""
            QWidget {
                background-color: #18181b;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #3b82f6;
                border-radius: 10px;
                height:30px;
            }
            QLineEdit {
                background-color: #505050;
                border-radius: 10px;
                height: 30px;
            }
        """)  # Dark mode with custom styles
    is_dark_mode = not is_dark_mode


app = QApplication([])

main_window = QMainWindow()
main_window.setWindowTitle("BitVerify")
main_window.setWindowIcon(QIcon('bitcoin.ico'))
main_window.resize(400, 200)

input_field = QLineEdit()
validate_btn = QPushButton("Validate")
clear_btn = QPushButton("Clear")

button_layout = QHBoxLayout()
button_layout.addWidget(validate_btn)
button_layout.addWidget(clear_btn)

validate_btn.clicked.connect(lambda: show_popup(is_valid_bitcoin_address(input_field.text())))
clear_btn.clicked.connect(lambda: input_field.clear())

toggle_theme_btn = QPushButton("Toggle Theme")
toggle_theme_btn.clicked.connect(toggle_theme)
button_layout.addWidget(toggle_theme_btn)

main_layout = QVBoxLayout()
main_layout.addWidget(input_field)
main_layout.addLayout(button_layout)

central_widget = QWidget()
central_widget.setLayout(main_layout)

main_window.setCentralWidget(central_widget)
toggle_theme()
main_window.show()

app.exec()
