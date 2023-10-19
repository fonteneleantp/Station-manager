# Station Manager

## Tutorial interface

![TutorialFontenele](https://github.com/fonteneleantp/operational-record/assets/140100514/874ec3db-5949-468d-8e44-40312c253daa)

## Sobre o projeto
Projeto desenolvido para aplicação na indústria onde cada posto conta com um operador para exercê-lo. O operador que atua em cada posto precisa estar habilitado, isto é, treinado para exercê-lo pelo time de engenharia. 
O Station Manager atua como Poca Yoke garantindo que somente operadores devidamente habilitados possam atuar. 

## Funcionalidades (registro)
Quando o operador é treinado pelo time de engenharia e formalmente habilitado, o resposável da engenharia digita a senha específica e clica em registrar, abrindo assim a interface de registro de novos usuários.
Na tela de registro o operador terá de digitar seu nome completo, sua matrícula, escolher uma senha de 8 dígitos e confirmá-la, ao concordar com as políticas de privacidade ele poderá se registrar como novo usuário.
Os dados registrados são armazenados num banco de dados desenvolvido em SQL e podem ser verificados através do DB Browser (SQLCipher):

![image](https://github.com/fonteneleantp/operational-record/assets/140100514/ab61b1f2-ba01-48c6-b36f-7959e799db78)

## Funcionalidades (Log)
Quando o sistema é aberto ele força o minimizar de toda e qualquer aba menos ele próprio, garantindo que o posso só possa ser exercido com normalidade caso o operador faça login.
No momento em que um operadordor faz login ele volta a poder atuar no posto. E é registrado um Log de que o usuário de matrícula específica fez login, bem como será registrado também caso ele clique em desconectar:

![image](https://github.com/fonteneleantp/operational-record/assets/140100514/396b0cf1-eed1-4ef4-ba59-6a65144bb390)

## Tecnologia usada
- Python
- SQL

## Bilbiotecas
- GetWindowsVersion
- Customtkinter
- Pillow
- SQLite
- Pygetwindow
- Threading
- Os
- DateTime

## Autor
Antonio Pereira Fontenele  
https://www.linkedin.com/in/antonio-fontenele-7555b7179/
