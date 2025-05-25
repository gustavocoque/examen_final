import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Participante:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntajes = []
        self.dificultades = []
        self.puntaje_final = 0
        self.clasificado = False
    
    def agregar_prueba(self, puntaje, dificultad):
        self.puntajes.append(puntaje)
        self.dificultades.append(dificultad)
    
    def calcular_puntaje_final(self):
        if len(self.puntajes) == 0:
            return 0
        
        suma_puntajes = sum(p * d for p, d in zip(self.puntajes, self.dificultades))
        suma_dificultades = sum(self.dificultades)
        
        self.puntaje_final = round(suma_puntajes / suma_dificultades)
        self.clasificado = self.puntaje_final >= 70
        return self.puntaje_final

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pruebas Deportivas")
        self.root.geometry("500x400")
        
        self.participantes = []
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Sistema de Gestión Deportiva", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(frame, text="1. Registrar participante", command=self.registrar_participante, width=25).pack(pady=5)
        tk.Button(frame, text="2. Mostrar reporte general", command=self.mostrar_reporte_general, width=25).pack(pady=5)
        tk.Button(frame, text="3. Mostrar reporte individual", command=self.mostrar_reporte_individual, width=25).pack(pady=5)
        tk.Button(frame, text="4. Salir", command=self.root.quit, width=25).pack(pady=5)
    
    def registrar_participante(self):
        nombre = simpledialog.askstring("Registro", "Ingrese nombre del participante:")
        if not nombre:
            return
        
        participante = Participante(nombre)
        
        pruebas = ["resistencia", "fuerza", "velocidad"]
        for prueba in pruebas:
            while True:
                try:
                    puntaje = simpledialog.askinteger(prueba, f"Ingrese puntaje de {prueba} (0-100):")
                    if puntaje is None:
                        return
                    if 0 <= puntaje <= 100:
                        break
                    else:
                        messagebox.showerror("Error", "Puntaje debe estar entre 0 y 100")
                except:
                    messagebox.showerror("Error", "Ingrese un número válido")
            
            dificultad = round(random.uniform(1.0, 1.3), 1)
            participante.agregar_prueba(puntaje, dificultad)
        
        participante.calcular_puntaje_final()
        self.participantes.append(participante)
        messagebox.showinfo("Éxito", f"Participante registrado!\nPuntaje final: {participante.puntaje_final}\nClasificado: {'Sí' if participante.clasificado else 'No'}")
    
    def mostrar_reporte_general(self):
        if not self.participantes:
            messagebox.showerror("Error", "No hay participantes registrados")
            return
        
        # Crear ventana para el reporte
        reporte_window = tk.Toplevel(self.root)
        reporte_window.title("Reporte General")
        reporte_window.geometry("800x600")
        
        # Datos para el reporte
        nombres = [p.nombre for p in self.participantes]
        puntajes = [p.puntaje_final for p in self.participantes]
        clasificados = ["Clasificó" if p.clasificado else "No clasificó" for p in self.participantes]
        
        # Crear DataFrame para estadísticas
        df = pd.DataFrame({
            'Nombre': nombres,
            'Puntaje': puntajes,
            'Estado': clasificados
        })
        
        # Mostrar datos básicos
        texto = "=== Reporte General ===\n\n"
        for p in self.participantes:
            texto += f"{p.nombre}: Puntaje {p.puntaje_final} - {p.clasificado}\n"
        
        texto += f"\nPuntaje promedio: {round(np.mean(puntajes), 2)}"
        
        tk.Label(reporte_window, text=texto, justify=tk.LEFT).pack(pady=10)
        
        # Estadísticas con pandas
        tk.Label(reporte_window, text="\nEstadísticas descriptivas:").pack()
        descripcion = df['Puntaje'].describe().to_string()
        tk.Label(reporte_window, text=descripcion).pack()
        
        # Gráfico de torta
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        clasificados_count = df[df['Estado'] == 'Clasificó'].shape[0]
        no_clasificados_count = df.shape[0] - clasificados_count
        ax1.pie([clasificados_count, no_clasificados_count], 
                labels=['Clasificados', 'No clasificados'], 
                autopct='%1.1f%%')
        ax1.set_title('Clasificación de participantes')
        
        canvas1 = FigureCanvasTkAgg(fig1, master=reporte_window)
        canvas1.draw()
        canvas1.get_tk_widget().pack()
        
        # Matriz de correlación (si hubiera más datos)
        if len(self.participantes) > 1:
            try:
                df_pruebas = pd.DataFrame({
                    'Resistencia': [p.puntajes[0] for p in self.participantes],
                    'Fuerza': [p.puntajes[1] for p in self.participantes],
                    'Velocidad': [p.puntajes[2] for p in self.participantes]
                })
                
                fig2, ax2 = plt.subplots(figsize=(5, 3))
                sns.heatmap(df_pruebas.corr(), annot=True, ax=ax2)
                ax2.set_title('Correlación entre pruebas')
                
                canvas2 = FigureCanvasTkAgg(fig2, master=reporte_window)
                canvas2.draw()
                canvas2.get_tk_widget().pack()
            except:
                pass
    
    def mostrar_reporte_individual(self):
        if not self.participantes:
            messagebox.showerror("Error", "No hay participantes registrados")
            return
        
        nombre = simpledialog.askstring("Reporte Individual", "Ingrese nombre del participante:")
        if not nombre:
            return
        
        participante = None
        for p in self.participantes:
            if p.nombre.lower() == nombre.lower():
                participante = p
                break
        
        if not participante:
            messagebox.showerror("Error", "Participante no encontrado")
            return
        
        # Crear ventana para el reporte individual
        ind_window = tk.Toplevel(self.root)
        ind_window.title(f"Reporte de {participante.nombre}")
        ind_window.geometry("800x800")
        
        # Mostrar datos básicos
        texto = f"=== Reporte de {participante.nombre} ===\n\n"
        texto += f"Puntaje final: {participante.puntaje_final}\n"
        texto += f"Estado: {'Clasificó' if participante.clasificado else 'No clasificó'}\n\n"
        
        pruebas = ["Resistencia", "Fuerza", "Velocidad"]
        texto += "Resultados por prueba:\n"
        for i in range(3):
            texto += f"{pruebas[i]}: Puntaje={participante.puntajes[i]}, Dificultad={participante.dificultades[i]}, Ponderado={round(participante.puntajes[i]*participante.dificultades[i], 1)}\n"
        
        tk.Label(ind_window, text=texto, justify=tk.LEFT).pack(pady=10)
        
        # Gráficos
        fig, axs = plt.subplots(3, 1, figsize=(6, 12))
        
        # Histograma de puntajes por prueba
        axs[0].bar(pruebas, participante.puntajes, color='blue')
        axs[0].set_title('Puntajes por prueba')
        axs[0].set_ylim(0, 100)
        
        # Histograma de dificultades
        axs[1].bar(pruebas, participante.dificultades, color='green')
        axs[1].set_title('Dificultad por prueba')
        axs[1].set_ylim(1.0, 1.3)
        
        # Histograma de puntajes ponderados
        ponderados = [p*d for p, d in zip(participante.puntajes, participante.dificultades)]
        axs[2].bar(pruebas, ponderados, color='red')
        axs[2].set_title('Puntajes ponderados por prueba')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=ind_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()