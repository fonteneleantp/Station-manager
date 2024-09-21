#Antonio Pereira Fontenele
#Station Manager

from sys import getwindowsversion
import customtkinter as ctk
from tkinter import END
from PIL import Image, ImageTk
from time import sleep
import sqlite3
from tkinter import messagebox
import pygetwindow as gw
import threading
import os
import datetime

posto_habilitado = False
log_file_name = "Station Manager Log"
#teste

class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("sistema_cadastro.db")
        self.cursor = self.conn.cursor()
        #print("Banco de dados conectado!")
    def desconecta_db(self):
        self.conn.close()
        #print("Banco de dados desconectado!")
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
        #print("Tabela criada com sucesso!")
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
            if (len(self.nome_registro)==0 or len(self.matricula_registro)==0 or len(self.senha_registro)==0 or len(self.csenha_registro)==0):
                messagebox.showerror(title="Station Manager", message="Por favor preencher todos os campos")
            elif(len(self.nome_registro) < 10):
                messagebox.showwarning(title="Station Manager", message="Favor digite seu nome completo")
            elif(len(self.senha_registro) < 8 or len(self.senha_registro) > 8):
                messagebox.showwarning(title="Station Manager", message="Sua senha deve possuir exatos 8 dígitos")
            elif(self.senha_registro != self.csenha_registro):
                messagebox.showerror(title="Station Manager", message="As senhas digitadas devem ser idênticas")
            else:
                self.conn.commit()
                self.tela_de_login()
                messagebox.showinfo(title="Station Manager", message=f"Novo usuário cadastrado com sucesso, usuário de matrícula {self.matricula_registro} Habilitado para atuar neste posto")
        except:
            messagebox.showerror(title="Station Manager", message="Erro no processamento do seu cadastro\n Por favor tente novamente")
    def verifica_login(self):
        self.matricula_login = self.matricula_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        #self.limpa_entry_login()
        self.conecta_db()
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Matrícula = ? AND Senha = ?)""", (self.matricula_login, self.senha_login))
        self.verifica_dados = self.cursor.fetchone() #Percorrendo na tabela Usuarios
        try:
            if(self.matricula_login=="" or self.senha_login==""):
                messagebox.showwarning(title="Station Manager", message="Por favor preencher todos os campos")
            elif(self.matricula_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                self.limpa_entry_login()
                self.posto_habilitado = True
                #Registrando Log de entrada
                self.agora = datetime.datetime.now()
                self.data_hora = self.agora.strftime("%H:%M – %d/%m/%Y")
                with open(log_file_name, 'a') as log_file:
                    log_file.write(f"MACHINE, {self.data_hora}: Usuário de matrícula {self.matricula_login} fez login.\n")
                #Finalizando Log
                messagebox.showinfo(title="Station Manager", message=f"Posto habilitado! Usuário de matrícula {self.matricula_login} operando o posto")
                self.desconecta_db()
                self.maximizador()
        except:
            messagebox.showerror(title="Station Manager", message="Usuário não encontrado!\nVerifique os seus dados")
            self.desconecta_db()
    def verifica_engenharia(self):
        self.senha_engenharia = self.senha_entry_engenharia.get()
        if (self.senha_engenharia == ""):
            messagebox.showwarning(title="Station Manager", message="Senha em branco")
        elif (self.senha_engenharia != "EngHarmanRegis"):
            messagebox.showerror(title="Station Manager", message="Senha incorreta")
        elif (self.senha_engenharia == "EngHarmanRegis"):
            self.frame_login.place_forget()
            #self.frame_engenharia.place_forget()
            self.tela_de_registro()
    def minimizador(self):
        self.posto_habilitado = posto_habilitado
        while not self.posto_habilitado:
            for j in gw.getAllTitles():
                if j != "Station Manager":
                    try:
                        windows = gw.getWindowsWithTitle(j)
                        if windows:
                            window = windows[0]
                            if window.isMaximized: #Se estiver maximizado (Não inclui programas nativos do windows)
                                window.minimize()
                            elif window.title == "brmafa":
                                window.minimize()
                            elif window.title == "HB-SCAPE Framework V4.4.67 - Workspace":
                                window.minimize()
                            elif window.title == "Site de comunicação":
                                window.minimize()
                            elif window.title == "Início":
                                window.minimize()
                            elif window.title == "Sem título":
                                window.minimize()
                            elif window.title == "Webex":
                                window.minimize()
                            elif window.title == "HB-SCAPE Framework V4.4.67 - Start Center":
                                window.minimize()
                    except Exception as e:
                        pass
    def maximizador(self):

        nome_janela = "Sem título"
        janelas = gw.getWindowsWithTitle(nome_janela)
        if janelas:
            janela = janelas[0]
            if not janela.isMaximized:
                janela.maximize()   
    def desconecta_usuario(self):
                # Atualize o estado do usuário para desconectado
        self.posto_habilitado = False
        #Registrando Log de entrada
        self.agora = datetime.datetime.now()
        self.data_hora = self.agora.strftime("%H:%M – %d/%m/%Y")
        with open(log_file_name, 'a') as log_file:
            log_file.write(f"MACHINE, {self.data_hora}: Usuário de matrícula {self.matricula_login} se desconectou do posto.\n")
        #Finalizando Log
        messagebox.showinfo(title="Station Manager", message=f"Usuário de matrícula {self.matricula_login} desconectado!")
        minimizador_thread = threading.Thread(target=self.minimizador)
        minimizador_thread.start()
    def politica_de_privacidade(self):
        self.politica = ctk.CTkInputDialog (text="Ao concordar com as políticas de privacidade, você assume total responsabilidade por manter a confidencialidade de sua senha não a compartilhando com outros funcionários. O registro de novos usuários é feito uma vez que o operador foi treinado e, por tanto, está habilidado para atuar neste posto, cada registro de conta está vinculado a matrícula do funcionário para uso não-compartilhado. Cada conta está vinculada ao posto em que foi registrada, favor usar a mesma senha em todos os postos.\nPara poresseguir digite 'Concordo'", title="Station Manager")
        self.texto_politica = self.politica.get_input()
        if (self.texto_politica == "Concordo"):
            #Dar um jeito de acionar o botão da política. PENDENTE
            pass
    def station_manager_log(self):
        if not os.path.isfile(log_file_name):
            with open(log_file_name, 'w') as log_file:
                log_file.write("Station Manager Log: ")
        pass
class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela()
        self.tela_de_login()
        self.cria_tabela()
        self.station_manager_log()
        minimizador_thread = threading.Thread(target=self.minimizador)
        minimizador_thread.start()
    def configuracoes_da_janela(self):
        #Configurando a janela principal
        #self.geometry("700x400")
        self.attributes("-fullscreen", True)
        #-alpha, -transparentcolor, -disabled, -fullscreen, -toolwindow, or -topmost
        self.title("Station Manager")
        self.resizable(True, True)
        ctk.set_appearance_mode("Dark")
    def tela_de_login(self):
        try:
            self.frame_registro.place_forget()
        except:
            pass
                #Criando aS FrameS
        self.frame_centro = ctk.CTkLabel(self,text=None, width = 700, height=400, fg_color="#1e1e1e", corner_radius=8)
        self.frame_centro.place(relx=0.32, rely=0.32) 
        #Trabalhando com as imagens
        img = Image.open("harman3.png")
        img_resize = img.resize((270, 180))
        img_resize_tk = ImageTk.PhotoImage(img_resize)
        self.lb_img = ctk.CTkLabel(self.frame_centro, text=None, image=img_resize_tk)
        self.lb_img.place(x=48, y=105)
        #Imagem Fontenele
        imgf = Image.open("FonteneleBack.png")
        imgf_resize = imgf.resize((300, 200))
        imgf_resize_tk = ImageTk.PhotoImage(imgf_resize)
        self.lb_imgf = ctk.CTkLabel(self, text=None, image=imgf_resize_tk)
        self.lb_imgf.place(relx=0.86, rely=0.86)
        #Frame de Login
        self.frame_login = ctk.CTkLabel(self.frame_centro,text=None, width = 330, height=380, fg_color="#323232", corner_radius=8)
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
        self.bt_iniciar = ctk.CTkButton(self.frame_login, text="INICIAR", width=300, fg_color="green", hover_color="#090", command=self.verifica_login)
        self.bt_iniciar.place(x=15, y=165)
        self.bt_desconectar = ctk.CTkButton(self.frame_login, text="DESCONECTAR", width=300,fg_color= "#b80000", hover_color="#cc0a0a", command=self.desconecta_usuario)
        self.bt_desconectar.place(x=15, y=200)
        """self.lb_registro_login = ctk.CTkLabel(self.frame_login, text="Novo usuário:", font=("Century Gothic bold", 15))
        self.lb_registro_login.place(x=15, y=235) 
        self.bt_registro_login = ctk.CTkButton(self.frame_login, text="REGISTRAR", width=205, hover_color="#337ecd", command=self.senha_engenharia)
        self.bt_registro_login.place(x=110, y=235)""" 
        self.frame_engenharia = ctk.CTkLabel(self.frame_login,text=None, width = 300, height=95, fg_color="#1e1e1e", corner_radius=8)
        self.frame_engenharia.place(x=15, y=275)
        #self.frame_engenharia.place(x=570, y=810)
        #self.frame_engenharia.place(x=10, y=10)
        self.lb_title_engenharia = ctk.CTkLabel(self.frame_engenharia, text="Cadastro de novo usuários", font=("Century Gothic bold", 14))
        self.lb_title_engenharia.place(x=65, y=0) 
        self.senha_entry_engenharia = ctk.CTkEntry(self.frame_engenharia, width=280, placeholder_text="Senha da engenharia", font=("Century Gothic bold", 16), show ="*") #, corner_radius=10
        self.senha_entry_engenharia.place(x=10, y=23)
        self.bt_engenharia = ctk.CTkButton(self.frame_engenharia, text="REGISTRAR", width=280, hover_color="#337ecd", command=self.verifica_engenharia)
        self.bt_engenharia.place(x=10, y=55)       
    def senha_engenharia(self):
        """self.frame_engenharia = ctk.CTkLabel(self.frame_login,text=None, width = 300, height=95, fg_color="#1e1e1e", corner_radius=8)
        self.frame_engenharia.place(x=15, y=275)
        #self.frame_engenharia.place(x=570, y=810)
        #self.frame_engenharia.place(x=10, y=10)
        self.lb_title_engenharia = ctk.CTkLabel(self.frame_engenharia, text="Digite a senha da engenharia", font=("Century Gothic bold", 14))
        self.lb_title_engenharia.place(x=50, y=0) 
        self.senha_entry_engenharia = ctk.CTkEntry(self.frame_engenharia, width=280, placeholder_text="Senha", font=("Century Gothic bold", 16), show ="*") #, corner_radius=10
        self.senha_entry_engenharia.place(x=10, y=23)
        self.bt_engenharia = ctk.CTkButton(self.frame_engenharia, text="AVANÇAR", width=280, hover_color="#337ecd", command=self.verifica_engenharia)
        self.bt_engenharia.place(x=10, y=55)"""
        pass
    def tela_de_registro(self):
        #self.concorda_privacidade == False
        #Remover frame de login
        self.frame_login.place_forget()
        #Criar frame de registro
        self.frame_registro = ctk.CTkLabel(self.frame_centro,text=None, width = 330, height=380, fg_color="#323232", corner_radius=8)
        self.frame_registro.place(x=360, y=10)      
        #Widgets da tela de registro
        self.lb_title_registro = ctk.CTkLabel(self.frame_registro, text="Registre um novo usuário", font=("Century Gothic bold", 14))
        self.lb_title_registro.place(x=85, y=20)
        self.nome_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Nome completo", font=("Century Gothic bold", 16)) #, corner_radius=10
        self.nome_registro_entry.place(x=15, y=50)
        self.matricula_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Sua matrícula", font=("Century Gothic bold", 16))
        self.matricula_registro_entry.place(x=15, y=85)
        self.senha_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Sua senha", font=("Century Gothic bold", 16), show="*")
        self.senha_registro_entry.place(x=15, y=120)
        self.csenha_registro_entry = ctk.CTkEntry(self.frame_registro, width=300, placeholder_text="Confirmar senha", font=("Century Gothic bold", 16), show="*")
        self.csenha_registro_entry.place(x=15, y=155)
        self.termo_registro = ctk.CTkCheckBox(self.frame_registro, text= "Concordo com as políticas de privacidade", command=self.politica_de_privacidade, corner_radius=15)
        self.termo_registro.place(x=30, y=190)
        self.bt_registro_registro = ctk.CTkButton(self.frame_registro, text="REGISTRAR", width=300, fg_color="green", hover_color="#090", command=self.cadastrar_usuario)
        self.bt_registro_registro.place(x=15, y=225) 
        self.bt_voltar_registro = ctk.CTkButton(self.frame_registro, text="VOLTAR", width=300, hover_color="#337ecd", command=self.tela_de_login)
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
