# Version V1.0.3
from hashlib import sha256

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QHBoxLayout, QFileDialog

from bech32_utils import decode

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
        if address[0] in ['1', '3']:
            return check_base58(address)

        elif address[:3] == 'bc1':
            hrp, data = decode('bc', address)
            return hrp is not None and data is not None

        else:
            return False
    except Exception as e:
        return False


def show_popup(is_valid):
    msg = QMessageBox()
    if is_valid:
        msg.setWindowTitle("Valid Address")
        msg.setText("The Bitcoin address is valid.")
    else:
        msg.setWindowTitle("Invalid Address")
        msg.setText("The Bitcoin address is not valid.")

    msg.setStyleSheet("QPushButton { min-width: 100px; }")

    msg.exec()


# Function to check addresses from file
def check_file():
    file_path, _ = QFileDialog.getOpenFileName(None, "Open Text File", "", "Text Files (*.txt)")
    if not file_path:
        return

    valid_addresses = []
    with open(file_path, 'r') as f:
        for line in f:
            address = line.strip()
            if is_valid_bitcoin_address(address):
                valid_addresses.append(address)

    if valid_addresses:
        with open('valid.txt', 'w') as f:
            for address in valid_addresses:
                f.write(f"{address}\n")
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Valid addresses have been written to valid.txt.")
        msg.setStyleSheet("QPushButton { min-width: 100px; min-height: 30px; }")
        msg.exec()
    else:
        msg = QMessageBox()
        msg.setWindowTitle("No Valid Addresses")
        msg.setText("No valid Bitcoin addresses were found in the file.")
        msg.setStyleSheet("QPushButton { min-width: 100px; min-height: 30px; }")
        msg.exec()


app = QApplication([])
app.setStyle("Fusion")

main_window = QMainWindow()
main_window.setWindowTitle("BitVerify")
main_window.setWindowIcon(QIcon('icon.ico'))
main_window.resize(400, 200)

input_field = QLineEdit()

# Define button styles
button_stylesheet = """
    QPushButton {
        background-color: #3b82f6;
        color: white;
        font-size: 14px;
        border-radius: 10px;
        height: 30px;
    }
    QPushButton:hover {
        background-color: #52525b;
    }
    QPushButton:pressed {
        background-color: #2563eb;
    }
    QPushButton:disabled {
        background-color: #A0A0A0; /* Gray for disabled state */
        color: #FFFFFF;
    }
"""

# Create buttons
validate_btn = QPushButton("Validate")
clear_btn = QPushButton("Clear")
check_file_btn = QPushButton("Check File")

# Apply button styles
validate_btn.setStyleSheet(button_stylesheet)
clear_btn.setStyleSheet(button_stylesheet)
check_file_btn.setStyleSheet(button_stylesheet)

# Layout and connections
button_layout = QHBoxLayout()
button_layout.addWidget(validate_btn)
button_layout.addWidget(clear_btn)
button_layout.addWidget(check_file_btn)

validate_btn.clicked.connect(lambda: show_popup(is_valid_bitcoin_address(input_field.text())))
clear_btn.clicked.connect(lambda: input_field.clear())
check_file_btn.clicked.connect(check_file)

main_layout = QVBoxLayout()
main_layout.addWidget(input_field)
main_layout.addLayout(button_layout)

central_widget = QWidget()
central_widget.setLayout(main_layout)

main_window.setCentralWidget(central_widget)
main_window.show()

app.exec()
