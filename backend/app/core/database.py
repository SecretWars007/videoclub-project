import os 
from typing import Optional 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch 

# --- SINGLETON PARA CONEXIÓN A OPENSEARCH ---
class OpenSearchClientSingleton:
    """ Patrón Singleton para la gestión de la conexión a OpenSearch. 
        Garantiza una única piscina de conexiones HTTP a través de HAProxy. 
    """ 
    _instance: Optional[OpenSearch] = None
    # Método para obtener la instancia del cliente OpenSearch
    @classmethod 
    def get_instance(cls) -> OpenSearch: 
        if cls._instance is None: 
            opensearch_host = os.getenv("OPENSEARCH_HOST", "http://haproxy:9200") 
            cls._instance = OpenSearch(
                hosts=[opensearch_host], 
                use_ssl=False, 
                verify_certs=False, 
                ssl_show_warn=False, 
                timeout=30, 
                max_retries=3, 
                retry_on_timeout=True
            )
            print(f"🔌 [SINGLETON] Cliente OpenSearch instanciado hacia: {opensearch_host}") 
        return cls._instance 

# Función para obtener la instancia del cliente OpenSearch
def get_db_client() -> OpenSearch:
    return OpenSearchClientSingleton.get_instance()