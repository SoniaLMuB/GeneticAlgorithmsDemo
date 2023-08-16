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

class Eater:
    ORIENTACIONES = ["N", "E", "S", "W"]  # Norte, Este, Sur, Oeste

    def __init__(self, x, y, genoma=None):
        self.x = x
        self.y = y
        self.direction = random.choice(['N', 'E', 'S', 'W'])  # Dirección inicial aleatoria
        if genoma:
            self.genoma = genoma
        else:
            # Si no se proporciona un genoma, generamos uno aleatorio.
            self.genoma = [random.randint(0, 15) for _ in range(64)]
        #self.posicion = posicion
        #self.orientacion = orientacion
        #self.estado = estado

    # def girar_izquierda(self):
    #     idx = self.ORIENTACIONES.index(self.orientacion)
    #     self.orientacion = self.ORIENTACIONES[(idx - 1) % 4]

    # def girar_derecha(self):
    #     idx = self.ORIENTACIONES.index(self.orientacion)
    #     self.orientacion = self.ORIENTACIONES[(idx + 1) % 4]

    # def avanzar(self):
    #     x, y = self.posicion
    #     if self.orientacion == "N":
    #         self.posicion = (x, y + 1)
    #     elif self.orientacion == "E":
    #         self.posicion = (x + 1, y)
    #     elif self.orientacion == "S":
    #         self.posicion = (x, y - 1)
    #     elif self.orientacion == "W":
    #         self.posicion = (x - 1, y)

    # def retroceder(self):
    #     x, y = self.posicion
    #     if self.orientacion == "N":
    #         self.posicion = (x, y - 1)
    #     elif self.orientacion == "E":
    #         self.posicion = (x - 1, y)
    #     elif self.orientacion == "S":
    #         self.posicion = (x, y + 1)
    #     elif self.orientacion == "W":
    #         self.posicion = (x + 1, y)

    # def cambiar_estado(self, nuevo_estado):
    #     self.estado = nuevo_estado % 16  # Asegura que el estado esté entre 0 y 15
    
    def see(self, world):
        # Usaremos las direcciones para determinar qué es "enfrente" del Eater
        directions = {
            'up': (0, 1),
            'down': (0, -1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        
        # Calculamos las coordenadas del cuadrado frente al Eater
        front_x = self.x + directions[self.direction][0]
        front_y = self.y + directions[self.direction][1]
        
        # Comprobamos qué hay en esa posición en el mundo
        return world.get_at(front_x, front_y)

    
    def act(self, world):
        # Ver lo que hay en frente
        front_object = self.see(world)
        
        # Definir acciones basadas en lo que ve
        if front_object == 'plant':
            self.eat(world)
        elif front_object == 'empty':
            self.move_forward(world)
        elif front_object == 'wall' or front_object == 'eater':
            self.turn_random()

    def eat(self, world):
        # Asume que la planta ya ha sido "comida", por lo que solo incrementa el puntaje
        self.score += 1

    def move_forward(self, world):
        # Mueve el Eater una posición en la dirección en la que está mirando
        directions = {
            'up': (0, 1),
            'down': (0, -1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        self.x += directions[self.direction][0]
        self.y += directions[self.direction][1]

    def turn_random(self):
        # Gira el Eater en una dirección aleatoria
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    
    @staticmethod
    def generate_random_genoma():
        return ''.join([str(random.randint(1, 4)) for _ in range(4)])

    def move_based_on_genoma(self, vision):
        # Aquí, la "visión" es lo que el comedor "ve" en frente de él.
        # Por simplicidad, asumimos que la visión puede ser: "planta", "comedor", "pared", o "nada".
        vision_map = {"planta": 0, "comedor": 1, "pared": 2, "nada": 3}
        action = int(self.genoma[vision_map[vision]])
        
        # Por ahora, las acciones son simples y se basan en el genoma:
        # 1 = avance
        # 2 = gire a la izquierda
        # 3 = gire a la derecha
        # 4 = retroceda
        if action == 1:
            angle = 0
        elif action == 2:
            angle = -90
        elif action == 3:
            angle = 90
        else:
            angle = 180
        
        # Convertir el ángulo a radianes y calcular el movimiento.
        angle_rad = math.radians(angle)
        move_x = math.cos(angle_rad)
        move_y = math.sin(angle_rad)
        
        self.x += move_x
        self.y += move_y

    @staticmethod
    def crossover(parent1, parent2):
        # Tomamos la primera mitad del genoma de un padre y la segunda mitad del otro padre.
        split_point = len(parent1.genoma) // 2
        child_genoma = parent1.genoma[:split_point] + parent2.genoma[split_point:]
        return Eater(parent1.x, parent1.y, child_genoma)

    def mutate(self, mutation_rate):
        # Hay una probabilidad de mutation_rate de que un gen cambie.
        new_genoma = ''
        for gene in self.genoma:
            if random.uniform(0, 100) < mutation_rate:
                new_genoma += str(random.randint(1, 4))
            else:
                new_genoma += gene
        self.genoma = new_genoma

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
            comedor = Eater(x, y)
            comedores.append(comedor)
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

    def ver_frente(self, otros_comedores, plantas):
        x, y = self.posicion
        if self.orientacion == "N":
            x, y = x, y + 1
        elif self.orientacion == "E":
            x, y = x + 1, y
        elif self.orientacion == "S":
            x, y = x, y - 1
        elif self.orientacion == "W":
            x, y = x - 1, y

        # Verificar si está viendo una pared
        if x < 0 or x >= 40 or y < 0 or y >= 40:
            return "pared"
        
        # Verificar si está viendo otro comedor
        for comedor in otros_comedores:
            if comedor.posicion == (x, y):
                return "comedor"

        # Verificar si está viendo una planta
        for planta in plantas:
            if planta == (x, y):
                return "planta"

        return "espacio"

    def aplicar_reglas(self, vista):
        if vista == "planta":
            self.avanzar()
        elif vista == "comedor":
            self.girar_izquierda()
        elif vista == "pared":
            self.girar_derecha()
        elif vista == "espacio":
            if self.estado % 2 == 0:
                self.avanzar()
            else:
                self.girar_izquierda()

    
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
            vista = comedor.ver_frente(self.comedores, self.plantas)
            comedor.aplicar_reglas(vista)
            comedor.act(self)  # Llama al método act del Eater
            if vista == "planta":
                comedor.avanzar()
            elif vista in ["pared", "comedor"]:
                comedor.girar_izquierda()
            else:
                accion = random.choice(["avanzar", "retroceder", "girar_izquierda", "girar_derecha"])
                if accion == "avanzar":
                    comedor.avanzar()
                elif accion == "retroceder":
                    comedor.retroceder()
                elif accion == "girar_izquierda":
                    comedor.girar_izquierda()
                elif accion == "girar_derecha":
                    comedor.girar_derecha()

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
            for comedor in self.comedores:
                comedor_graphic, = ax.plot(comedor.x, comedor.y, "4", color='red', markersize=7)
                self.comedores_graphics.append(comedor_graphic)

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
