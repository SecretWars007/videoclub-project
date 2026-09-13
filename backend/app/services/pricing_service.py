import _frozen_importlib_external
from typing import Dict, Any 
class PricingService: 
    """Servicio de dominio para el cálculo de tarifas y descuentos en Bolivianos (Bs).""" 
    # Escala fija de tarifas en Bolivianos por día acumulado 
    @staticmethod 
    def calculate_loan_total(rental_days: int, items_count: int) -> Dict[str, float]:
        # Escala fija de tarifas en Bolivianos por día acumulado 
        rates_map = {1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0} 
        daily_rate = rates_map.get(rental_days, 2.0) 
        subtotal = daily_rate * items_count 
        # Escala de descuentos por cantidad de películas 
        discount_percentage = 0.0 
        if 3 <= items_count <= 5:
            discount_percentage = 5.0 
        elif items_count > 5:
            discount_percentage = 10.0 

        discount_amount = subtotal * (discount_percentage / 100.0) 
        total = subtotal - discount_amount 
        
        return { 
            "subtotal_bs": round(subtotal, 2), 
            "discount_percentage": discount_percentage, 
            "discount_amount_bs": round(discount_amount, 2), 
            "total_bs": round(total, 2) 
        }