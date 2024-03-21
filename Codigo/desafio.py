import mysql.connector
import requests

# Configurações do Banco de Dados
host = 'localhost'
user = 'root'
password = '1234'
database = 'TRANSACOES_DESAFIO'

try:
    # Conectar ao banco de dados
    with mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
    ) as conexao:
        # Criar um cursor
        with conexao.cursor() as cursor:

            # Exemplo de transferência entre usuários
            id_usuario_remetente = 2  # Supondo que o usuário é o remetente 
            id_usuario_destinatario = 1  # Supondo que o usuário 2 é o destinatário
            valor_transferencia = 50.00

            # Iniciar transação
            conexao.start_transaction()


            try:
                # Verificar se a conta remetente é lojista
                cursor.execute("SELECT TipoUsuario FROM Usuarios WHERE IDUSUARIO = %s", (id_usuario_remetente,))
                tipo_usuario_remetente = cursor.fetchone()[0]

                if tipo_usuario_remetente == 'LOJISTA':
                    print("Conta remetente é lojista. Transferência não autorizada para envio.")
                else:
                    # Transferência autorizada, realizar operação
                    cursor.execute("UPDATE Carteiras SET Saldo = Saldo - %s WHERE ID_USUARIO = %s", (valor_transferencia, id_usuario_remetente))
                    cursor.execute("UPDATE Carteiras SET Saldo = Saldo + %s WHERE ID_USUARIO = %s", (valor_transferencia, id_usuario_destinatario))

                    # Registrar a transferência na tabela Transferencias
                    cursor.execute("INSERT INTO Transferencias (ID_USUARIO_REMETENTE, ID_USUARIO_DESTINATARIO, Valor, Status) VALUES (%s, %s, %s, %s)",
                                (id_usuario_remetente, id_usuario_destinatario, valor_transferencia, "CONCLUIDA"))
                    notificacao1 = requests.get("https://run.mocky.io/v3/5794d450-d2e2-4412-8131-73d0293ac1cc").json()
                    if 'message' in notificacao1 and (notificacao1['message'] == 'Autorizado' or notificacao1['message'].lower() == 'autorizado'):
                        # Enviar notificação (mock)
                        notificacao2 = requests.get("https://run.mocky.io/v3/54dc2cf1-3add-45b5-b5a9-6bf7e7f1f4a6").json()
                        print(notificacao2)
                        if 'message' in notificacao2 and (notificacao2['message'] == True or notificacao2['message'].lower() == 'true'):
                            # Registrar notificação na tabela Notificacoes
                            cursor.execute("INSERT INTO Notificacoes (ID_USUARIO, Tipo, Status) VALUES (%s, %s, %s)",
                                        (id_usuario_destinatario, "TRANSFERENCIA", "ENVIADA"))
                        # Confirmar a transação
                        conexao.commit()
                        print("Transferência realizada com sucesso.")
                    else:
                        print("Transferência não autorizada.")
                    
            except Exception as e:
                # Se ocorrer algum erro, reverter a transação
                print(f"Erro na transferência: {e}")
                conexao.rollback()

            finally:
                # Fechar conexão
                cursor.close()
                conexao.close()

except mysql.connector.Error as erro:
    print(f"Erro no MySQL: {erro}")
