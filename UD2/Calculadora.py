import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QGridLayout, QVBoxLayout,
                               QLineEdit, QPushButton)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")

        # Asignamos el widget principal
        # y el layout al que le añadiremos los componentes
        self.widget = QWidget()
        self.layout_general = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout_general)

        # Creamos la ventana donde apareceran los valores que introduzcamos
        # (Usamos la funcion serReadOnly(True)
        # para que solo se pueda leer y no modificar)
        self.ventana = QLineEdit()
        self.ventana.setReadOnly(True)
        self.layout_general.addWidget(self.ventana)

        # Creamos las variables
        # String de botones pulsados
        self.guardados = ""
        # Comprovador para el cambio de parentesis
        self.comprovar_parentesis = True
        # Lista de botones
        self.teclas = {}
        # Layout para botones
        teclas_layout = QGridLayout()

        teclas = {
                    'C': (0, 0), '()': (0, 1), '%': (0, 2), '/': (0, 3),
                    '7': (1, 0), '8': (1, 1), '9': (1, 2), 'x': (1, 3),
                    '4': (2, 0), '5': (2, 1), '6': (2, 2), '+': (2, 3),
                    '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
                    '0': (4, 0), '.': (4, 1), 'DEL': (4, 2), '=': (4, 3),
                  }

        # Creamos los botones segun la lista anterior
        for boton, posicion in teclas.items():
            self.teclas[boton] = QPushButton(boton)
            self.teclas[boton].setFixedSize(60, 30)
            teclas_layout.addWidget(self.teclas[boton],
                                    posicion[0], posicion[1])

            self.teclas[boton].clicked.connect(self.operacion)

        # Añadimos el layout
        self.layout_general.addLayout(teclas_layout)
        self.teclas['='].clicked.connect(self.resultado)

    # Funcion para actuar segun el boton de operando que se a clicado
    # Y comprovar lo que se necesite
    def operacion(self):
        if (self.sender().text() == "="):
            pass
        elif (self.sender().text() == "DEL"):
            self.actualizar_texto(self.guardados[:-1])
            self.guardados = self.guardados[:-1]
        elif (self.sender().text() == "C"):
            self.borrar_texto()
        elif (self.sender().text() == "x"):
            self.guardados += "*"
            self.actualizar_texto(self.guardados)
        elif (self.sender().text() == "()"):
            if(self.comprovar_parentesis):
                self.guardados += "("
                self.comprovar_parentesis = False
                self.actualizar_texto(self.guardados)
            elif(not self.comprovar_parentesis):
                self.guardados += ")"
                self.comprovar_parentesis = True
                self.actualizar_texto(self.guardados)
        else:
            self.guardados += self.sender().text()
            self.actualizar_texto(self.guardados)

    # Borra el Strin/Texto que se muestra en la ventana
    def borrar_texto(self):
        self.actualizar_texto("")
        self.guardados = ""

    # Calcula la operacion guardada en el String "guardados" con el metodo eval
    def resultado(self):
        self.actualizar_texto(str(eval(self.guardados)))

    # Actualiza el texto que se muestra por pantalla
    def actualizar_texto(self, text):
        self.ventana.setText(text)
        self.ventana.setFocus()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
