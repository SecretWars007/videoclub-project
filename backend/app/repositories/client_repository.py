from typing import List, Dict, Any
from app.repositories.base_repository import BaseRepository

# Clase para el repositorio de clientes
class ClientRepository(BaseRepository): 
    # Método para inicializar el repositorio
    def __init__(self, client=None): 
        super().__init__(index_name="clients", client=client) 
    # Método para buscar clientes
    def search_by_location(self, lat: float, lon: float, distance_km: float = 5.0) -> List[Dict[str, Any]]: 
        """Busca clientes cercanos utilizando la consulta geoespacial geo_distance.""" 
        body = { 
            "query": { 
                "bool": { 
                    "must": [{"match_all": {}}], 
                    "filter": { "geo_distance": { "distance": f"{distance_km}km", "location": { 
                        "lat": lat, 
                        "lon": lon 
                    } } } 
                } 
            } 
        } 
        # Ejecución de la búsqueda
        response = self.client.search(index=self.index_name, body=body) 
        # Extracción de resultados
        results = [] 
        for hit in response["hits"]["hits"]: 
            doc = hit["\_source"] 
            doc["client_id"] = hit["\_id"] 
            results.append(doc) 
        return results