def verifica_login(self):
    self.matricula_login = self.matricula_login_entry.get()
    self.senha_login = self.senha_login_entry.get()

    self.conecta_db()

    try:
        # Modificando para fetchall para obter todos os resultados
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Matrícula = ? AND Senha = ?)""", (self.matricula_login, self.senha_login))
        self.verifica_dados = self.cursor.fetchall()  # Modificado para fetchall

        if not self.matricula_login or not self.senha_login:
            messagebox.showwarning(title="Station Manager", message="Por favor preencher todos os campos")
        elif any((self.matricula_login, self.senha_login) in row for row in self.verifica_dados):
            # Utilizando a função any para verificar se os dados estão presentes em alguma linha
            self.limpa_entry_login()
            self.posto_habilitado = True
            # Registrando Log de entrada
            self.agora = datetime.datetime.now()
            self.data_hora = self.agora.strftime("%H:%M – %d/%m/%Y")
            with open(log_file_name, 'a') as log_file:
                log_file.write(f"MACHINE, {self.data_hora}: Usuário de matrícula {self.matricula_login} fez login.\n")
            # Finalizando Log
            messagebox.showinfo(title="Station Manager", message=f"Posto habilitado! Usuário de matrícula {self.matricula_login} operando o posto")
            self.desconecta_db()
            self.maximizador()
        else:
            messagebox.showerror(title="Station Manager", message="Usuário não encontrado!\nVerifique os seus dados")
            print(f"Matrícula: {self.matricula_login}")
            print(f"Senha: {self.senha_login}")
            print(f"Verifica Dados: {self.verifica_dados}")
            self.desconecta_db()

    except sqlite3.Error as sqlite_error:
        messagebox.showerror(title="Station Manager", message=f"Erro SQLite: {str(sqlite_error)}")
        self.desconecta_db()

    except Exception as general_error:
        messagebox.showerror(title="Station Manager", message=f"Erro inesperado: {str(general_error)}")
        self.desconecta_db()
