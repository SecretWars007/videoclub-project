from typing import Dict, Any, Optional 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch
from app.core.database import get_db_client 

# Clase base para repositorios que implementan CRUD básico y control de concurrencia optimista
class BaseRepository: 
    
    # Inicializa el repositorio con el nombre del índice y el cliente de OpenSearch
    def __init__(self, index_name: str, client: Optional[OpenSearch] = None):
        self.index_name = index_name
        self.client = client or get_db_client()

    # Obtiene un documento por su ID
    def get_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        try: 
            response = self.client.get(index=self.index_name, id=doc_id) 
            doc = response["_source"] # Extraer metadatos de control de concurrencia optimista (OCC)
            doc["_seq_no"] = response.get("_seq_no") 
            doc["_primary_term"] = response.get("_primary_term") 
            return doc 
        except Exception: 
            return None 
    
    # Indexa un documento en OpenSearch
    def index_document(self, doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]: 
        return self.client.index(index=self.index_name, id=doc_id, body=document, refresh=True) 
    
    # Elimina un documento por su ID
    def delete_document(self, doc_id: str) -> bool: 
        try: 
            self.client.delete(index=self.index_name, id=doc_id, refresh=True) 
            return True 
        except Exception: 
            return False
