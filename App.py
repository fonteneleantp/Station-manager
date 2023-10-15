#Antonio Pereira Fontenele
#OperationalRecord

import customtkinter as ctk
from tkinter import END
from PIL import Image, ImageTk
from time import sleep
import sqlite3
from tkinter import messagebox
import pygetwindow as gw
import threading

posto_habilitado = False


class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("sistema_cadastro.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado!")
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado!")
    def cria_tabela(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Matrícula TEXT NOT NULL,
                Senha TEXT NOT NULL,
                CSenha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconecta_db()
    def cadastrar_usuario(self):
        self.nome_registro = self.nome_registro_entry.get()
        self.matricula_registro = self.matricula_registro_entry.get()
        self.senha_registro = self.senha_registro_entry.get()
        self.csenha_registro = self.csenha_registro_entry.get()

        self.conecta_db()
        self.cursor.execute("""
            INSERT INTO Usuarios (Nome, Matrícula, Senha, CSenha)
            VALUES (?, ?, ?, ?)
        """, (self.nome_registro, self.matricula_registro, self.senha_registro, self.csenha_registro))

        try:
            if (self.nome_registro=="" or self.matricula_registro=="" or self.senha_registro=="" or self.csenha_registro==""):
                messagebox.showerror(title="OperationalRecord", message="Por favor preencher todos os campos")
            elif(len(self.nome_registro) < 10):
                messagebox.showwarning(title="OperationalRecord", message="Favor digite seu nome completo")
            elif(len(self.senha_registro) < 8):
                messagebox.showwarning(title="OperationalRecord", message="Sua senha deve possuir no mínimo 9 dígitos")
            elif(self.senha_registro != self.csenha_registro):
                messagebox.showerror(title="OperationalRecord", message="As senhas digitadas devem ser idênticas")
            else:
                self.conn.commit()
                messagebox.showinfo(title="OperationalRecord", message="Novo usuário cadastrado com sucesso")
        except:
            messagebox.showerror(title="OperationalRecord", message="Erro no processamento do seu cadastro\n Por favor tente novamente")
    def verifica_login(self):
        self.matricula_login = self.matricula_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        #self.limpa_entry_login()

        self.conecta_db()

        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Matrícula = ? AND Senha = ?)""", (self.matricula_login, self.senha_login))

        self.verifica_dados = self.cursor.fetchone() #Percorrendo na tabela Usuarios
        try:
            if(self.matricula_login=="" or self.senha_login==""):
                messagebox.showwarning(title="OperationalRecord", message="Por favor preencher todos os campos")
            elif(self.matricula_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                self.limpa_entry_login()
                self.posto_habilitado = True
                messagebox.showinfo(title="OperationalRecord", message=f"Posto habilitado! Usuário de matrícula {self.matricula_login} operando o posto")
                self.desconecta_db()

        except:
            messagebox.showerror(title="OperationalRecord", message="Usuário não encontrado!\nVerifique os seus dados")
            self.desconecta_db()
    def minimizador(self):
        self.posto_habilitado = posto_habilitado
        while not self.posto_habilitado:
            for j in gw.getAllTitles():
                if j != "OperationalRecord":
                    try:
                        window = gw.getWindowsWithTitle(j)[0]
                        if window.isMaximized:
                            window.minimize()
                    except IndexError:
                        pass
            #   sleep(1)
    """def minimizador(self):
        self.posto_habilitado = posto_habilitado

        while not self.posto_habilitado:
            for janela in gw.getAllTitles():
                if janela != "OperationalRecord": #and "Barra de Tarefas" not in janela:
                    j = gw.getWindowsWithTitle(janela)[0]
                    # Verifique se a janela não está minimizada antes de minimizá-la
                    if not j.isMinimized:
                        j.minimize()
        sleep(1)"""

class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela()
        self.tela_de_login()
        self.cria_tabela()
        minimizador_thread = threading.Thread(target=self.minimizador)
        minimizador_thread.start()
    def configuracoes_da_janela(self):
        #Configurando a janela principal
        self.geometry("700x400")
        self.title("OperationalRecord")
        self.resizable(True, True)
        ctk.set_appearance_mode("Dark")
    def tela_de_login(self):
        #Trabalhando com as imagens
        img = Image.open("Team.png")
        img_resize = img.resize((380, 380))
        img_resize_tk = ImageTk.PhotoImage(img_resize)
        self.lb_img = ctk.CTkLabel(self, text=None, image=img_resize_tk)
        self.lb_img.place(x=0, y=10)
        #Criando a Frame
        self.frame_login = ctk.CTkLabel(self,text=None, width = 330, height=380, fg_color="#323232", corner_radius=8)
        self.frame_login.place(x=360, y=10)
        #Widgets da frame_login
        self.lb_title_login = ctk.CTkLabel(self.frame_login, text="Faça login para habilitar o posto", font=("Century Gothic bold", 14))
        self.lb_title_login.place(x=65, y=20)
        self.matricula_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Matrícula", font=("Century Gothic bold", 16)) #, corner_radius=10
        self.matricula_login_entry.place(x=15, y=50)
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", font=("Century Gothic bold", 16), show="*")
        self.senha_login_entry.place(x=15, y=85)
        self.save_mat_entry = ctk.CTkCheckBox(self.frame_login, text= "Memorizar matrícula", corner_radius=15)
        self.save_mat_entry.place(x=15, y=120) 
        self.bt_iniciar = ctk.CTkButton(self.frame_login, text="INICIAR!", width=300, hover_color="#87bdfd", command=self.verifica_login)
        self.bt_iniciar.place(x=15, y=170)
        self.lb_registro_login = ctk.CTkLabel(self.frame_login, text="Novo usuário:", font=("Century Gothic bold", 15))
        self.lb_registro_login.place(x=15, y=205) 
        self.bt_registro_login = ctk.CTkButton(self.frame_login, text="REGISTRAR", width=205, fg_color="green", hover_color="#090", command=self.tela_de_registro)
        self.bt_registro_login.place(x=110, y=205)     
    def tela_de_registro(self):
        #Remover frame de login
        self.frame_login.place_forget()
        #Criar frame de registro
        self.frame_registro = ctk.CTkLabel(self,text=None, width = 330, height=380, fg_color="#323232", corner_radius=8)
        self.frame_registro.place(x=360, y=10)      
        #Widgets da tela de registro
        self.lb_title_registro = ctk.CTkLabel(self.frame_registro, text="Registre um novo usuário", font=("Century Gothic bold", 14))
        self.lb_title_registro.place(x=85, y=20)
        self.nome_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Nome completo", font=("Century Gothic bold", 16)) #, corner_radius=10
        self.nome_registro_entry.place(x=15, y=50)
        self.matricula_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Nova matrícula", font=("Century Gothic bold", 16))
        self.matricula_registro_entry.place(x=15, y=85)
        self.senha_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Nova senha", font=("Century Gothic bold", 16), show="*")
        self.senha_registro_entry.place(x=15, y=120)
        self.csenha_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Confirmar senha", font=("Century Gothic bold", 16), show="*")
        self.csenha_registro_entry.place(x=15, y=155)
        self.termo_registro = ctk.CTkCheckBox(self.frame_registro, text= "concordo com as políticas de sigilo", corner_radius=15)
        self.termo_registro.place(x=50, y=190)
        self.bt_registro_registro = ctk.CTkButton(self.frame_registro, text="REGISTRAR", width=300, fg_color="green", hover_color="#090", command=self.cadastrar_usuario)
        self.bt_registro_registro.place(x=15, y=225) 
        self.bt_voltar_registro = ctk.CTkButton(self.frame_registro, text="VOLTAR", width=300, hover_color="#87bdfd", command=self.tela_de_login)
        self.bt_voltar_registro.place(x=15, y=260)  
    def limpa_entry_cadastro(self):
        self.nome_registro_entry.delete(0, END)
        self.matricula_registro_entry.delete(0, END)
        self.senha_registro_entry.delete(0, END)
        self.csenha_registro_entry.delete(0, END)  
    def limpa_entry_login(self):
        self.senha_login_entry.delete(0, END)

if __name__=="__main__":
    app = App()
    app.mainloop()
