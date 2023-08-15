import sys
import random
import math
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
        self.setGeometry(100, 100, 1000, 750)  # Establece la posición y el tamaño de la ventana
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
        buttonMundo = QPushButton('Generar mundo')

        
        labelVelocidad = QLabel("Velocidad")
        comboVelocif = QComboBox()
        comboVelocif.addItems(["Rápido", "Moderado", "Lento"])
        
        self.comboTrgetPob = QComboBox()
        labelcomedores = QLabel("Número de comedores")
        self.comboTrgetPob.addItems(["10", "25", "30", "40", "50"])
        #self.comboTrgetPob.currentIndexChanged.connect(self.generarMundo)
        
        labelnacerCom = QLabel("Los comedores nacen:")
        self.nacerCom = QComboBox()
        self.nacerCom.addItems(["cerca del centro", "en un lugar aleatorio", "cerca de la esquina superior derecha", "En la ubicación del padre"])
        #self.nacerCom.currentIndexChanged.connect(self.generarMundo)

        labelmutation = QLabel("% Probabilidad en mutación:")
        self.combmutation = QComboBox()
        self.combmutation.addItems(["0", "0.01", "0.05","0.1","1","2","5","10"])
        #self.combmutation.currentIndexChanged.connect(self.generarMundo)

        labelcrossover = QLabel("% Probabilidad en putación:")
        self.combmcrossover = QComboBox()
        self.combmcrossover.addItems(["0", "10", "25","50","60","70","80","90","95"])

        labelplants = QLabel("Número de plantas:")
        self.combmplants = QComboBox()
        self.combmplants.addItems(["50", "100", "150","250","500"])

        labelgrowplants = QLabel("La planta crece")
        self.combmgrowplants = QComboBox()
        self.combmgrowplants.addItems(["En filas", "En grupos ", "Aleatorio","A lo largo de la parte inferior"])

        labelgrowbackplants = QLabel("Cuando la planta es comida")
        self.combmgrowbackplants = QComboBox()
        self.combmgrowbackplants.addItems(["Crece en un lugar aleatorio", "Crece cerca ", "No regresa"])


        #Agregamos los botones al layout de botones
        controleslayout.addWidget(buttonCorrer)
        controleslayout.addWidget(buttonPausa)
        controleslayout.addWidget(buttonStep)
        controleslayout.addWidget(buttonMundo)

        controleslayout.addWidget(labelVelocidad)
        controleslayout.addWidget(comboVelocif)
        controleslayout.addWidget(labelcomedores)
        controleslayout.addWidget(self.comboTrgetPob)
        controleslayout.addWidget(labelnacerCom)
        controleslayout.addWidget(self.nacerCom)
        controleslayout.addWidget(labelmutation)
        controleslayout.addWidget(self.combmutation)
        controleslayout.addWidget(labelcrossover)
        controleslayout.addWidget(self.combmcrossover)
        controleslayout.addWidget(labelplants)
        controleslayout.addWidget(self.combmplants)
        controleslayout.addWidget(labelgrowplants)
        controleslayout.addWidget(self.combmgrowplants)
        controleslayout.addWidget(labelgrowbackplants)
        controleslayout.addWidget(self.combmgrowbackplants)

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
        buttonMundo.clicked.connect(self.generarMundo)
        buttonPausa.clicked.connect(self.pausar_moviemitno)
        buttonStep.clicked.connect(self.movimientopaso_x_paso)

        #Creamos una gráfica de ejemplo en Matplotlib
        self.comedores = []
        self.nacer_com = "cerca del centro"
        self.plantas = []
        self.plot_example()

        #Inicializamos el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_comedores)

    def update_comedores(self):
        num_comedores_index = self.comboTrgetPob.currentIndex()
        num_comedores = int(self.comboTrgetPob.itemText(num_comedores_index))
        
        nacer_com_index = self.nacerCom.currentIndex()
        nacer_com = self.nacerCom.itemText(nacer_com_index)

        
        self.comedores = self.generate_comedores(num_comedores, nacer_com)
        
        num_plantas_index = self.combmplants.currentIndex()
        num_plantas = int(self.combmplants.itemText(num_plantas_index))
        
        grow_plants_index = self.combmgrowplants.currentIndex()
        grow_plants = self.combmgrowplants.itemText(grow_plants_index)
        
        self.plantas = self.generate_plantas(num_plantas, grow_plants)
        
        self.update_plot()
    
    def distancia_euclidiana(self,p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    def calcular_proximidad_minima(self,comedor, plantas):
        distancias = [self.distancia_euclidiana(comedor, planta) for planta in plantas]
        return min(distancias)

    def seleccionar_comedores_aptos(self,comedores, plantas, porcentaje_seleccion=0.5):
        # 1. Evaluar la aptitud de cada comedor
        aptitudes = [self.calcular_proximidad_minima(comedor, plantas) for comedor in comedores]
        
        # 2. Clasificar los comedores basados en su aptitud
        # Usamos un truco aquí: zip para emparejar comedores con aptitudes, y luego ordenar basado en aptitud
        comedores_ordenados = [comedor for comedor, aptitud in sorted(zip(comedores, aptitudes), key=lambda x: x[1])]
        
        # 3. Seleccionar un subconjunto de los comedores más aptos
        num_seleccionados = int(len(comedores) * porcentaje_seleccion)
        return comedores_ordenados[:num_seleccionados]


    def run_genetic_algorithm(self):
        # Aquí va el código del algoritmo genético.
        # Por ejemplo:
        # 1. Evaluar la aptitud de cada "comedor" basado en su proximidad a las plantas.
        # 2. Seleccionar los "comedores" más aptos.
        # 3. Cruzar y mutar los "comedores" seleccionados para crear una nueva generación.
        # 4. Reemplazar la generación actual con la nueva generación.
        # 5. Repetir por un número determinado de generaciones o hasta que se alcance un criterio de parada.
        
        # Nota: Necesitarás definir cómo se evalúa la aptitud, cómo se seleccionan, cruzan y mutan los "comedores", etc.
        
        # Al final, actualiza la gráfica para mostrar los resultados del algoritmo genético.
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
    
    def generarMundo(self,index):
        self.update_comedores()
    

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
        # Velocidad de movimiento de los comedores
        speed = 1

        # Lista para almacenar las plantas que son comidas
        plantas_comidas = []

        for comedor in self.comedores:
            # Genera una dirección aleatoria en la que moverse
            angle = random.uniform(0, 2 * math.pi)
            move_x = math.cos(angle) * speed
            move_y = math.sin(angle) * speed

            # Actualiza la posición del comedor
            new_x = comedor[0] + move_x
            new_y = comedor[1] + move_y

            # Asegurarse de que el comedor no salga del límite del área de simulación
            new_x = max(0, min(40, new_x))
            new_y = max(0, min(40, new_y))

            index = self.comedores.index(comedor)
            self.comedores[index] = (new_x, new_y)

            # Verificar si el comedor está cerca de alguna planta
            for planta in self.plantas:
                if self.distancia_euclidiana((new_x, new_y), planta) < 1.5:  # Asumimos que si están a menos de 1.5 unidades, el comedor come la planta
                    plantas_comidas.append(planta)
        
        plantas_comidas_set = set(plantas_comidas)  # Convertir la lista a un conjunto

        # Eliminar las plantas que fueron comidas
        for planta in plantas_comidas_set:
            self.plantas.remove(planta)
            
            # Comportamiento de las plantas después de ser comidas
            comportamiento = self.combmgrowbackplants.currentText()
            if comportamiento == "Crece en un lugar aleatorio":
                new_x = random.uniform(0, 40)
                new_y = random.uniform(0, 40)
                self.plantas.append((new_x, new_y))
            elif comportamiento == "Crece cerca":
                # Ajustar la posición para que esté cerca de la posición anterior
                dx = random.uniform(-2, 2)
                dy = random.uniform(-2, 2)
                new_x = planta[0] + dx
                new_y = planta[1] + dy
                # Asegurarse de que las nuevas coordenadas están dentro de los límites
                new_x = max(0, min(40, new_x))
                new_y = max(0, min(40, new_y))
                self.plantas.append((new_x, new_y))
            # Si el comportamiento es "No regresa", entonces simplemente no hacemos nada

        # Actualiza la gráfica
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
        # Iniciar el temporizador con un intervalo de tiempo (por ejemplo, 100 ms)
        self.timer.start(100)

    def pausar_moviemitno(self):
        print("dunción pausar m")

    def movimientopaso_x_paso(self):
        print("funcionamiento paso por paso")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
