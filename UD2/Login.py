from mimetypes import MimeTypes
import sys
from PySide6 import QtCore
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QStatusBar, QVBoxLayout, QLineEdit,
                               QPushButton, QLabel)
# from PySide6.QtCore import QSize, Qt
from random import randint


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin")
        self.layout_a = QVBoxLayout()
        self.widget_a = QWidget()
        self.label_admin = QLabel("Has iniciado sesion como admin")
        self.boton_cerrar = QPushButton('Cerrar Sesion')
        self.boton_cerrar.clicked.connect(self.cerrar_sesion)
        self.boton_salir = QPushButton('Salir')
        self.boton_salir.clicked.connect(self.salir)
        self.layout_a.addWidget(self.label_admin)
        self.layout_a.addWidget(self.boton_cerrar)
        self.layout_a.addWidget(self.boton_salir)
        self.setLayout(self.layout_a)

    def cerrar_sesion(self):
        self.hide()

    def salir(self):
        app.closeAllWindows()


class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User")
        self.layout_u = QVBoxLayout()
        self.widget_u = QWidget()
        self.label_user = QLabel("Has iniciado sesion como usuario")
        self.boton_cerrar = QPushButton('Cerrar Sesion')
        self.boton_cerrar.clicked.connect(self.cerrar_sesion)
        self.boton_salir = QPushButton('Salir')
        self.boton_salir.clicked.connect(self.salir)
        self.layout_u.addWidget(self.label_user)
        self.layout_u.addWidget(self.boton_cerrar)
        self.layout_u.addWidget(self.boton_salir)
        self.setLayout(self.layout_u)

    def cerrar_sesion(self):
        self.hide()
        self.main = MainWindow()
        self.main.show()

    def salir(self):
        app.closeAllWindows()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.setFixedSize(144, 120)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        
        # VENTANAS
        
        self.a = AdminWindow()
        self.u = UserWindow()

        # VENTANA LOGIN

        self.w_login = QWidget(self.widget)

        self.layoutv_login = QVBoxLayout(self.w_login)
        self.layoutv_login.setAlignment(QtCore.Qt.AlignRight)

        self.ventana_user = QLineEdit()
        self.ventana_user.setPlaceholderText("Usuario")
        self.layoutv_login.addWidget(self.ventana_user)
        self.ventana_user.setAlignment(QtCore.Qt.AlignCenter)

        self.ventana_psswd = QLineEdit()
        self.ventana_psswd.setPlaceholderText("Contraseña")
        self.layoutv_login.addWidget(self.ventana_psswd)
        self.ventana_psswd.setAlignment(QtCore.Qt.AlignCenter)

        self.boton_login = QPushButton('Login')
        self.layoutv_login.addWidget(self.boton_login)
        self.boton_login.clicked.connect(self.button_pressed)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusLabel = QLabel('Not Logged')
        self.statusBar.addPermanentWidget(self.statusLabel)


    def button_pressed(self):
        self.statusLabel.setText("Not Logged")
        if self.ventana_user.text() == "admin" and self.ventana_psswd.text() == "1234":
            self.a.show()
            self.statusLabel.setText("Logged")
        elif self.ventana_user.text() == "user" and self.ventana_psswd.text() == "1234":
            self.u.show()
            self.statusLabel.setText("Logged")
        else:
            self.statusLabel.setText("Datos incorrectos")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
