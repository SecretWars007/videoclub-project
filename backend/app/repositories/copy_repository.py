from typing import Dict, Any, Optional
from datetime import datetime
# pyrefly: ignore [missing-import]
from opensearchpy.exceptions import ConflictError
from app.repositories.base_repository import BaseRepository
# Clase para el repositorio de copias 
class CopyRepository(BaseRepository): 
    # Método para inicializar el repositorio 
    def __init__(self, client=None): 
        super().__init__(index_name="copies", client=client) 
    # Método para actualizar el estado de la copia utilizando Control de Concurrencia Optimista 
    def update_status_occ(self, copy_id: str, new_status: str, seq_no: int, primary_term: int) -> bool: 
        """Actualiza el estado de la copia utilizando Control de Concurrencia Optimista (OCC)."""
        doc = self.get_by_id(copy_id) 
        if not doc: 
            raise ValueError(f"Copia {copy_id} no encontrada.") 
        doc["status"] = new_status 
        doc["updated_at"] = datetime.utcnow().isoformat()

        # Al especificar if_seq_no e if_primary_term, OpenSearch rechaza la mutación si hubo escrituras concurrentes 
        self.client.index( 
            index=self.index_name, 
            id=copy_id, 
            body=doc, 
            if_seq_no=seq_no, 
            if_primary_term=primary_term, 
            refresh=True 
        ) 
        return True
    # Método para registrar la baja de una copia usando un Script Painless atómico 
    def retire_copy_painless(self, copy_id: str, reason: str, notes: Optional[str] = None) -> bool: 
        """Registra la baja de una copia usando un Script Painless atómico.""" 
        now_str = datetime.utcnow().isoformat() 
        script_body = { 
            "script": { 
                "source": """ 
                    ctx._source.status = 'retired'; 
                    ctx._source.retirement_info = [
                        'retired_at': params.now, 
                        'reason': params.reason, 
                        'notes': params.notes 
                    ]; 
                    ctx._source.updated_at = params.now; 
                """, 
                "lang": "painless", 
                "params": { 
                    "now": now_str, 
                    "reason": reason, 
                    "notes": notes or "" 
                } 
            } 
        } 
        try: 
            self.client.update(index=self.index_name, id=copy_id, body=script_body, refresh=True) 
            return True 
        except Exception as e: 
            print(f"❌ Error al retirar copia con Painless: {str(e)}") 
            return False
