import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Configuraciones
N_INDIVIDUOS = 10
L_CROMOSOMA = 20
N_GENERACIONES = 100
P_MUTACION = 0.01

# Inicializa poblacion
poblacion = np.random.randint(2, size=(N_INDIVIDUOS, L_CROMOSOMA))

fig, ax = plt.subplots()

# Función de fitness


def fitness(individuo):
    return np.sum(individuo)

# Seleccion


def seleccion(poblacion):
    fit = np.array([fitness(ind) for ind in poblacion])
    probs = fit / np.sum(fit)
    padre = poblacion[np.random.choice(len(poblacion), p=probs)]
    madre = poblacion[np.random.choice(len(poblacion), p=probs)]
    return padre, madre

# Cruce


def cruce(padre, madre):
    pos = np.random.randint(L_CROMOSOMA)
    hijo1 = np.concatenate((padre[:pos], madre[pos:]))
    hijo2 = np.concatenate((madre[:pos], padre[pos:]))
    return hijo1, hijo2

# Mutación


def mutacion(individuo):
    for i in range(L_CROMOSOMA):
        if np.random.random() < P_MUTACION:
            individuo[i] = 1 - individuo[i]
    return individuo

# Actualiza la animación


def update(num):
    ax.clear()

    global poblacion
    nueva_poblacion = []
    for _ in range(N_INDIVIDUOS // 2):
        padre, madre = seleccion(poblacion)
        hijo1, hijo2 = cruce(padre, madre)
        nueva_poblacion.append(mutacion(hijo1))
        nueva_poblacion.append(mutacion(hijo2))

    poblacion = np.array(nueva_poblacion)

    c = ax.imshow(poblacion, cmap='gray')
    return c,


ani = animation.FuncAnimation(fig, update, frames=N_GENERACIONES, blit=True)
plt.show()
