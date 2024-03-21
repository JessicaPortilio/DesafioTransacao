from db_manager import DatabaseManager
from transfer_manager import TransferManager
from config import Config

import mysql.connector
import requests



try:
    # Usando a classe de configuração
    config = Config()

    # Conectar ao banco de dados
    with DatabaseManager(config) as db_manager:
        # Exemplo de transferência entre usuários
        id_usuario_remetente = 2  # Supondo que o usuário é o remetente
        id_usuario_destinatario = 1  # Supondo que o usuário 2 é o destinatário
        valor_transferencia = 1000.00

        # Iniciar transação
        db_manager.execute_query("START TRANSACTION")

        try:
            # Verificar se a conta remetente é lojista
            db_manager.execute_query("SELECT TipoUsuario FROM Usuarios WHERE IDUSUARIO = %s", (id_usuario_remetente,))
            tipo_usuario_remetente = db_manager.fetch_one()[0]

            if tipo_usuario_remetente == 'LOJISTA':
                print("Conta remetente é lojista. Transferência não autorizada para envio.")
            else:
                print('Entrei')
                db_manager.execute_query("SELECT SALDO FROM CARTEIRAS WHERE ID_USUARIO = %s", (id_usuario_remetente,))
                saldo = db_manager.fetch_one()[0]
                print(saldo)
                if saldo >= valor_transferencia:
                    # Transferência autorizada, realizar operação
                    db_manager.execute_query("UPDATE Carteiras SET Saldo = Saldo - %s WHERE ID_USUARIO = %s", (valor_transferencia, id_usuario_remetente))
                    db_manager.execute_query("UPDATE Carteiras SET Saldo = Saldo + %s WHERE ID_USUARIO = %s", (valor_transferencia, id_usuario_destinatario))

                    # Registrar a transferência na tabela Transferencias
                    db_manager.execute_query("INSERT INTO Transferencias (ID_USUARIO_REMETENTE, ID_USUARIO_DESTINATARIO, Valor, Status) VALUES (%s, %s, %s, %s)",
                                (id_usuario_remetente, id_usuario_destinatario, valor_transferencia, "CONCLUIDA"))

                    # Verificar autorização externa
                    if TransferManager.authorize_transfer(config.EXTERNAL_SERVICE_URL):
                        # Enviar notificação (mock)
                        notificacao = requests.get("https://run.mocky.io/v3/54dc2cf1-3add-45b5-b5a9-6bf7e7f1f4a6").json()
                        print(notificacao)
                        if 'message' in notificacao and (notificacao['message'] == True or notificacao['message'].lower() == 'true'):
                            # Registrar notificação na tabela Notificacoes
                            db_manager.execute_query("INSERT INTO Notificacoes (ID_USUARIO, Tipo, Status) VALUES (%s, %s, %s)",
                                    (id_usuario_destinatario, "TRANSFERENCIA", "ENVIADA"))

                        # Confirmar a transação
                        db_manager.commit()
                        print("Transferência realizada com sucesso.")
                    else:
                        print("Transferência não autorizada.")
                else:
                     print("Saldo insuficiente!")

        except Exception as e:
            # Se ocorrer algum erro, reverter a transação
            print(f"Erro na transferência: {e}")
            db_manager.rollback()

        finally:
            # Fechar conexão
            db_manager.close()

except mysql.connector.Error as erro:
    print(f"Erro no MySQL ao conectar: {erro}")
    raise  # Propaga a exceção para notificar o chamador
