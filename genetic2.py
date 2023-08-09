import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QMenu, QAction
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import random


class Cell:
    def __init__(self):
        self.eater = None
        self.plant = None


class Eater:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.state = 0
        self.x = 0
        self.y = 0
        # 0: up, 1: right, 2: down, 3: left
        self.direction = random.randint(0, 3)
        self.score = 0

    def decide_action(self, cell_in_front):
        plant_value = 1 if cell_in_front.plant else 0
        rule = self.chromosome[self.state * 4 + plant_value]
        self.state = rule // 4
        return rule % 4  # 0: move forward, 1: move back, 2: turn left, 3: turn right


class World:
    def __init__(self, size, num_eaters, num_plants):
        self.size = size
        self.grid = np.empty((size, size), dtype=object)
        for i in range(size):
            for j in range(size):
                self.grid[i, j] = Cell()

        self.eaters = [Eater(np.random.randint(0, 64, 64))
                       for _ in range(num_eaters)]
        for eater in self.eaters:
            while True:
                x = np.random.randint(0, size)
                y = np.random.randint(0, size)
                if self.grid[x, y].eater is None:
                    self.grid[x, y].eater = eater
                    eater.x = x
                    eater.y = y
                    break

        for _ in range(num_plants):
            while True:
                x = np.random.randint(0, size)
                y = np.random.randint(0, size)
                if self.grid[x, y].plant is None:
                    self.grid[x, y].plant = True
                    break

    def advance_time(self):
        for eater in self.eaters:
            dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][eater.direction]
            cell_in_front = self.grid[(eater.x + dx) %
                                      self.size, (eater.y + dy) % self.size]
            action = eater.decide_action(cell_in_front)
            if action == 0:  # move forward
                if cell_in_front.eater is None:
                    self.grid[eater.x, eater.y].eater = None
                    eater.x = (eater.x + dx) % self.size
                    eater.y = (eater.y + dy) % self.size
                    self.grid[eater.x, eater.y].eater = eater
                    if self.grid[eater.x, eater.y].plant is not None:
                        eater.score += 1
                        self.grid[eater.x, eater.y].plant = None
            elif action == 1:  # move backward
                x = (eater.x - dx) % self.size
                y = (eater.y - dy) % self.size
                if self.grid[x, y].eater is None:
                    self.grid[eater.x, eater.y].eater = None
                    eater.x = x
                    eater.y = y
                    self.grid[x, y].eater = eater
            elif action == 2:  # turn left
                eater.direction = (eater.direction - 1) % 4
            else:  # turn right
                eater.direction = (eater.direction + 1) % 4

    def visualize(self):
        image = np.zeros((self.size, self.size, 3), dtype=float)
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j].plant is not None:
                    image[i, j, 1] = 1.0
                if self.grid[i, j].eater is not None:
                    image[i, j, 0] = 1.0
        plt.imshow(image)

    def draw_world(self):
        # Create a figure
        fig, ax = plt.subplots()

        # Convert world to numpy array for visualization
        world = np.zeros((self.size, self.size))

        # Fill the numpy array with the status of the world
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y].eater:
                    world[x][y] = 1
                elif self.grid[x][y].plant:
                    world[x][y] = 2

        # Plot the world, eaters and plants
        world_map = ax.imshow(world, cmap='tab10')

        plt.show(block=False)

        return fig, world_map

    def update_world(self, fig, world_map):
        # Convert world to numpy array for visualization
        world = np.zeros((self.size, self.size))

        # Fill the numpy array with the status of the world
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y].eater:
                    world[x][y] = 1
                elif self.grid[x][y].plant:
                    world[x][y] = 2

        # Update the plot data
        world_map.set_data(world)

        # Redraw the figure
        fig.canvas.draw_idle()

        plt.pause(0.1)


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        self.world = World(20, 25, 250)  # initial world
        MyMplCanvas.__init__(self, *args, **kwargs)  # Now this line comes after the initialization of world.
        self.timer = QTimer(self)  # Create a QTimer instance
        self.timer.timeout.connect(self.update_figure)  # Connect the timer timeout signal to update_figure
        self.timer.start(100)  # Fire the timeout signal every 100ms

    def update_figure(self):
        self.world.advance_time()
        world_np = np.zeros((self.world.size, self.world.size))
        for i in range(self.world.size):
            for j in range(self.world.size):
                if self.world.grid[i][j].eater:
                    world_np[i][j] = 1
                elif self.world.grid[i][j].plant:
                    world_np[i][j] = 2
        self.axes.clear()  # clear the previous plot
        self.axes.imshow(world_np, cmap='tab10')
        self.draw()

    def compute_initial_figure(self):
        world_np = np.zeros((self.world.size, self.world.size))
        for i in range(self.world.size):
            for j in range(self.world.size):
                if self.world.grid[i][j].eater:
                    world_np[i][j] = 1
                elif self.world.grid[i][j].plant:
                    world_np[i][j] = 2
        self.axes.imshow(world_np, cmap='tab10')




class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

if __name__ == '__main__':
    qApp = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % "PyQt5 window with a matplotlib plot")
    aw.show()

    sys.exit(qApp.exec_())
