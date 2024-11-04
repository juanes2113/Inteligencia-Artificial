import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cargar los datos
url = r'C:\Users\emman\OneDrive\Documentos\Juan\Poli\SEMESTRE 8\INTELIGENCIA ARTIFICIAL\daily_weather.csv'
data = pd.read_csv(url)

# Reemplazar NaN con la media de cada columna
data = data.fillna(data.mean())

# Selección de características y variable objetivo con nuevos nombres
X = data[['relative_humidity_9am', 'air_pressure_9am', 'avg_wind_speed_9am']]
X.columns = ['Humedad', 'Presión', 'Velocidad']
y = data['relative_humidity_3pm']
y.name = 'Temperatura'

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Crear y entrenar el modelo de regresión lineal
regresion_model = LinearRegression()
regresion_model.fit(X_train, y_train)

# Predice los valores en el conjunto de prueba
y_pred_regresion = regresion_model.predict(X_test)

# Calcular el error cuadrático medio
mse = mean_squared_error(y_test, y_pred_regresion)

# Calcular el coeficiente de correlación
correlation_coef = np.corrcoef(y_test, y_pred_regresion)[0, 1]

# Crear interfaz gráfica
def mostrar_datos():
    # Crear ventana
    root = tk.Tk()
    root.title("Datos Meteorológicos")
    root.maxsize(1600, 1600)

    # Frame principal para organizar tabla y gráfica en paralelo
    frame_principal = tk.Frame(root)
    frame_principal.pack(fill="both", expand=True)
    
    # Estilo de la tabla
    estilo = ttk.Style()
    estilo.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), anchor="center")
    estilo.configure("Treeview", font=("Helvetica", 10), rowheight=30, anchor="center")
    
    # Frame para el título
    frame_titulo = tk.Frame(frame_principal)
    frame_titulo.pack(pady=10)
    titulo = tk.Label(frame_titulo, text="Aprendizaje de Máquina Supervisado: Regresión", font=("Helvetica", 16, "bold"))
    titulo.pack()

    # ----- Frame para la Tabla -----
    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.pack(side="left", padx=10, pady=10)

    # Crear tabla sin la columna raíz
    tabla = ttk.Treeview(frame_tabla, columns=list(X.columns) + [y.name], show='headings')

    # Definir encabezados y ancho de columnas
    for col in tabla['columns']:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)

    # Agregar filas a la tabla
    for i in range(10):
        valores = list(X.iloc[i]) + [y.iloc[i]]
        tabla.insert('', 'end', values=valores)

    # Configurar barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)

    # Empaquetar la tabla y la barra de desplazamiento
    tabla.pack(side="left", fill="y", padx=5)
    scrollbar.pack(side="right", fill="y")

    # ----- Frame para la Gráfica -----
    frame_grafica = tk.Frame(frame_principal)
    frame_grafica.pack(side="right", padx=10, pady=10)

    # Crear la figura de Matplotlib
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred_regresion, color='blue', label='Predicciones')
    
    # Agregar la línea de ajuste (en rojo)
    ax.plot(y_test, y_test, color='red', linestyle='--', label='Línea de Ajuste')
    
    ax.set_xlabel("Temperatura Real")
    ax.set_ylabel("Temperatura Predicha")
    ax.set_title("Predicción de Temperatura")
    ax.legend()

    # Insertar la figura en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Mostrar MSE y coeficiente de correlación en la interfaz
    frame_resultados = tk.Frame(root)
    frame_resultados.pack(pady=10)
    
    label_mse = tk.Label(frame_resultados, text=f"Error cuadrático medio (MSE): {mse:.2f}", font=("Helvetica", 12))
    label_mse.pack()

    label_correlation = tk.Label(frame_resultados, text=f"Coeficiente de correlación: {correlation_coef:.2f}", font=("Helvetica", 12))
    label_correlation.pack()

    root.mainloop()

# Llamar a la función para mostrar la interfaz gráfica
mostrar_datos()