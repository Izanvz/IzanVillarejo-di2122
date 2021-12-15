import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QGridLayout, QVBoxLayout, QStackedLayout,
                               QLineEdit, QPushButton)
# from PySide6.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")

        # Asignamos el widget para la calculadora estandar
        # y el layout al que le añadiremos los componentes
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        # self.layout_general = QVBoxLayout(self.widget)
        # self.widget.setLayout(self.layout_general)

        # Creamos un staquedlayout para guardar el layout de
        # los dos modos de calculadora
        self.stackedLayout = QStackedLayout(self.widget)

        # Creamos un widget y un layout para el modo estandar
        self.Estandar = QWidget()
        self.layout_estandar = QVBoxLayout(self.Estandar)
        self.Estandar.setLayout(self.layout_estandar)

        # Creamos un widget y un layout para el modo cientifico
        self.Cientifica = QWidget()
        self.layout_cientifica = QVBoxLayout(self.Cientifica)
        self.Cientifica.setLayout(self.layout_cientifica)

        # Añadimos los widgets al stackedlayout
        self.stackedLayout.addWidget(self.Estandar)
        self.stackedLayout.addWidget(self.Cientifica)

        # Creamos los botones para los menus widget
        button_cientifica = QAction("Cientifica", self)
        button_cientifica.triggered.connect(self.modo_cientifica)

        button_estandar = QAction("Estandar", self)
        button_estandar.triggered.connect(self.modo_estandar)

        button_guardado = QAction("&Activar Guardado", self)
        button_guardado.setCheckable(True)
        button_guardado.triggered.connect(self.Guardado)

        button_salir = QAction("Salir", self)
        button_salir.triggered.connect(self.salir)

        # Creamos el menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&Opciones")

        # Añadimos un submenu y las opciones
        file_submenu = file_menu.addMenu("Modos")
        file_submenu.addAction(button_cientifica)
        file_submenu.addAction(button_estandar)
        file_menu.addAction(button_guardado)
        file_menu.addAction(button_salir)

        # Creamos las variables
        # String de botones pulsados
        self.guardados = ""
        self.result = ""
        self.total = ""
        # Comprovador para el cambio de parentesis
        self.comprovar_parentesis = True

        # ##########################-ESTANDAR-#################################

        # Creamos la ventana estandar para los valores que introduzcamos
        # Usamos la funcion serReadOnly(True)
        # para que solo se pueda leer y no modificar
        self.ventana_estandar = QLineEdit()
        self.ventana_estandar.setReadOnly(True)
        self.layout_estandar.addWidget(self.ventana_estandar)

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
            self.teclas[boton].setShortcut(boton)
            teclas_layout.addWidget(self.teclas[boton],
                                    posicion[0], posicion[1])

            self.teclas[boton].clicked.connect(self.operacion)

        # Añadimos el layout
        self.layout_estandar.addLayout(teclas_layout)
        self.teclas['='].clicked.connect(self.resultado)

        # ##########################-CIENTIFICA-################################

        # Creamos la ventana cientifica para los valores que introduzcamos
        # Usamos la funcion serReadOnly(True)
        # para que solo se pueda leer y no modificar
        self.ventana_cientifica = QLineEdit()
        self.ventana_cientifica.setReadOnly(True)
        self.layout_cientifica.addWidget(self.ventana_cientifica)

        # Lista de botones
        self.teclas_c = {}
        # Layout para botones
        teclas_layout_c = QGridLayout()

        teclas_cientifica = {
            'exp': (0, 0), 'C': (0, 1), '()': (0, 2), '%': (0, 3), '/': (0, 4),
            'mod': (1, 0), '7': (1, 1), '8': (1, 2), '9': (1, 3), 'x': (1, 4),
            '|x|': (2, 0), '4': (2, 1), '5': (2, 2), '6': (2, 3), '+': (2, 4),
            ' e ': (3, 0), '1': (3, 1), '2': (3, 2), '3': (3, 3), '-': (3, 4),
            'log': (4, 0), '0': (4, 1), '.': (4, 2), 'DEL': (4, 3), '=': (4, 4)
        }

        # Creamos los botones segun la lista anterior
        for boton_c, posicion_c in teclas_cientifica.items():
            self.teclas_c[boton_c] = QPushButton(boton_c)
            self.teclas_c[boton_c].setFixedSize(60, 30)
            self.teclas_c[boton_c].setShortcut(boton_c)
            teclas_layout_c.addWidget(self.teclas_c[boton_c],
                                      posicion_c[0], posicion_c[1])

            self.teclas_c[boton_c].clicked.connect(self.operacion)

        # Añadimos el layout
        # self.layout_general.addLayout(teclas_layout_c)
        self.layout_cientifica.addLayout(teclas_layout_c)
        self.teclas_c['='].clicked.connect(self.resultado)

        # #######################################################################

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

    # Borra el String/Texto que se muestra en la ventana
    def borrar_texto(self):
        self.actualizar_texto("")
        self.guardados = ""

    # Calcula la operacion guardada en el String "guardados" con el metodo eval
    def resultado(self):
        self.result = str(eval(self.guardados))
        self.actualizar_texto(str(eval(self.guardados)))

    # Actualiza el texto que se muestra por pantalla
    def actualizar_texto(self, text):
        self.ventana_estandar.setText(text)
        self.ventana_cientifica.setText(text)

    # Salir/Cerrar la aplicación
    def salir(self):
        exit()

    # Guardar las operaciones en un fichero
    def Guardado(self):
        print("Guardado Activado")
        # with open('Historial.txt', 'a+') as f:
        #    self.total = self.guardados + " = " + self.result
        #    f.write(self.total)
        #    f.write('\n')

    # Cambiar a la calculadora estandar
    def modo_estandar(self):
        self.stackedLayout.setCurrentWidget(self.Estandar)
        print("Estandar")

    # Cambiar a la calculadora cientifica
    def modo_cientifica(self):
        self.stackedLayout.setCurrentWidget(self.Cientifica)
        print("Cientifica")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
