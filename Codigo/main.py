# Instalando ambiente virtual para instalar a biblioteca
# python -m venv env
# Vamos instalar a biblioteca mysql.connector
# pip install mysql-connector-python

import mysql.connector

# Configurações do Banco de Dados
host = 'localhost'
user = 'root'
password = '1234'
database = 'TRANSACOES_DESAFIO'

try:
    # Conectar ao banco de dados
    conexao = mysql.connector.connect(
        host= host,
        user = user,
        password = password,
        database = database
    )

    # Criar um cursor
    cursor = conexao.cursor()

    # Dados do novo usuário
    novo_usuario = {
        "NomeCompleto": "Fulano de Tal",
        "CPFCNPJ": "12345678901",
        "Email": "fulano@email.com",
        "Senha": "senha123",
        "TipoUsuario": "COMUM"
    }

    # Verificar unicidade de CPF/CNPJ e e-mail
    cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE CPFCNPJ = %s OR Email = %s", (novo_usuario["CPFCNPJ"], novo_usuario["Email"]))
    if cursor.fetchone()[0] > 0:
        print("CPF/CNPJ ou e-mail já cadastrado. Por favor, escolha dados únicos.")
    else:
        # Inserir novo usuário
        cursor.execute("INSERT INTO Usuarios (NomeCompleto, CPFCNPJ, Email, Senha, TipoUsuario) VALUES (%s, %s, %s, %s, %s)",
                    (novo_usuario["NomeCompleto"], novo_usuario["CPFCNPJ"], novo_usuario["Email"], novo_usuario["Senha"], novo_usuario["TipoUsuario"]))
        conexao.commit()
        print("Novo usuário cadastrado com sucesso.")
    
   

    # Fechar conexão
    cursor.close()
    conexao.close()
except mysql.connector.Error as erro:
    print(f"Erro no MySQL: {erro}")

finally:
    # Fechar o cursor e a conexão, mesmo em caso de exceção
    if 'cursor' in locals() and cursor is not None:
        cursor.close()

    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()