import sys
import random
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Genetic Algorithms Demo")
        
        #Creamos un layout principal para la ventana
        main_layout = QHBoxLayout()

        #Creamos una figura de Matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        #Creamos un widget para contener los botones
        button_widget = QWidget()
        #Creamos un layout para los botones
        controleslayout = QVBoxLayout()
        

        #Creamos los botones
        buttonCorrer = QPushButton('Correr')
        buttonPausa = QPushButton('Pausa')
        buttonStep = QPushButton('Por paso')
        labelVelocidad = QLabel("Velocidad")
        comboVelocif = QComboBox()
        comboVelocif.addItems(["Rápido", "Moderado", "Lento"])
        
        self.comboTrgetPob = QComboBox()
        labelcomedores = QLabel("Número de comedores")
        self.comboTrgetPob.addItems(["10", "25", "30", "40", "50"])
        self.comboTrgetPob.currentIndexChanged.connect(self.update_comedores)
        
        labelnacerCom = QLabel("Los comedores nacen:")
        self.nacerCom = QComboBox()
        self.nacerCom.addItems(["cerca del centro", "en un lugar aleatorio", "cerca de la esquina superior derecha", "En la ubicación del padre"])
        self.nacerCom.currentIndexChanged.connect(self.update_comedores)

        labelmutation = QLabel("% Probabilidad en mutación:")
        self.combmutation = QComboBox()
        self.combmutation.addItems(["0", "0.01", "0.05","0.1","1","2","5","10"])
        self.combmutation.currentIndexChanged.connect(self.update_comedores)

        labelcrossover = QLabel("% Probabilidad en putación:")
        self.combmcrossover = QComboBox()
        self.combmcrossover.addItems(["0", "10", "25","50","60","70","80","90","95"])

        labelplants = QLabel("Número de plantas:")
        self.combmplants = QComboBox()
        self.combmplants.addItems(["50", "100", "150","250","500"])

        labelgrowplants = QLabel("La planta crece")
        self.combmgrowplants = QComboBox()
        self.combmgrowplants.addItems(["En filas", "En grupos ", "Aleatorio","A lo largo de la parte inferior"])

        labelgrowplants = QLabel("Cuando la planta cr")
        self.combmgrowplants = QComboBox()
        self.combmgrowplants.addItems(["En filas", "En grupos ", "Aleatorio","A lo largo de la parte inferior"])


        #Agregamos los botones al layout de botones
        controleslayout.addWidget(buttonCorrer)
        controleslayout.addWidget(buttonPausa)
        controleslayout.addWidget(buttonStep)

        #controleslayout.addWidget(labelVelocidad)
        #controleslayout.addWidget(comboVelocif)
        controleslayout.addWidget(labelcomedores)
        controleslayout.addWidget(self.comboTrgetPob)
        controleslayout.addWidget(labelnacerCom)
        controleslayout.addWidget(self.nacerCom)
        #controleslayout.addWidget(labelmutation)
        #controleslayout.addWidget(self.combmutation)
        #controleslayout.addWidget(labelcrossover)
        #controleslayout.addWidget(self.combmcrossover)
        controleslayout.addWidget(labelplants)
        controleslayout.addWidget(self.combmplants)
        controleslayout.addWidget(labelgrowplants)
        controleslayout.addWidget(self.combmgrowplants)

        #Establecemos el layout de botones en el widget
        button_widget.setLayout(controleslayout)
        #Agregamos el widget de botones al layout principal
        main_layout.addWidget(button_widget)

        #Creamos un widget central que contendrá todos los elementos
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        #Establecemos el widget central en la ventana
        self.setCentralWidget(central_widget)

        #Conectamos los botones a sus funciones correspondientes
        buttonCorrer.clicked.connect(self.start)
        buttonPausa.clicked.connect(self.on_button2_clicked)
        buttonStep.clicked.connect(self.on_button3_clicked)

        #Creamos una gráfica de ejemplo en Matplotlib
        self.comedores = []
        self.nacer_com = "cerca del centro"
        self.plantas = []
        self.plot_example()

        #Inicializamos el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_comedores)

    def update_comedores(self, index):
        num_comedores = int(self.comboTrgetPob.itemText(index))
        nacer_com = self.nacerCom.currentText()
        self.comedores = self.generate_comedores(num_comedores, nacer_com)
        num_plantas = int(self.combmplants.currentText())
        grow_plants = self.combmgrowplants.currentText()
        self.plantas = self.generate_plantas(num_plantas, grow_plants)
        self.update_plot()

    def generate_comedores(self, num_comedores, nacer_com):
        comedores = []
        table_size = 40  #Tamaño de la tabla (se asume cuadrada, 40x40 en este caso)
        cell_size = 1  #Tamaño de una celda
        for i in range(num_comedores):
            if nacer_com == "cerca del centro":
                x = random.uniform(10, 25)
                y = random.uniform(10, 25)
            elif nacer_com == "en un lugar aleatorio":
                x = random.uniform(0, table_size - cell_size)
                y = random.uniform(0, table_size - cell_size)
            elif nacer_com == "cerca de la esquina superior derecha":
                x = random.uniform(table_size / 2, table_size - cell_size)
                y = random.uniform(table_size / 2, table_size - cell_size)
            elif nacer_com == "En la ubicación del padre":
                x = random.uniform(0, table_size - cell_size)
                y = random.uniform(0, table_size - cell_size)
            comedores.append((x, y))
        return comedores
    
    

    def generate_plantas(self, num_plantas, grow_plants):
        plantas = []
        table_size = 40  #Tamaño de la tabla (se asume cuadrada, 40x40 en este caso)
        cell_size = 1  #Tamaño de una celda
        for i in range(num_plantas):
            if grow_plants == "En filas":
                x = random.uniform(cell_size, table_size - cell_size)
                y = random.uniform(cell_size, table_size / 2)
            elif grow_plants == "En grupos":
                x = random.uniform(cell_size, table_size / 2)
                y = random.uniform(cell_size, table_size / 2)
            elif grow_plants == "Aleatorio":
                x = random.uniform(cell_size, table_size - cell_size)
                y = random.uniform(cell_size, table_size - cell_size)
            elif grow_plants == "A lo largo de la parte inferior":
                x = random.uniform(cell_size, table_size - cell_size)
                y = random.uniform(1, table_size / 2)
            else:
                #Si grow_plants no coincide con ninguna opción válida, se asignan valores por defecto
                x = random.uniform(cell_size, table_size - cell_size)
                y = random.uniform(cell_size, table_size - cell_size)
            plantas.append((x, y))
        return plantas

    def move_comedores(self):
        #Actualizar la posición de los comedores aquí
        #Por ejemplo, puedes modificar las coordenadas de los comedores y luego llamar a plot_example para actualizar la gráfica

        #Llamar a plot_example para refrescar la gráfica
        self.plot_example()

    def plot_example(self):
        #Limpiamos la figura
        self.figure.clear()
        #Obtenemos el eje de la figura
        ax = self.figure.add_subplot(111)

        #Definir límites máximos para los ejes x e y
        max_x = 40
        max_y = 40

        #Dibujar comedores como palitos rojos
        for x, y in self.comedores:
            ax.plot([x, x], [y, y + 1], color='red')

        #Dibujar plantas como cuadritos verdes
        for x, y in self.plantas:
            ax.add_patch(plt.Rectangle((x, y), 0.5, 0.5, color='green'))

        #Establecer los límites máximos de los ejes
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)
        #Actualizamos la gráfica en el canvas
        self.canvas.draw()

    def update_plot(self):
        
        self.plot_example()


    def start(self):
        print("Botón 1 presionado")
        #Iniciar el temporizador con un intervalo de tiempo (por ejemplo, 100 ms)
        self.timer.start(100)

    def on_button2_clicked(self):
        print("Botón 2 presionado")

    def on_button3_clicked(self):
        print("Botón 3 presionado")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
