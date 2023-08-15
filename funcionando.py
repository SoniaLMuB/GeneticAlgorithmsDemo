import sys
import random
import math
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.style as mplstyle
mplstyle.use('fast')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dias=0
        self.anios=0
        self.Programacorriendo=False
        self.correrPrograma=False
        self.cache=None
        self.comedores_graphics = []
        self.plantas_graphics = []
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
        self.buttonCorrer = QPushButton('Correr')
        self.buttonPausa = QPushButton('Pausa')
        self.buttonStep = QPushButton('Por paso')
        self.buttonMundo = QPushButton('Generar mundo')
        self.buttonCorrer.setEnabled(False)
        self.buttonPausa.setEnabled(False)
        self.buttonStep.setEnabled(False)

        
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

        labelcrossover = QLabel("% Probabilidad de cruce:")
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
        
        self.labelDias = QLabel(f"Año {self.anios}. Día: {self.dias}")
        controleslayout.addWidget(self.labelDias)

        #Agregamos los botones al layout de botones
        controleslayout.addWidget(self.buttonCorrer)
        controleslayout.addWidget(self.buttonPausa)
        controleslayout.addWidget(self.buttonStep)
        controleslayout.addWidget(self.buttonMundo)

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
        self.buttonCorrer.clicked.connect(self.start)
        self.buttonMundo.clicked.connect(self.generarMundo)
        self.buttonPausa.clicked.connect(self.pausar_moviemitno)
        self.buttonStep.clicked.connect(self.movimientopaso_x_paso)

        

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
    
    def generarMundo(self):
        self.dias = 0
        self.anios =0
        self.correrPrograma=True
        if (self.correrPrograma ):
            self.buttonCorrer.setEnabled(True)
            self.buttonPausa.setEnabled(True)
            self.buttonStep.setEnabled(True)
        self.labelDias.setText(f"Año {self.anios}. Día: {self.dias}")

        self.update_comedores() 

    def mutate(self, comedor):
        mutation_rate = float(self.combmutation.currentText())
        if random.uniform(0, 100) < mutation_rate:
            # Cambiamos ligeramente las coordenadas del comedor
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            mutated_x = comedor[0] + dx
            mutated_y = comedor[1] + dy
            return (mutated_x, mutated_y)
        return comedor

    def generar_nueva_generacion(self, comedores_seleccionados):
        nueva_generacion = []
        crossover_rate = float(self.combmcrossover.currentText())

        for i in range(0, len(comedores_seleccionados)-1, 2):
            parent1 = comedores_seleccionados[i]
            parent2 = comedores_seleccionados[i+1]

            # Aplicamos el crossover con una cierta probabilidad
            if random.uniform(0, 100) < crossover_rate:
                child1, child2 = self.crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            # Mutamos a los hijos y los añadimos a la nueva generación
            nueva_generacion.append(self.mutate(child1))
            nueva_generacion.append(self.mutate(child2))

        return nueva_generacion

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

    def crossover(self, parent1, parent2):
        # Tomamos las coordenadas x de ambos padres y las intercambiamos
        child1 = (parent1[0], parent2[1])
        child2 = (parent2[0], parent1[1])
        return child1, child2


    def reiniciar_mundo(self):
        comedores_seleccionados = self.seleccionar_comedores_aptos(self.comedores, self.plantas)
        self.comedores = self.generar_nueva_generacion(comedores_seleccionados)
        self.update_comedores()  # reiniciar comedores y plantas
        self.anios = 0
        self.dias = 0
        self.labelDias.setText(f"Día: {self.dias}")

    def move_comedores(self):
        self.dias +=1
        # Velocidad de movimiento de los comedores
        speed = 1
        if (self.dias==250):
            self.anios +=1
            print(self.anios)
            self.dias=0
            
        if (self.anios>=1):
            self.labelDias.setText(f"Año {self.anios}. Día: {self.dias}")
            self.reiniciar_mundo()
            print("salie")
            return
        else:
            self.labelDias.setText(f"Día: {self.dias}")
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
        # Limpiamos la figura
        if not self.comedores_graphics:  # Si es la primera vez
            ax = self.figure.add_subplot(111)
            
            # Dibuja comedores
            for x, y in self.comedores:
                comedor, = ax.plot(x, y, "4", color='red', markersize=7)
                self.comedores_graphics.append(comedor)

            # Dibuja plantas
            for x, y in self.plantas:
                planta = ax.add_patch(plt.Rectangle((x, y), 0.5, 0.5, color='green'))
                self.plantas_graphics.append(planta)

            ax.set_xlim(0, 40)
            ax.set_ylim(0, 40)
            ax.set_yticks([])
            ax.set_xticks([])

            self.canvas.draw()
        else:
            # Si no es la primera vez, solo actualiza las coordenadas
            for comedor_graphic, (x, y) in zip(self.comedores_graphics, self.comedores):
                comedor_graphic.set_data([x], [y])
            
            # Actualiza las plantas (esto es un poco más complicado ya que son rectángulos)
            for planta_graphic, (x, y) in zip(self.plantas_graphics, self.plantas):
                planta_graphic.set_xy((x, y))

            self.canvas.draw_idle()  # Este es un draw más eficiente para actualizaciones

    def update_plot(self):
        #self.canvas.restore_region(self.cache)
        self.plot_example()


    def start(self):
        # Iniciar el temporizador con un intervalo de tiempo (por ejemplo, 100 ms)
        self.Programacorriendo=True
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
