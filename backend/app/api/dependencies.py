from fastapi import Depends 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch
from app.core.database import get_db_client
from app.core.unit_of_work import UnitOfWork 

# Inyección de dependencia para el cliente Singleton de OpenSearch
def get_opensearch_db() -> OpenSearch: 
    """Inyección de dependencia para el cliente Singleton de OpenSearch."""
    return get_db_client() 
    
# Inyección de dependencia para la unidad de trabajo (Unit of Work)
def get_uow(client: OpenSearch = Depends(get_opensearch_db)) -> UnitOfWork:
    """Inyección de dependencia para la unidad de trabajo (Unit of Work)."""
    return UnitOfWork(client=client)