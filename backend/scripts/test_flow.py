import os 
import sys 
# Asegurar que el directorio app esté en el PATH de Python 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.database import get_db_client 
from app.repositories.video_repository import VideoRepository 
from app.repositories.client_repository import ClientRepository 
from app.repositories.copy_repository import CopyRepository 
from app.services.pricing_service import PricingService 
def run_integration_tests(): 
    print("🧪 Iniciando pruebas de integración End-to-End...") 
    client = get_db_client() 
# Test 1: Healthcheck de la base de datos OpenSearch 
    health = client.cluster.health()
    assert health["status"] in ["green", "yellow"], "Fallo en healthcheck de OpenSearch" 
    print(f" ✅ [TEST 1] Conexión al clúster OpenSearch: OK (Estado: {health['status']})") 
# Test 2: Búsqueda Fuzzy en Películas 
    video_repo = VideoRepository(client=client) 
    fuzzy_results = video_repo.search_videos(query_text="Padrino")
    assert len(fuzzy_results) > 0, "No se encontraron resultados en la búsqueda Fuzzy" 
    print(f" ✅ [TEST 2] Búsqueda Fuzzy de películas: {len(fuzzy_results)} resultado(s) encontrado(s)") 
# Test 3: Motor de Precios en Bolivianos (Bs) y Descuentos 
    pricing = PricingService.calculate_loan_total(rental_days=3, items_count=4) 
    assert pricing["total_bs"] == 15.2, f"Cálculo de tarifas incorrecto: {pricing}" 
    print(f" ✅ [TEST 3] Motor de cálculo en Bs (Descuentos): {pricing['total_bs']} Bs (OK)") 
# Test 4: Búsqueda Geoespacial (geo_distance) 
    client_repo = ClientRepository(client=client) 
    nearby = client_repo.search_by_location(lat=-16.5000, lon=-68.1500, distance_km=5.0) 
    assert len(nearby) > 0, "No se encontraron clientes cercanos" 
    print(f" ✅ [TEST 4] Búsqueda geoespacial geo_distance: {len(nearby)} cliente(s) en el radio") 
# Test 5: Verificación de Copias Físicas de Inventario 
    copy_repo = CopyRepository(client=client) 
    copy = copy_repo.get_by_id("cop_101") 
    assert copy is not None, "Copia de prueba no encontrada" 
    copy_id = copy.get("copy_id", "cop_101") 
    print(f" ✅ [TEST 5] Verificación de inventario de copias: ID {copy_id} ({copy['status']}) - OK") 
    print("\n🎉 ¡Todas las pruebas de integración End-to-End pasaron correctamente!")
# fin de las pruebas de integración End-to-End
# ejecutar las pruebas de integración End-to-End
if __name__ == "__main__": run_integration_tests()