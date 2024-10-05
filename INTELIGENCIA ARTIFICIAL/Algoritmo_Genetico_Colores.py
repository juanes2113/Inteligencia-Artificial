import tkinter as tk
import random
import math

# Parámetros del Algoritmo Genético
POPULATION_SIZE = 10 # Tamaño de la población
NUM_GENERATIONS = 2000
MUTATION_RATE = 0.1 # Posibilidadde que un algoritmo mute
STOP_THRESHOLD = 100  # Valor inicial de STOP_THRESHOLD

# Definimos colores primarios y sus combinaciones posibles
PRIMARY_COLORS = {
    'Rojo': (255, 0, 0),
    'Azul': (0, 0, 255),
    'Amarillo': (255, 255, 0),
}

TARGET_COLOR = (0, 255, 0)  # Verde

class ColorIndividual:
    def __init__(self, rgb):
        self.rgb = rgb

    def fitness(self, target_color):
        # Distancia Euclidiana entre los colores
        return -sum((self.rgb[i] - target_color[i]) ** 2 for i in range(3))


class Population:
    def __init__(self, target_color):
        self.individuals = [self.create_individual() for _ in range(POPULATION_SIZE)]
        self.target_color = target_color
        self.history = []

    def create_individual(self):
        # Genera un color aleatorio basado en los colores primarios
        return ColorIndividual(random.choice(list(PRIMARY_COLORS.values())))

    def fitness(self, individual):
        return individual.fitness(self.target_color)

    def mutate(self, individual):
        # Mutación: mezclar componentes de los colores primarios
        if random.random() < MUTATION_RATE:
            # Mezclar colores (modificar un canal RGB aleatorio)
            new_rgb = list(individual.rgb)
            channel_to_mutate = random.randint(0, 2)
            if channel_to_mutate == 0:  # Mezclar rojo
                new_rgb[channel_to_mutate] = (individual.rgb[0] + random.choice([PRIMARY_COLORS['Rojo'][0], 0])) // 2
            elif channel_to_mutate == 1:  # Mezclar verde
                new_rgb[channel_to_mutate] = (individual.rgb[1] + random.choice([PRIMARY_COLORS['Amarillo'][1], PRIMARY_COLORS['Azul'][1]])) // 2
            elif channel_to_mutate == 2:  # Mezclar azul
                new_rgb[channel_to_mutate] = (individual.rgb[2] + random.choice([PRIMARY_COLORS['Azul'][2], 0])) // 2
            individual.rgb = tuple(new_rgb)
        return individual

    def evolve(self):
        best_individual = max(self.individuals, key=lambda ind: self.fitness(ind))
        self.history.append(best_individual.rgb)
        new_population = []
        for _ in range(POPULATION_SIZE):
            mutated_individual = self.mutate(best_individual)
            new_population.append(mutated_individual)
        self.individuals = new_population
        return best_individual


class ColorEvolutionApp:
    def __init__(self, root):
        self.root = root
        self.target_color = TARGET_COLOR
        self.mutations_path1 = 0
        self.mutations_path2 = 0
        self.evolution_complete = False

        # Configuración de la interfaz gráfica
        self.canvas = tk.Canvas(root, width=400, height=200)
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Iniciar Evolución", command=self.start_evolution)
        self.start_button.pack()

        self.stop_threshold_label = tk.Label(root, text="Umbral de precisión")
        self.stop_threshold_label.pack()

        self.stop_threshold_entry = tk.Entry(root)
        self.stop_threshold_entry.insert(0, str(STOP_THRESHOLD))  # Valor inicial
        self.stop_threshold_entry.pack()

        self.mutations_label = tk.Label(root, text="Mutaciones Camino 1: 0\nMutaciones Camino 2: 0")
        self.mutations_label.pack()

        self.path1_label = tk.Label(root, text="Camino 1: ")
        self.path1_label.pack()

        self.path2_label = tk.Label(root, text="Camino 2: ")
        self.path2_label.pack()

        self.console_output = tk.Text(root, height=10, width=60)
        self.console_output.pack()

        # Mostrar los colores primarios
        self.primary_colors_label = tk.Label(root, text="Colores Primarios:")
        self.primary_colors_label.pack()

        self.primary_colors_frame = tk.Frame(root)
        self.primary_colors_frame.pack()

        for color_name, rgb in PRIMARY_COLORS.items():
            self.display_primary_color(color_name, rgb)

        # Botón para reiniciar
        self.reset_button = tk.Button(root, text="Reiniciar Evolución", command=self.reset_evolution)
        self.reset_button.pack()

    def display_primary_color(self, color_name, rgb):
        frame = tk.Frame(self.primary_colors_frame)
        frame.pack(side=tk.LEFT, padx=5)

        color_label = tk.Label(frame, text=color_name)
        color_label.pack()

        color_canvas = tk.Canvas(frame, width=50, height=50)
        color_canvas.pack()
        color_canvas.create_rectangle(0, 0, 50, 50, fill=self.rgb_to_hex(rgb))

    def start_evolution(self):
        # Actualizar el valor de STOP_THRESHOLD con el valor ingresado por el usuario
        global STOP_THRESHOLD
        try:
            STOP_THRESHOLD = int(self.stop_threshold_entry.get())
        except ValueError:
            STOP_THRESHOLD = 100  # Valor predeterminado si hay error en la entrada
            self.console_output.insert(tk.END, "Valor de STOP_THRESHOLD inválido. Usando 100 por defecto.\n")

        # Crear dos poblaciones (dos caminos)
        self.population1 = Population(self.target_color)
        self.population2 = Population(self.target_color)
        self.run_evolution()

    def run_evolution(self):
        # Si la evolución ya ha terminado, no continuar
        if self.evolution_complete:
            return

        if self.mutations_path1 < NUM_GENERATIONS and self.mutations_path2 < NUM_GENERATIONS:
            # Evolucionar camino 1
            best_individual_path1 = self.population1.evolve()
            self.mutations_path1 += 1

            # Evolucionar camino 2
            best_individual_path2 = self.population2.evolve()
            self.mutations_path2 += 1

            # Separar los colores con un espacio (1 cm)
            self.canvas.create_rectangle(50, 50, 150, 150, fill=self.rgb_to_hex(best_individual_path1.rgb))
            self.canvas.create_text(100, 25, text="Camino 1", font=("Arial", 12))

            # Espacio de 1 cm (aproximadamente 38px en la mayoría de pantallas)
            self.canvas.create_rectangle(252, 50, 352, 150, fill=self.rgb_to_hex(best_individual_path2.rgb))
            self.canvas.create_text(302, 25, text="Camino 2", font=("Arial", 12))

            # Mostrar historial y mutaciones
            self.update_history()

            # Actualizar etiqueta de mutaciones
            self.mutations_label.config(text=f"Mutaciones Camino 1: {self.mutations_path1}\nMutaciones Camino 2: {self.mutations_path2}")

            # Revisar si alguno de los caminos ha alcanzado el objetivo (color verde)
            if self.is_target_reached(best_individual_path1, camino="C1") or self.is_target_reached(best_individual_path2, camino="C2"):
                self.evolution_complete = True
                self.start_button.config(text="Evolución Completa")
                return
            else:
                # Continuar evolución
                self.root.after(500, self.run_evolution)

    def reset_evolution(self):
        # Reiniciar los parámetros y la interfaz
        self.mutations_path1 = 0
        self.mutations_path2 = 0
        self.evolution_complete = False
        self.console_output.delete(1.0, tk.END)
        self.mutations_label.config(text="Mutaciones Camino 1: 0\nMutaciones Camino 2: 0")
        self.path1_label.config(text="Camino 1: ")
        self.path2_label.config(text="Camino 2: ")
        self.start_button.config(text="Iniciar Evolución")
        self.canvas.delete("all")

    def is_target_reached(self, individual, camino):
        # Calcular la distancia Euclidiana entre el mejor individuo y el color objetivo
        distance = math.sqrt(sum((individual.rgb[i] - self.target_color[i]) ** 2 for i in range(3)))

        # Limitar la distancia a 5 decimales
        distance = round(distance, 5)

        # Mostrar el color actual para depuración en la interfaz gráfica
        message = f"{camino}: Color actual: {individual.rgb}, Distancia: {distance}\n"
        self.console_output.insert(tk.END, message)
        self.console_output.see(tk.END)  # Desplazar automáticamente hacia abajo
        
        return distance < STOP_THRESHOLD

    def update_history(self):
        # Historial de las últimas 5 combinaciones
        path1_text = "Camino 1: " + " -> ".join([self.rgb_to_hex(rgb) for rgb in self.population1.history[-5:]])
        path2_text = "Camino 2: " + " -> ".join([self.rgb_to_hex(rgb) for rgb in self.population2.history[-5:]])
        self.path1_label.config(text=path1_text)
        self.path2_label.config(text=path2_text)

    @staticmethod
    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorEvolutionApp(root)
    root.mainloop()
