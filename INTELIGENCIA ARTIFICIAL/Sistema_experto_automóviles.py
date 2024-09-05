import tkinter as tk
from tkinter import messagebox
from clips import Environment

# Creamos la instancia del entorno CLIPS
env = Environment()

# Definimos la plantilla de síntomas
env.build("""
(deftemplate symptom
  (slot name))
""")

# Definimos las reglas, pero eliminamos los hechos iniciales
env.build("""
(defrule bateria-descargada
  (symptom (name "El auto no arranca"))
  (symptom (name "Las luces no se encienden"))
  =>
  (assert (diagnosis "La batería está descargada")))
""")

env.build("""
(defrule problema-alternador
  (symptom (name "El auto no arranca"))
  (symptom (name "La batería está nueva"))
  =>
  (assert (diagnosis "Posible problema con el alternador")))
""")

env.build("""
(defrule problema-motor-arranque
  (symptom (name "El motor hace clics"))
  =>
  (assert (diagnosis "Posible problema con el motor de arranque")))
""")

# Función para ejecutar las reglas y mostrar resultados
def run_expert_system(selected_symptoms):
    env.reset()  # Restablecemos el entorno CLIPS
    
    # Agregamos los síntomas seleccionados por el usuario al entorno CLIPS
    for symptom in selected_symptoms:
        env.assert_string(f'(symptom (name "{symptom}"))')
    
    # Ejecutamos las reglas en el entorno
    env.run()
    
    # Obtenemos los diagnósticos generados
    diagnoses = []
    for fact in env.facts():
        if fact.template.name == 'diagnosis':
            diagnoses.append(fact[0])
    
    # Mostramos el diagnóstico relevante
    if diagnoses:
        messagebox.showinfo("Diagnóstico", "\n".join(diagnoses))
    else:
        messagebox.showinfo("Diagnóstico", "No se ha podido realizar un diagnóstico.")

# Función para obtener los síntomas seleccionados por el usuario
def get_selected_symptoms():
    selected = []
    for symptom, var in symptom_vars.items():
        if var.get():
            selected.append(symptom)
    run_expert_system(selected)

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Sistema Experto para Diagnóstico de Automóviles")

# Etiqueta de instrucciones
label = tk.Label(root, text="Seleccione los síntomas observados:")
label.pack(pady=10)

# Diccionario de síntomas y variables de control
symptoms = ["El auto no arranca", "Las luces no se encienden", "El motor hace clics", "La batería está nueva"]
symptom_vars = {symptom: tk.BooleanVar() for symptom in symptoms}

# Creación de checkboxes para cada síntoma
for symptom, var in symptom_vars.items():
    checkbox = tk.Checkbutton(root, text=symptom, variable=var)
    checkbox.pack(anchor='w')

# Botón para ejecutar el sistema experto
run_button = tk.Button(root, text="Diagnosticar", command=get_selected_symptoms)
run_button.pack(pady=10)

# Inicia el loop de la interfaz gráfica
root.mainloop()