import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# El objetivo es controlar la velocidad de un automóvil en función de la densidad del tráfico y la visibilidad.

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Sistema de Control Difuso para la Velocidad de un Vehículo")

# Variables para los valores de entrada
traffic_density_var = tk.DoubleVar()
visibility_var = tk.DoubleVar()
result_var = tk.StringVar()

# Definir las variables lingüísticas
traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')  # Densidad de tráfico de 0% a 100%
visibility = ctrl.Antecedent(np.arange(0, 101, 1), 'visibility')  # Visibilidad de 0% a 100%
speed = ctrl.Consequent(np.arange(0, 121, 1), 'speed')  # Velocidad de 0 km/h a 120 km/h

# Funciones de membresía para la densidad de tráfico
traffic_density['low'] = fuzz.trapmf(traffic_density.universe, [0, 0, 20, 50])
traffic_density['medium'] = fuzz.trapmf(traffic_density.universe, [30, 40, 60, 70])
traffic_density['high'] = fuzz.trapmf(traffic_density.universe, [60, 80, 100, 100])

# Funciones de membresía para la visibilidad
visibility['poor'] = fuzz.trapmf(visibility.universe, [0, 0, 20, 50])
visibility['average'] = fuzz.trapmf(visibility.universe, [30, 40, 60, 70])
visibility['good'] = fuzz.trapmf(visibility.universe, [60, 80, 100, 100])

# Funciones de membresía para la velocidad del automóvil
speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 60])
speed['moderate'] = fuzz.trimf(speed.universe, [40, 60, 80])
speed['fast'] = fuzz.trimf(speed.universe, [60, 120, 120])

# Reglas difusas

# Definimos las reglas de razonamiento que controlan el sistema.
# Por ejemplo, si la densidad de tráfico es alta o la visibilidad es baja, la velocidad debe ser lenta.

rule1 = ctrl.Rule(traffic_density['low'] & visibility['good'], speed['fast'])
rule2 = ctrl.Rule(traffic_density['medium'] & visibility['average'], speed['moderate'])
rule3 = ctrl.Rule(traffic_density['high'] | visibility['poor'], speed['slow'])

# Crear el sistema de control difuso
speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
speed_sim = ctrl.ControlSystemSimulation(speed_ctrl)

# Función para ejecutar la simulación con los valores proporcionados por el usuario
def simulate():
    try:
        traffic_density_value = traffic_density_var.get()
        visibility_value = visibility_var.get()

        # Verificar que los valores estén dentro del rango permitido
        if 0 <= traffic_density_value <= 100 and 0 <= visibility_value <= 100:
            # Proporcionar los valores de entrada
            speed_sim.input['traffic_density'] = traffic_density_value
            speed_sim.input['visibility'] = visibility_value

            # Ejecutar la simulación
            speed_sim.compute()
            
            # Mostrar el resultado
            result_var.set(f"Velocidad recomendada: {speed_sim.output['speed']:.2f} km/h")

            # Visualizar la salida de velocidad después de la defuzificación
            speed.view(sim=speed_sim)
            plt.show()
        else:
            messagebox.showerror("Error", "Los valores deben estar entre 0 y 100.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
# Función para reiniciar los valores
def reset():
    traffic_density_var.set(0)
    visibility_var.set(0)
    result_var.set("")

# Crear los paneles
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

frame1.grid(row=0, column=0, padx=10, pady=10)
frame2.grid(row=0, column=1, padx=10, pady=10)

# Panel 1: Visualización de las funciones de membresía
tk.Label(frame1, text="Funciones de Membresía").grid(row=0, column=0, columnspan=2)

def plot_memberships():
    traffic_density.view()
    visibility.view()
    speed.view()
    plt.show()

tk.Button(frame1, text="Mostrar Rangos", command=plot_memberships).grid(row=1, column=0, columnspan=2)

# Panel 2: Entrada del usuario y resultado
tk.Label(frame2, text="Densidad de Tráfico (0-100)").grid(row=0, column=0)
tk.Entry(frame2, textvariable=traffic_density_var).grid(row=0, column=1)

tk.Label(frame2, text="Visibilidad (0-100)").grid(row=1, column=0)
tk.Entry(frame2, textvariable=visibility_var).grid(row=1, column=1)

tk.Button(frame2, text="Simular", command=simulate).grid(row=2, column=0)
tk.Button(frame2, text="Resetear", command=reset).grid(row=2, column=1)

tk.Label(frame2, textvariable=result_var).grid(row=3, columnspan=2)

# Iniciar la aplicación
root.mainloop()

