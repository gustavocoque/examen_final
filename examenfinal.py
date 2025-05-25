import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class SistemaDeporte:
    def __init__(self):
        self.participantes = []

    def registrar_participante(self, nombre, resistencia, fuerza, velocidad):
        dificultad_r = round(random.uniform(1.0, 1.3), 2)
        dificultad_f = round(random.uniform(1.0, 1.3), 2)
        dificultad_v = round(random.uniform(1.0, 1.3), 2)

        ponderado_r = resistencia * dificultad_r
        ponderado_f = fuerza * dificultad_f
        ponderado_v = velocidad * dificultad_v

        suma_ponderada = ponderado_r + ponderado_f + ponderado_v
        suma_dificultad = dificultad_r + dificultad_f + dificultad_v

        puntaje_final = round(suma_ponderada / suma_dificultad)
        estado = "Clasificó" if puntaje_final >= 70 else "No clasificó"

        self.participantes.append({
            "Nombre": nombre,
            "Resistencia": resistencia,
            "Fuerza": fuerza,
            "Velocidad": velocidad,
            "Dificultad Resistencia": dificultad_r,
            "Dificultad Fuerza": dificultad_f,
            "Dificultad Velocidad": dificultad_v,
            "Puntaje Final": puntaje_final,
            "Estado": estado
        })

    def generar_dataframe(self):
        if not self.participantes:
            return pd.DataFrame()
        return pd.DataFrame(self.participantes)

sistema = SistemaDeporte()

def registrar_participante():
    nombre = simpledialog.askstring("Registro", "Nombre del participante:")
    try:
        r = int(simpledialog.askstring("Registro", "Puntaje en resistencia (0-100):"))
        f = int(simpledialog.askstring("Registro", "Puntaje en fuerza (0-100):"))
        v = int(simpledialog.askstring("Registro", "Puntaje en velocidad (0-100):"))
    except:
        messagebox.showerror("Error", "Los puntajes deben ser números enteros")
        return

    if any(p < 0 or p > 100 for p in [r, f, v]):
        messagebox.showerror("Error", "Los puntajes deben estar entre 0 y 100")
        return

    sistema.registrar_participante(nombre, r, f, v)
    messagebox.showinfo("Registro", f"Participante '{nombre}' registrado con éxito")

def mostrar_reporte_general():
    df = sistema.generar_dataframe()
    if df.empty:
        messagebox.showwarning("Advertencia", "No hay participantes registrados")
        return

    print(df) 


    print("\nEstadísticas (describe):")
    print(df.describe())

    promedio = df["Puntaje Final"].mean()
    print(f"\nPuntaje promedio del grupo: {promedio:.2f}")

    plt.figure(figsize=(5, 5))
    df["Estado"].value_counts().plot.pie(autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title("Clasificados vs No Clasificados")
    plt.ylabel("")
    plt.show()

    plt.figure(figsize=(6, 5))
    corr = df[["Resistencia", "Fuerza", "Velocidad"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Matriz de Correlación de Puntajes")
    plt.show()

def mostrar_reporte_individual():
    nombre = simpledialog.askstring("Reporte Individual", "Nombre del participante:")
    df = sistema.generar_dataframe()
    datos = df[df["Nombre"] == nombre]

    if datos.empty:
        messagebox.showerror("Error", f"No se encontró a '{nombre}'")
        return

    p = datos.iloc[0]
    messagebox.showinfo("Reporte", f"Puntaje final: {p['Puntaje Final']}\nEstado: {p['Estado']}")


    plt.figure(figsize=(10, 3))

    plt.subplot(1, 3, 1)
    plt.bar(["Resistencia", "Fuerza", "Velocidad"], [p["Resistencia"], p["Fuerza"], p["Velocidad"]], color='skyblue')
    plt.title("Puntajes")

    plt.subplot(1, 3, 2)
    plt.bar(["Resistencia", "Fuerza", "Velocidad"], 
            [p["Dificultad Resistencia"], p["Dificultad Fuerza"], p["Dificultad Velocidad"]], color='orange')
    plt.title("Dificultades")

    ponderados = [
        p["Resistencia"] * p["Dificultad Resistencia"],
        p["Fuerza"] * p["Dificultad Fuerza"],
        p["Velocidad"] * p["Dificultad Velocidad"]
    ]
    plt.subplot(1, 3, 3)
    plt.bar(["Resistencia", "Fuerza", "Velocidad"], ponderados, color='green')
    plt.title("Puntaje Ponderado")

    plt.tight_layout()
    plt.show()
    

ventana = tk.Tk()
ventana.title("Sistema Deportivo")

tk.Label(ventana, text="Menú Principal", font=("Arial", 16)).pack(pady=10)

tk.Button(ventana, text="1. Registrar participante", command=registrar_participante).pack(fill='x', padx=20, pady=5)
tk.Button(ventana, text="2. Mostrar reporte general", command=mostrar_reporte_general).pack(fill='x', padx=20, pady=5)
tk.Button(ventana, text="3. Mostrar reporte individual", command=mostrar_reporte_individual).pack(fill='x', padx=20, pady=5)
tk.Button(ventana, text="4. Salir", command=ventana.destroy).pack(fill='x', padx=20, pady=10)

ventana.mainloop()
