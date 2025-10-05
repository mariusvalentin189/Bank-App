import PyQt6
import re
from PyQt6.QtCore import Qt
import sys
from Databases.database_manager import DatabaseManager
from Custom.custom_classes import DigitOnlyLineEdit
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget, QGridLayout, QLabel, QLineEdit


#Main app for the user
class UserApplication(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My Bank")
        self.setFixedSize(450, 600)

        self.__database_manager = DatabaseManager()

        self.__stack = QStackedWidget()

        self.__stack.setCurrentIndex(1)

        self.__main_page = MainPage(self.__database_manager, self.__open_register_window, self.__open_accounts_window)
        self.__register_Page = RegisterPage(self.__database_manager, self.__back_to_main_window)
        self.__accounts_page = UserAccountPage(self.__database_manager, self.__back_to_main_window)

        self.__stack.addWidget(self.__main_page)
        self.__stack.addWidget(self.__register_Page)
        self.__stack.addWidget(self.__accounts_page)

        layout = QVBoxLayout()
        layout.addWidget(self.__stack)
        self.setLayout(layout)

        self.__stack.setCurrentIndex(0)

    def __open_register_window(self):
        self.__stack.setCurrentIndex(1)
    
    def __open_accounts_window(self):
        self.__stack.setCurrentIndex(2)
    
    def __back_to_main_window(self):
        self.__stack.setCurrentIndex(0)

#Register Page
class RegisterPage(QWidget):
    def __init__(self, database_manager: DatabaseManager, back_function):
        super().__init__()

        self.__database_manager = database_manager
        
        self.__first_name = QLineEdit()
        self.__last_name = QLineEdit()
        self.__pin = DigitOnlyLineEdit()
        self.__pin.setMaxLength(13)
        self.__email = QLineEdit()
        self.__password = QLineEdit()
        self.__password.setEchoMode(QLineEdit.EchoMode.Password)
        self.__phone_number = DigitOnlyLineEdit()
        self.__phone_number.setMaxLength(10) #Length for romanian phone numbers

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("First Name:"), 0, 0)
        grid_layout.addWidget(self.__first_name, 0, 1)

        grid_layout.addWidget(QLabel("Last Name:"), 1, 0)
        grid_layout.addWidget(self.__last_name, 1, 1)

        grid_layout.addWidget(QLabel("Personal Identification Number:"), 2, 0)
        grid_layout.addWidget(self.__pin, 2, 1)

        grid_layout.addWidget(QLabel("Phone Number:"), 3, 0)
        grid_layout.addWidget(self.__phone_number, 3, 1)

        grid_layout.addWidget(QLabel("Email:"), 4, 0)
        grid_layout.addWidget(self.__email, 4, 1)

        grid_layout.addWidget(QLabel("Password:"), 5, 0)
        grid_layout.addWidget(self.__password, 5, 1)

        self.__status_message = QLabel()
        self.__status_message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.__register_user)

        back_button = QPushButton("Back")
        back_button.clicked.connect(back_function)

        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        bottom_layout.addWidget(self.__status_message)
        bottom_layout.addWidget(register_button)
        bottom_layout.addWidget(back_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def __register_user(self):
        user_data = [1, 
                    self.__first_name.text().strip(), 
                    self.__last_name.text().strip(), 
                    self.__pin.text().strip(), 
                    self.__phone_number.text().strip(),
                    self.__email.text().strip(),
                    self.__password.text().strip()]
        if not self.__is_data_entered():
            self.__status_message.setText("All fields are required")
        elif not self.__pin_valid():
            self.__status_message.setText("Personal Identification Number not Valid")
        elif not self.__is_valid_phone_number():
            self.__status_message.setText("Phone number not Valid")
        elif not self.__is_valid_email():
            self.__status_message.setText("Email not Valid")
        elif self.__database_manager.already_registered_user(self.__email.text().strip()):
            self.__status_message.setText("Already registered")
        else:
            self.__database_manager.insert_user_data(user_data)
            self.__status_message.setText("Registered successfuly")
            self.__empty_data()

    def __is_valid_email(self):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, self.__email.text().strip()) is not None
    
    def __is_valid_phone_number(self):
        #Romanian mobile phone number check
        pattern = r'^07\d{8}$'
        return re.match(pattern, self.__phone_number.text().strip()) is not None
    
    def __is_data_entered(self):
        return (len(self.__first_name.text().strip()) > 0 and 
        len(self.__last_name.text().strip()) > 0 and 
        len(self.__pin.text().strip()) > 0 and
        len(self.__email.text().strip()) > 0 and
        len(self.__password.text().strip()) > 0 and 
        len(self.__phone_number.text().strip()) > 0)

    def __pin_valid(self):
        return len(self.__pin.text().strip()) == 13

    def __empty_data(self):
        self.__first_name.setText("")
        self.__last_name.setText("")
        self.__pin.setText("")
        self.__phone_number.setText("")
        self.__email.setText("")
        self.__password.setText("")

#Main Page
class MainPage(QWidget):
    def __init__(self, database_manager : DatabaseManager, register_function, login_function):
        super().__init__()
        self.__database_manager = database_manager
        self.__login_function = login_function
        self.__email = QLineEdit()
        self.__password = QLineEdit()
        self.__password.setEchoMode(QLineEdit.EchoMode.Password)

        register_button = QPushButton("Register")
        register_button.clicked.connect(register_function)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.__login_user)

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Email:"), 0, 0)
        grid_layout.addWidget(self.__email, 0, 1)

        grid_layout.addWidget(QLabel("Password:"), 1, 0)
        grid_layout.addWidget(self.__password, 1, 1)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.__status_message = QLabel()
        self.__status_message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.__status_message)
        bottom_layout.addWidget(login_button)
        bottom_layout.addWidget(register_button)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def __login_user(self):
        if not self.__credentials_filled():
            self.__status_message.setText("All fields are required")
        elif not self.__is_valid_email():
            self.__status_message.setText("Email is not valid")
        else:
            login_status_id = self.__database_manager.check_user_data(self.__email.text().strip(), self.__password.text().strip())
            if login_status_id == 1:
                #User not found
                self.__status_message.setText("Email not found")
            elif login_status_id == 2:
                #Wrong password
                self.__status_message.setText("Wrong password")
            else:
                #Login user
                self.__login_function()

    def __is_valid_email(self):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, self.__email.text().strip()) is not None

    def __credentials_filled(self):
        return len(self.__email.text().strip()) > 0 and len(self.__password.text().strip()) > 0


#User accounts page
class UserAccountPage(QWidget):
    def __init__(self, database_manager : DatabaseManager, logout_function):
        super().__init__()
        self.__database_manager = database_manager

        top_layout = QVBoxLayout()

        title = QLabel("Your accounts")
        title.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(title)

        grid_layout = QGridLayout()

        bottom_layout = QVBoxLayout()
        logout_button = QPushButton("Log out")
        logout_button.clicked.connect(logout_function)
        bottom_layout.addWidget(logout_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

def open_app():
    app = QApplication(sys.argv)

    # Load and apply CSS stylesheet
    stylesheet = load_stylesheet("./Style/app_style.css")
    app.setStyleSheet(stylesheet)

    window = UserApplication()
    window.show()

    sys.exit(app.exec())

def load_stylesheet(file_path):
    with open(file_path, "r") as f:
        return f.read()
    