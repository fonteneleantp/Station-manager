import sqlite3
import customtkinter as ctk
from tkinter import Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import matplotlib.pyplot as plt

class DataWarehouseViewer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Warehouse Viewer")
        self.geometry("300x200")
        self.configure(bg="#1e1e1e")
        self.create_widgets()
        self.plot_data()

    def create_widgets(self):
        # Create a button to generate the report
        self.btn_generate_report = ctk.CTkButton(self, text="Gerar Relatório de Tempo de Login", command=self.plot_data)
        self.btn_generate_report.pack(pady=20)
        
    def plot_data(self):
        # Connect to the database and fetch the data
        conn = sqlite3.connect("sistema_cadastro.db")
        cursor = conn.cursor()

        # SQL query to fetch login and logout times
        cursor.execute("""
            SELECT Matricula, 
                   Tipo, 
                   DataHora
            FROM DataWarehouse
            WHERE Tipo IN ('Login', 'Logout')
            ORDER BY Matricula, DataHora
        """)

        rows = cursor.fetchall()
        conn.close()

        # Process the data to calculate login durations
        usuarios = []
        duracoes = []

        login_times = {}
        for row in rows:
            matricula = row[0]
            tipo = row[1]
            # Substituir qualquer travessão ou hífen por um único hífen
            data_str = row[2].replace("–", "-").replace("—", "-")
            data_hora = datetime.datetime.strptime(data_str, "%H:%M - %d/%m/%Y")




            if tipo == 'Login':
                login_times[matricula] = data_hora
            elif tipo == 'Logout' and matricula in login_times:
                login_time = login_times.pop(matricula)
                duration = (data_hora - login_time).total_seconds() / 3600  # Convert to hours
                if matricula in usuarios:
                    index = usuarios.index(matricula)
                    duracoes[index] += duration
                else:
                    usuarios.append(matricula)
                    duracoes.append(duration)

        # Create a matplotlib figure and axis
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Plot the data
        ax.bar(usuarios, duracoes, color='skyblue')
        ax.set_xlabel('Matrícula')
        ax.set_ylabel('Tempo de Login (horas)')
        ax.set_title('Tempo de Login por Usuário')
        ax.set_xticklabels(usuarios, rotation=45, ha='right')

        # Display the plot in a tkinter window
        self.plot_window = Toplevel(self)
        self.plot_window.title("Gráfico de Tempo de Login")
        self.plot_window.geometry("800x600")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
    app = DataWarehouseViewer()
    app.mainloop()


