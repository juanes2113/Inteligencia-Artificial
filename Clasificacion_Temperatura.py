import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cargar los datos
url = r'C:\Users\emman\OneDrive\Documentos\Juan\Poli\SEMESTRE 8\INTELIGENCIA ARTIFICIAL\daily_weather.csv'
data = pd.read_csv(url)

# Reemplazar NaN con la media de cada columna
data = data.fillna(data.mean())

# Definir las categorías para la variable objetivo
data['class_humidity'] = pd.qcut(data['relative_humidity_3pm'], q=3, labels=['Baja', 'Media', 'Alta'])

# Selección de características y variable objetivo
X = data[['relative_humidity_9am', 'air_pressure_9am', 'avg_wind_speed_9am']]
X.columns = ['Humedad', 'Presión', 'Velocidad']
y = data['class_humidity']
y.name = 'Clase de Humedad'

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Escalar características
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Crear y entrenar el modelo de regresión logística
clasificacion_model = LogisticRegression(max_iter=200)
clasificacion_model.fit(X_train, y_train)

# Predice los valores en el conjunto de prueba
y_pred_clasificacion = clasificacion_model.predict(X_test)

# Calcular la matriz de confusión y el reporte de clasificación
conf_matrix = confusion_matrix(y_test, y_pred_clasificacion)
class_report_dict = classification_report(y_test, y_pred_clasificacion, output_dict=True)

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
    titulo = tk.Label(frame_titulo, text="Aprendizaje de Máquina Supervisado: Clasificación", font=("Helvetica", 16, "bold"))
    titulo.pack()

    # ----- Frame para la Tabla de Datos -----
    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.pack(side="left", padx=10, pady=10)

    # Crear tabla para mostrar los datos
    tabla = ttk.Treeview(frame_tabla, columns=list(X.columns) + [y.name], show='headings')

    # Definir encabezados y ancho de columnas
    for col in tabla['columns']:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)

    # Agregar filas a la tabla
    for i in range(10):
        valores = list(X.iloc[i]) + [y.iloc[i]]
        tabla.insert('', 'end', values=valores)

    # Barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    tabla.pack(side="left", fill="y", padx=5)
    scrollbar.pack(side="right", fill="y")

    # ----- Frame para la Gráfica -----
    frame_grafica = tk.Frame(frame_principal, width=600, height=400)
    frame_grafica.pack(side="right", padx=10, pady=10)
    frame_grafica.pack_propagate(False)

    # Crear la figura para la matriz de confusión
    fig, ax = plt.subplots()
    cax = ax.matshow(conf_matrix, cmap='Blues')
    fig.colorbar(cax)

    # Configurar etiquetas de los ejes
    clases = list(set(y))
    ax.set_xticks(range(len(clases)))
    ax.set_xticklabels(clases)
    ax.set_yticks(range(len(clases)))
    ax.set_yticklabels(clases)
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de Confusión")

    # Insertar la figura en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # ----- Frame para el Reporte de Clasificación -----
    frame_resultados = tk.Frame(root)
    frame_resultados.pack(pady=10)

    # Crear la tabla para el reporte de clasificación
    columnas_reporte = ['Clase', 'Precisión', 'Recall', 'F1-Score', 'Soporte']
    tabla_reporte = ttk.Treeview(frame_resultados, columns=columnas_reporte, show='headings')

    # Definir encabezados y ancho de columnas
    for col in columnas_reporte:
        tabla_reporte.heading(col, text=col)
        tabla_reporte.column(col, anchor="center", width=120)

    # Agregar filas al reporte de clasificación
    for clase, valores in class_report_dict.items():
        if isinstance(valores, dict):  # Evitar las métricas globales
            fila = [clase] + [round(valores[metrica], 2) for metrica in ['precision', 'recall', 'f1-score', 'support']]
            tabla_reporte.insert('', 'end', values=fila)

    # Empaquetar la tabla de reporte
    tabla_reporte.pack()

    root.mainloop()

# Llamar a la función para mostrar la interfaz gráfica
mostrar_datos()