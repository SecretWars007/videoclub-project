from typing import List, Callable 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch
from app.core.database import get_db_client

# Unidad de trabajo para coordinar operaciones mutantes NoSQL multi-índice con soporte de transacciones compensatorias (Rollback manual).
class UnitOfWork: 
    
    # Inicializa la unidad de trabajo con una instancia del cliente OpenSearch.
    def __init__(self, client: OpenSearch = None): 
        self.client = client or get_db_client()
        self._rollback_actions: List[Callable[[], None]] = []
    
    # Función para registrar acciones compensatorias. 
    def register_rollback(self, action: Callable[[], None]): 
        """Registra una función compensatoria para revertir cambios si falla una operación posterior."""
        self._rollback_actions.append(action)
    
    # Función para ejecutar acciones compensatorias. 
    def rollback(self): 
        """Ejecuta en orden inverso las acciones compensatorias registradas."""
        print("⚠️ [UNIT OF WORK] Ejecutando transacción compensatoria (Rollback)...")
        for action in reversed(self._rollback_actions):
            try:
                action()
            except Exception as e:
                print(f"❌ [ROLLBACK ERROR] Falló la acción compensatoria: {str(e)}")
        self._rollback_actions.clear()
    
    # Función para entrar en el contexto de la unidad de trabajo. 
    def __enter__(self): 
        return self
        
    # Función para salir del contexto de la unidad de trabajo. 
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"❌ [UNIT OF WORK] Excepción detectada: ({exc_type.__name__}): {exc_val}")
            self.rollback()
            return False # Propaga la excepción hacia la API
        self._rollback_actions.clear()
        return True