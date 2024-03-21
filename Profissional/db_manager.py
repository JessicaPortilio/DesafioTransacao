import mysql.connector

# Gerenciador de banco de dados
class DatabaseManager:
    def __init__(self, config):
        """
        Inicializa a conexão com o banco de dados.

        Parameters:
        - host: string, endereço do servidor do banco de dados.
        - user: string, nome de usuário para autenticação.
        - password: string, senha para autenticação.
        - database: string, nome do banco de dados.

        Raises:
        - mysql.connector.Error: Em caso de falha na conexão.
        """
        
        try:
            self.connection = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_DATABASE
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise  # Propaga a exceção para notificar o chamador


    def execute_query(self, query, params=None):
        """
        Executa uma query no banco de dados.

        Parameters:
        - query: string, a query SQL a ser executada.
        - params: tuple, parâmetros para substituir placeholders na query.

        Raises:
        - mysql.connector.Error: Em caso de falha ao executar a query.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except mysql.connector.Error as e:
            print(f"Erro ao executar a query: {e}")
            raise

    def fetch_one(self):
        """
        Recupera a próxima linha do resultado da última query.

        Returns:
        - tuple: Uma tupla representando a próxima linha do resultado.

        Raises:
        - mysql.connector.Error: Em caso de falha ao recuperar dados.
        """
        try:
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Erro ao recuperar dados: {e}")
            raise

    def commit(self):
        """
        Realiza o commit da transação.

        Raises:
        - mysql.connector.Error: Em caso de falha ao fazer commit.
        """
        try:
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Erro ao fazer commit: {e}")
            raise

    def rollback(self):
        """
        Reverte a transação.

        Raises:
        - mysql.connector.Error: Em caso de falha ao fazer rollback.
        """
        try:
            self.connection.rollback()
        except mysql.connector.Error as e:
            print(f"Erro ao fazer rollback: {e}")
            raise

    def close(self):
        """
        Fecha a conexão com o banco de dados.

        Raises:
        - mysql.connector.Error: Em caso de falha ao fechar a conexão.
        """
        try:
            self.cursor.close()
            self.connection.close()
        except mysql.connector.Error as e:
            print(f"Erro ao fechar conexão: {e}")
            raise
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            # Se ocorrer uma exceção, faz rollback
            self.rollback()
        self.close()