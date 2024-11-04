import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from tkinter import Tk, Label, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cargar y preprocesar los datos
url = r'C:\Users\emman\OneDrive\Documentos\Juan\Poli\SEMESTRE 8\INTELIGENCIA ARTIFICIAL\daily_weather.csv'
data = pd.read_csv(url)
data = data.fillna(data.mean())

# Seleccionar características y variable objetivo
X = data[['relative_humidity_9am', 'air_pressure_9am', 'avg_wind_speed_9am']]
y = data['relative_humidity_3pm']

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Definir el modelo usando la API funcional de TensorFlow
inputs = tf.keras.Input(shape=(X_train.shape[1],))
x = tf.keras.layers.Dense(64, activation='relu')(inputs)
x = tf.keras.layers.Dense(32, activation='relu')(x)
outputs = tf.keras.layers.Dense(1)(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, verbose=1)

# Calcular el MAE en el conjunto de prueba
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)

# Función para predecir y graficar resultados
def predict_and_plot():
    predictions = model.predict(X_test).flatten()
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values, label='Actual Humidity')
    plt.plot(predictions, label='Predicted Humidity')
    plt.xlabel('Sample')
    plt.ylabel('Relative Humidity at 3 pm')
    plt.legend()
    plt.show()

# Interfaz gráfica con Tkinter
class WeatherPredictionApp:
    def __init__(self, master):
        self.master = master
        master.title("Weather Prediction")

        self.label = Label(master, text="Predicción de humedad relativa con RNA", font=("Helvetica", 14))
        self.label.pack(pady=10)
        
        # Etiqueta para mostrar el MAE
        self.mae_label = Label(master, text=f"Error Absoluto Medio (MAE): {test_mae:.2f}", font=("Helvetica", 12))
        self.mae_label.pack(pady=5)

        self.plot_button = Button(master, text="Mostrar Predicción", command=self.show_plot)
        self.plot_button.pack(pady=5)

        self.close_button = Button(master, text="Cerrar", command=master.quit)
        self.close_button.pack(pady=5)

        # Crear marco para los gráficos
        self.frame = Frame(master)
        self.frame.pack(pady=10)

    def show_plot(self):
        # Crear el gráfico en Tkinter
        fig, ax = plt.subplots(figsize=(8, 4))
        predictions = model.predict(X_test).flatten()
        ax.plot(y_test.values, label='Actual Humidity')
        ax.plot(predictions, label='Predicted Humidity')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Relative Humidity at 3 pm')
        ax.legend()

        # Integrar el gráfico en la interfaz Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Inicializar la aplicación
root = Tk()
app = WeatherPredictionApp(root)
root.mainloop()

"""
Capa de entrada: Recibe las características de entrada (como la humedad relativa a las 9 am, presión de aire, y velocidad del viento promedio).
Capas ocultas: Procesan las entradas con funciones de activación (por ejemplo, ReLU).
Capa de salida: Proporciona la predicción de la humedad relativa a las 3 pm.Aquí se muestra el progreso del entrenamiento para la primera época de un total de 100. En esta primera época:

Aquí se muestra el progreso del entrenamiento para la primera época de un total de 100. En esta primera época:
22/22 indica que el entrenamiento ha pasado por los 22 lotes (batches) de datos en el conjunto de entrenamiento.
2s es el tiempo total que tardó en completarse esta época.
18ms/step es el tiempo promedio por paso de entrenamiento.
loss (1772.8616) y mae (35.3326) son las métricas de error en el conjunto de entrenamiento, siendo loss la función de pérdida (objetivo principal a minimizar), y mae (mean absolute error o error absoluto medio) una métrica adicional.
val_loss (1793.6812) y val_mae (34.9861) representan las métricas de error en el conjunto de validación, permitiéndote monitorear cómo generaliza el modelo en datos no vistos durante el entrenamiento.
Estos valores indican que el modelo está comenzando a entrenarse, pero los errores (loss y mae) son altos.
"""