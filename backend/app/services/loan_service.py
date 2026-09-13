from app.core import unit_of_work
from app.core import unit_of_work
from typing import List, Dict, Any 
from datetime import datetime, timedelta 
from app.repositories.copy_repository import CopyRepository 
from app.repositories.client_repository import ClientRepository 
from app.services.pricing_service import PricingService 
from app.core.unit_of_work import UnitOfWork

class LoanService: 
    """Servicio orquestador del ciclo de vida de préstamos NoSQL."""
    # Función para inicializar el servicio de préstamos
    def __init__(self, uow: UnitOfWork): 
        self.uow = uow
        self.copy_repo = CopyRepository(client=uow.client) 
        self.client_repo = ClientRepository(client=uow.client) 
    # función para crear un nuevo préstamo
    def create_loan(self, client_id: str, copy_ids: List[str], rental_days: int) -> Dict[str, Any]: 
        # 1. Validar existencia y estado de bloqueo del cliente 
        client = self.client_repo.get_by_id(client_id) 
        if not client: 
            raise ValueError(f"Cliente con ID '{client_id}' no encontrado.")
        if client.get("is_blocked", False): 
            raise ValueError(f"El cliente '{client.get('full_name')}' está bloqueado para nuevos préstamos.")
        items = [] 
        # 2. Reservar copias físicamente mediante OCC y registrar compensación en UoW 
        for copy_id in copy_ids: 
            copy_doc = self.copy_repo.get_by_id(copy_id) 
            if not copy_doc: 
                raise ValueError(f"La copia '{copy_id}' no existe.") 
            if copy_doc.get("status") != "available": 
                raise ValueError(f"La copia '{copy_id}' ({copy_doc.get('video_title')}) no está disponible.")

            seq_no = copy_doc["_seq_no"] 
            primary_term = copy_doc["_primary_term"] 
            # Actualización concurrente segura 
            self.copy_repo.update_status_occ(copy_id, "rented", seq_no, primary_term) 
            
            # Acción compensatoria si la transacción falla más adelante 
            self.uow.register_rollback( 
                lambda c_id=copy_id, s_no=seq_no, p_term=primary_term: 
                self.copy_repo.update_status_occ(c_id, "available", s_no + 1, p_term) 
            )

            items.append({ 
                "copy_id": copy_id, 
                "video_id": copy_doc.get("video_id"), 
                "video_title": copy_doc.get("video_title"), 
                "daily_rate_bs": 2.0 
            }) 
        # 3. Calcular desglose económico en Bs 
        pricing = PricingService.calculate_loan_total(rental_days, len(copy_ids)) 
        # 4. Crear documento del préstamo 
        now = datetime.utcnow() 
        loan_doc = { 
            "client_id": client_id, 
            "client_name": client.get("full_name"), 
            "client_ci_nit": client.get("ci_nit"), 
            "items": items, 
            "rental_days": rental_days, 
            "loan_date": now.isoformat(), 
            "expected_return_date": (now + timedelta(days=rental_days)).isoformat(), 
            "subtotal_bs": pricing["subtotal_bs"], 
            "discount_percentage": pricing["discount_percentage"], 
            "discount_amount_bs": pricing["discount_amount_bs"], 
            "total_bs": pricing["total_bs"], 
            "status": "active" 
        } 
        loan_id = f"loan_{int(now.timestamp())}" 
        self.uow.client.index(index="loans", id=loan_id, body=loan_doc, refresh=True) 
        loan_doc["loan_id"] = loan_id
        # 5. Limpiar estado de "reserva en memoria" (No hay rollback explícito aquí)
        # Las copias ya están marcadas como "rented" en Elasticsearch.
        # La compensación solo se ejecutaría si el try falla antes de indexar.
        return loan_doc