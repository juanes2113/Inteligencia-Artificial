import numpy as np
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random
import tkinter as tk

# Cargar la imagen desde una URL
url = 'https://thumbs.dreamstime.com/b/golden-retriever-puppy-2-months-old-sitting-17001032.jpg'
rta = requests.get(url)
imagen_deseada = Image.open(BytesIO(rta.content))
imagen_deseada = imagen_deseada.resize((250, 250))  # Reducir resolución

# Convertir la imagen deseada a escala de grises
imagen_deseada_array = np.array(imagen_deseada)
imagen_deseada_array = 0.3 * imagen_deseada_array[:, :, 0] + 0.6 * imagen_deseada_array[:, :, 1] + 0.1 * imagen_deseada_array[:, :, 2]

# Crear una imagen inicial blanca de 100x100
imagen_inicial = Image.new("RGB", (250, 250), color=(255, 255, 255))
imagen_inicial_array = np.array(imagen_inicial)
imagen_inicial_array = 0.3 * imagen_inicial_array[:, :, 0] + 0.6 * imagen_inicial_array[:, :, 1] + 0.1 * imagen_inicial_array[:, :, 2]

# Función de adaptación
def calcular_adaptacion(imagen_array):
    diff_array = np.abs(imagen_deseada_array - imagen_array)
    adaptacion = np.sum(diff_array)
    return adaptacion

# Función de mutación
def funcion_mutacion(imagen_array):
    mutacion_array = np.copy(imagen_array)
    for i in range(10):
        x = random.randint(0, imagen_array.shape[0] - 1)
        y = random.randint(0, imagen_array.shape[1] - 1)
        mutacion_array[x, y] = random.randint(0, 255)
    return mutacion_array

# Función de selección
def funcion_seleccion(poblacion, adaptacion, num_padres):
    ganadores = []
    for i in range(num_padres):
        torneo_indices = random.sample(range(len(poblacion)), 5)
        torneo_adaptacion = [adaptacion[j] for j in torneo_indices]
        ganador = torneo_indices[torneo_adaptacion.index(min(torneo_adaptacion))]
        ganadores.append(ganador)
    return [poblacion[i] for i in ganadores]

# Función para actualizar la interfaz con la imagen actual
def actualizar_imagen(imagen_array, label):
    imagen = Image.fromarray(imagen_array.astype('uint8'))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label.config(image=imagen_tk)
    label.image = imagen_tk

# Función principal del algoritmo genético
def ejecutar_algoritmo():
    tam_poblacion = 5000
    num_padres = 100
    num_iteraciones = 5

    poblacion_actual = [imagen_inicial_array] * tam_poblacion
    for i in range(num_iteraciones):
        puntos = [calcular_adaptacion(image) for image in poblacion_actual]
        padres = funcion_seleccion(poblacion_actual, puntos, num_padres)
        hijos = []

        for padre in padres:
            mutacion = funcion_mutacion(padre)
            hijos.append(mutacion)

        poblacion_actual = padres + hijos

        # Actualizar la mejor imagen cada 100 iteraciones
        if i % 100 == 0:
            mejor_indice = puntos.index(min(puntos))
            mejor_imagen = poblacion_actual[mejor_indice]
            actualizar_imagen(mejor_imagen, label_modificada)

    # Mostrar la mejor imagen generada
    mejor_indice = puntos.index(min(puntos))
    mejor_imagen = poblacion_actual[mejor_indice]
    actualizar_imagen(mejor_imagen, label_modificada)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Algoritmo Genético - Evolución de Imágenes")

# Cargar y mostrar la imagen deseada
imagen_deseada_pil = Image.fromarray(imagen_deseada_array.astype('uint8'))
imagen_deseada_tk = ImageTk.PhotoImage(imagen_deseada_pil)

label_deseada = tk.Label(root, text="Imagen Deseada", image=imagen_deseada_tk)
label_deseada.pack(side="left", padx=10, pady=10)

# Mostrar la imagen modificada que se va evolucionando
label_modificada = tk.Label(root, text="Imagen Modificada")
label_modificada.pack(side="right", padx=10, pady=10)

# Botón para ejecutar el algoritmo genético
boton = tk.Button(root, text="Iniciar Evolución", command=ejecutar_algoritmo)
boton.pack(pady=20)

# Iniciar la interfaz gráfica
root.mainloop()

# pip install numpy Pillow requests matplotlib
