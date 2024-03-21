
import requests

class TransferManager:
    def __init__(self, external_service_url):
        self.external_service_url = external_service_url

    # @staticmethod em Python é usado para declarar métodos estáticos em uma classe, 
    # pertencendo à classe em vez de uma instância específica, 
    # sem acesso aos atributos de instância ou a capacidade de modificar o estado da instância
    @staticmethod
    def authorize_transfer(external_service_url):
        try:
            # Realiza a solicitação para a API externa
            response = requests.get(external_service_url)
            
            # Verifica se a solicitação foi bem-sucedida
            response.raise_for_status()

            # Processa os dados da resposta JSON
            response_data = response.json()

            # Verifica se a transferência está autorizada
            if 'message' in response_data and response_data['message'].lower() == 'autorizado':
                return True
            else:
                return False

        except requests.exceptions.RequestException as req_error:
            print(f"Erro na solicitação HTTP para {external_service_url}: {req_error}")
            raise
        
        except Exception as e:
            print(f"Erro ao processar resposta da API externa: {e}")
            raise