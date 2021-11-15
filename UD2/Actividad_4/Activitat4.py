from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import QSize
from config import *


class MainWindow(QMainWindow):
    def __init__(self, title="Title", button_text="Text", fixed=False):
        super().__init__()
        self.setWindowTitle(title)
        
        self.setWindowTitle("Ventana Estandar")
        
        self.setFixedSize(500,500)
        self.setMinimumSize(300,100)
        self.setMaximumSize(800,800)
        

        self.max_button = QPushButton('Maximizar', self)

        self.max_button.clicked.connect(self.button_max)
        
        self.max_button.resize(lado1_boton,lado2_boton)
        self.max_button.move(100, 200)
        
        
        
        self.stand_button = QPushButton('Estandar', self)

        self.stand_button.clicked.connect(self.button_stand) 
        
        self.stand_button.resize(lado1_boton,lado2_boton)
        self.stand_button.move(300, 200)
        
        
        
        self.min_button = QPushButton('Minimizar', self)

        self.min_button.clicked.connect(self.button_min) 
        
        self.min_button.resize(lado1_boton,lado2_boton)
        self.min_button.move(200, 200)
        
        self.max_button.setEnabled(True)
        self.min_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        
        
        
        

    def button_max(self):
        
        self.resize(lado1_maximizada,lado2_maximizada)
        
        self.max_button.move(150, 350)
        self.min_button.move(350, 350)
        self.stand_button.move(550, 350)
        
        self.setWindowTitle("Ventana Maximizada")
        
        print('Clic max!')
        
        self.max_button.setEnabled(False)
        self.min_button.setEnabled(True)
        self.stand_button.setEnabled(True)

    def button_min(self):
        
        self.resize(lado1_minimizada, lado2_minimizada)
        
        self.max_button.move(0, 0)
        self.min_button.move(100, 0)
        self.stand_button.move(200, 0)
        
        self.setWindowTitle("Ventana Minimizada")
    
        print('Clic min!')
        
        self.max_button.setEnabled(True)
        self.min_button.setEnabled(False)
        self.stand_button.setEnabled(True)
    
    def button_stand(self):
        
        self.resize(lado1_estandar, lado2_estandar)
        
        self.max_button.move(100, 200)
        self.min_button.move(200, 200)
        self.stand_button.move(300, 200)
        
        self.setWindowTitle("Ventana Estandar")
    
        print('Clic stand!')
        
        self.max_button.setEnabled(True)
        self.min_button.setEnabled(True)
        self.stand_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()
