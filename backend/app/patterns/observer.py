from typing import List, Callable, Dict, Any 
# Clase LoanSubject (sujeto observable) para gestionar eventos de préstamos
# Utiliza polimorfismo y herencia para notificar a los observadores.
class LoanSubject: 
    """Sujeto del patrón Observer para notificar eventos sobre alquileres."""
    # Método constructor que inicializa la lista de observadores
    def __init__(self): 
        self._observers: List[Callable[[str, Dict[str, Any]], None]] = [] 
    # Método para adjuntar un observador
    def attach(self, observer: Callable[[str, Dict[str, Any]], None]): 
        self._observers.append(observer) 
    # Método para notificar a todos los observadores
    def notify(self, event_type: str, data: Dict[str, Any]): 
        for observer in self._observers: 
            try: 
                observer(event_type, data) 
            except Exception as e: 
                print(f"⚠️ [OBSERVER ERROR] ({event_type}): {str(e)}") 
    # Método para registrar eventos de préstamos
    def audit_log_observer(self,event_type: str, data: Dict[str, Any]): 
        """Observer para auditoría de préstamos.""" 
        print(f"📢 [EVENTO OBSERVER] {event_type.upper()}: Préstamo {data.get('loan_id')} registrado para {data.get('client_name')}.")