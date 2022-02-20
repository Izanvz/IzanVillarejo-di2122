import csv
import matplotlib
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt, QAbstractTableModel
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QComboBox, QStatusBar, QVBoxLayout,
                               QLineEdit, QToolBar, QPushButton, QTableView,
                               QHBoxLayout, QLabel, QStackedLayout, QMessageBox)
matplotlib.use('Qt5Agg')

################################################################
#                                                              #
#       Datos sacados de github:                               #
#       https://github.com/montera34/escovid19data/            #
#                                                              #
################################################################

##############################################################################################
#                                                                                            #
#       Funciones adicionales de la tabla y el grafico sacadas de                            #
#                                                                                            #
#       https://www.pythonguis.com/tutorials/pyside6-qtableview-modelviews-numpy-pandas/     #
#                                                                                            #
#       https://www.pythonguis.com/tutorials/plotting-matplotlib/                            #
#                                                                                            #
##############################################################################################

###################################
#                                 #
#       Para loguearse:           #
#       Usuario : admin           #
#       Contraseña : 1234         #
#                                 #
###################################

# Ventana de login basico con un solo usuario/contraseña
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.setFixedSize(200, 140)

        self.main_window = MainWindow()

        self.layoutv_login = QVBoxLayout()
        self.layoutv_login.setAlignment(Qt.AlignRight)

        self.ventana_user = QLineEdit()
        self.ventana_user.setPlaceholderText("admin")
        self.layoutv_login.addWidget(self.ventana_user)
        self.ventana_user.setAlignment(Qt.AlignCenter)

        self.ventana_psswd = QLineEdit()
        self.ventana_psswd.setPlaceholderText("1234")
        self.layoutv_login.addWidget(self.ventana_psswd)
        self.ventana_psswd.setAlignment(Qt.AlignCenter)

        self.boton_login = QPushButton('Login')
        self.layoutv_login.addWidget(self.boton_login)
        self.boton_login.clicked.connect(self.button_pressed)

        self.cerrar_aplicacion = QPushButton('Salir')
        self.layoutv_login.addWidget(self.cerrar_aplicacion)
        self.cerrar_aplicacion.clicked.connect(self.salir)

        self.setLayout(self.layoutv_login)

    def salir(self):
        app.closeAllWindows()

    def button_pressed(self):
        if self.ventana_user.text() == "admin" and self.ventana_psswd.text() == "1234":
            self.hide()
            self.main_window.show()


class TableModel(QAbstractTableModel):

    # https://www.pythonguis.com/tutorials/pyside6-qtableview-modelviews-numpy-pandas/

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MplCanvas(FigureCanvasQTAgg):

    # https://www.pythonguis.com/tutorials/plotting-matplotlib/

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Estadisticas Covid")

        self.setFixedSize(900, 600)

# ################################ Widgets ####################################

        self.widget = QWidget()          # Widget central
        self.holder_grafico = QWidget()  # Widget para el cambio de stackedlayout
        self.holder_tabla = QWidget()    # Widget para el cambio de stackedlayout
        '''Uso widgets como holders de los layout porque si no al
        meter un layout en un stackedlayout no se posiciona bien'''

# ############################# Layouts #######################################

        self.layout_general = QVBoxLayout()      # Layout Central
        self.layout_labels = QHBoxLayout()       # Layout para los labels
        self.layout_botones = QHBoxLayout()      # Layout para los botones
        self.stackedlayout = QStackedLayout()    # Layout para cambiar entre grafico y tabla
        self.layout_tabla = QVBoxLayout()        # Layout para la tabla de ciudades
        self.layout_graficoinfo = QVBoxLayout()  # Layout el grafico + la info
        self.layout_pantalla = QHBoxLayout()     # Layout para el grafico

# ####################### Declaracion de algunas variables ####################

        self.pantalla_llena = False
        self.table = QTableView()
        self.grafico = MplCanvas(self, width=5, height=4, dpi=100)

# ##################### Creacion de botones / widgets #########################

        # Creamos los Comobox
        self.cb_esp = QComboBox()
        self.cb_esp.setStatusTip("Arriba ESPAÑA")
        self.cb_esp.setFixedWidth(100)
        self.cb_esp.addItems(["España"])

        self.provincias_esp = QComboBox()
        self.provincias_esp.setStatusTip("Eligindo Provincia...")
        self.provincias_esp.setFixedWidth(200)

        self.ciudades_valencia = QComboBox()
        self.ciudades_valencia.setStatusTip("Eligiendo ciudad...")
        self.ciudades_valencia.setFixedWidth(200)

        # Label de informacion
        self.label_info = QLabel(self.widget)
        self.label_info.setFixedSize(900, 100)

        # Labels para los combobox
        self.pais = QLabel("                           Pais: ", self.widget)
        self.label_info.setFixedSize(900, 20)
        self.provincia = QLabel("Provincias: ", self.widget)
        self.label_info.setFixedSize(900, 20)
        self.ciudades = QLabel("Ciudades Valencia: ", self.widget)
        self.label_info.setFixedSize(900, 20)

# ################### AddWidget / AddLayout / SetLayout #######################

        # Añadimos los botones al layout
        self.layout_botones.addWidget(self.cb_esp)
        self.layout_botones.addWidget(self.provincias_esp)
        self.layout_botones.addWidget(self.ciudades_valencia)

        # Añadimos labels de informacion al layout de labels
        self.layout_labels.addWidget(self.pais)
        self.layout_labels.addWidget(self.provincia)
        self.layout_labels.addWidget(self.ciudades)

        # Añadimos el stackedlayout
        self.layout_general.addLayout(self.stackedlayout)

        # Añadimos los layouts a los holders
        self.holder_grafico.setLayout(self.layout_graficoinfo)
        self.holder_tabla.setLayout(self.layout_tabla)

        # Añadimos los widgets holders al stackedlayout
        self.stackedlayout.addWidget(self.holder_grafico)
        self.stackedlayout.addWidget(self.holder_tabla)

        # Añadmios la tabla al layout
        self.layout_tabla.addWidget(self.table)

        # Añadmios los labels el grafico y los botones
        self.layout_graficoinfo.addLayout(self.layout_labels)
        self.layout_graficoinfo.addLayout(self.layout_botones)
        self.layout_graficoinfo.addLayout(self.layout_pantalla)
        self.layout_graficoinfo.addWidget(self.label_info)

# ################################# QActions ##################################

        self.graficoC_action = QAction("Grafico Ciudades", self)
        self.graficoC_action.triggered.connect(self.generar_grafico_ciudades)
        self.graficoC_action.setStatusTip("Generar grafico ciudades")

        self.tabla_action = QAction("Tabla Ciudades", self)
        self.tabla_action.triggered.connect(self.generar_tabla)
        self.tabla_action.setStatusTip("Generar Tabla")

        self.graficoP_action = QAction("Grafico Provincias", self)
        self.graficoP_action.triggered.connect(self.generar_grafico_provincias)
        self.graficoP_action.setStatusTip("Generar grafico provincias")
        
        self.tablaESP_action = QAction("Tabla Provincias", self)
        self.tablaESP_action.triggered.connect(self.generar_tablaESP)
        self.tablaESP_action.setStatusTip("Generar Tabla")

        cerrar_aplicacion = QAction("Cerrar Aplicacion", self)
        cerrar_aplicacion.setStatusTip("Cerrar Aplicacion")
        cerrar_aplicacion.triggered.connect(self.salir)

        logout = QAction("Cerrar Session", self)
        logout.setStatusTip("Cerrar Session")
        logout.triggered.connect(self.cerrar_sesion)
        
        info_csv = QAction("CSV Data", self)
        info_csv.setStatusTip("CSV Data")
        info_csv.triggered.connect(self.button_CSVinfo)

        info = QAction("Graficos/Tablas", self)
        info.setStatusTip("Graficos/Tablas")
        info.triggered.connect(self.button_info)

# ############################## ToolBar ######################################

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(200, 200))
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.setMovable(False)

        toolbar.addSeparator()
        toolbar.addAction(self.graficoC_action)
        toolbar.addSeparator()
        toolbar.addAction(self.tabla_action)
        toolbar.addSeparator()
        toolbar.addAction(self.graficoP_action)
        toolbar.addSeparator()
        toolbar.addAction(self.tablaESP_action)
        toolbar.addSeparator()

# ################################ Menu / StatusBar ##########################

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&App")
        file_menu.addAction(cerrar_aplicacion)
        file_menu.addAction(logout)
        info_menu = menu.addMenu("&Info")
        info_menu.addAction(info_csv)
        info_menu.addAction(info)

# ############################### Sacamos datos del CSV #######################

        # Rellenamos el combobox de las ciudades de valencia
        with open('data/municipios.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            next(csv_reader, None)
            for line in csv_reader:
                self.ciudades_valencia.addItem(line[1])

        # Rellenamos el combobox de las ciudades de valencia
        with open('data/provincias.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader, None)
            for line in csv_reader:
                self.provincias_esp.addItem(line[1])

# ############################# Widget y Layout principales ###################

        self.widget.setLayout(self.layout_general)

        self.setCentralWidget(self.widget)


# ###################################### Funciones ############################

    '''Funcion para borrar el grafico/tabla + los datos del label'''
    def limpiar_pantalla(self):

        if self.pantalla_llena == True:
            self.grafico.close()
            self.layout_pantalla.removeWidget(self.grafico)
            self.label_info.clear()
            self.pantalla_llena = False

    '''Funcion para generar el grafico de las ciudades de valencia'''
    def generar_grafico_ciudades(self):
        self.limpiar_pantalla()
        self.grafico.close()

        # Definimos variables para los datos del label
        pcr = 0
        pcr14 = 0
        muertos = 0

        data_csv = pd.read_csv('data/municipios.csv', sep=';')
        # Definimos las columnas que queremos que coja el grafico
        colums = ['Casos PCR+', 'PCR+ 14d', 'Defuncions']
        # Definimos el grafico y sus balores basicos
        self.grafico = MplCanvas(self, width=5, height=4, dpi=100)
        # Creamos el grafico comparando la columna de provincias con los
        # items del combobox y lo crea con las columnas que le definimos
        data_csv.loc[data_csv.Municipi == self.ciudades_valencia.currentText(),
                     colums].plot.bar(ax=self.grafico.axes)

        self.layout_pantalla.addWidget(self.grafico)

        with open('data/municipios.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for line in csv_reader:
                if line[1] == self.ciudades_valencia.currentText():
                    pcr = line[2]
                    pcr14 = line[4]
                    muertos = line[6]

        self.label_info.setText("|  PCR: " + pcr + "  |  "
                                + "PCR 14 DIAS: " + pcr14 + "  |  "
                                + "FALLECIDOS: " + muertos + "  |")

        self.stackedlayout.setCurrentWidget(self.holder_grafico)

        self.pantalla_llena = True

    '''Funcion para generar la tabla de las ciudades de valencia'''
    def generar_tabla(self):
        self.limpiar_pantalla()
        # Cogemos la informacion del csv
        data_csv = pd.read_csv('data/municipios.csv', sep=';', decimal=',')
        # Convertimos la informacion del csv en un DataFrame
        df = pd.DataFrame(data_csv)
        # Creamos la tabla con el DataFrame
        self.model = TableModel(df)
        # Metemos la informacion en las celdas
        self.table.setModel(self.model)

        self.layout_tabla.addWidget(self.table)
        self.pantalla_llena = True
        self.stackedlayout.setCurrentWidget(self.holder_tabla)
        
        
    def generar_tablaESP(self):
        self.limpiar_pantalla()
        # Cogemos la informacion del csv
        data_csv = pd.read_csv('data/españa.csv', sep=',', decimal='.')
        # Convertimos la informacion del csv en un DataFrame
        df = pd.DataFrame(data_csv)
        # Creamos la tabla con el DataFrame
        self.model = TableModel(df)
        # Metemos la informacion en las celdas
        self.table.setModel(self.model)

        self.layout_tabla.addWidget(self.table)
        self.pantalla_llena = True
        self.stackedlayout.setCurrentWidget(self.holder_tabla)


    '''Funcion para generar el grafico de las provincias de españa'''
    def generar_grafico_provincias(self):
        self.limpiar_pantalla()
        self.grafico.close()

        casos_totales = 0
        hosp = 0
        uci = 0
        fallecidos = 0

        data_csv = pd.read_csv('data/provincias.csv', sep=',')
        # Definimos las columnas que queremos que coja el grafico
        colums = ['num_casos_cum2', 'num_hosp_cum', 'num_uci_cum', 'num_def_cum']
        # Definimos el grafico y sus balores basicos
        self.grafico = MplCanvas(self, width=5, height=4, dpi=100)
        # Creamos el grafico comparando la columna de provincias con los
        # items del combobox y lo crea con las columnas que le definimos
        data_csv.loc[data_csv.province == self.provincias_esp.currentText(),
                     colums].plot.bar(ax=self.grafico.axes)

        self.layout_pantalla.addWidget(self.grafico)

        # Cogemos la informacion de las columnas del csv
        with open('data/provincias.csv') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            for line in csv_reader:
                if line[1] == self.provincias_esp.currentText():
                    casos_totales = line[28]
                    hosp = line[29]
                    uci = line[30]
                    fallecidos = line[31]

        # Añadimos la informacion al label
        self.label_info.setText("|  Casos totales: " + casos_totales + "  |  "
                                + "Hospitalizados: " + hosp + "  |  " +
                                "Hospitalizados(UCI): " + uci + "  |  " +
                                "FALLECIDOS: " + fallecidos + "  |")

        self.stackedlayout.setCurrentWidget(self.holder_grafico)

        self.pantalla_llena = True
    
    def button_CSVinfo(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Info CSV")
        dlg.setText("https://github.com/montera34/escovid19data/")
        button = dlg.exec_()

    def button_info(self, s):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Info CSV")
        dlg.setText("Informacion para hacer tablas : \n" +
                    "https://www.pythonguis.com/tutorials/pyside6-qtableview-modelviews-numpy-pandas/\n" +
                    "Informacion para añadir graficos a pyside con matplotlib: \n" +
                    "https://www.pythonguis.com/tutorials/plotting-matplotlib/\n")
        button = dlg.exec_()

    def cerrar_sesion(self):
        self.hide()
        self.login = LoginWindow()
        self.login.show()

    def salir(self):
        app.closeAllWindows()


if __name__ == "__main__":
    app = QApplication([])
    logWin = LoginWindow()
    logWin.show()
    app.exec()
