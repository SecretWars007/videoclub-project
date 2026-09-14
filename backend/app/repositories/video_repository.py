from typing import List, Dict, Any, Optional
from app.repositories.base_repository import BaseRepository

# Clase para el repositorio de videos
class VideoRepository(BaseRepository):
    # Método para inicializar el repositorio
    def __init__(self, client=None): 
        super().__init__(index_name="videos", client=client) 
    # Método para buscar videos
    def search_videos(self, query_text: Optional[str] = None, genre: Optional[str] = None) -> List[Dict[str, Any]]: 
        must_clause = [] 
        if query_text: 
            must_clause.append({ 
                "multi_match": { 
                    "query": query_text, 
                    "fields": ["title^3", "alternative_titles^2", "actors"], "fuzziness": "AUTO" 
                } 
            })
        # Si se proporciona un género, se agrega un filtro de término
        if genre: 
            must_clause.append({"term": {"genre": genre}}) 
        # Construcción del cuerpo de la consulta
        body = { 
            "query": { 
                "bool": { 
                    "must": must_clause if must_clause else [{"match_all": {}}] 
                } 
            } 
        } 
        # Ejecución de la búsqueda
        response = self.client.search(index=self.index_name, body=body) 
        # Extracción de resultados
        results = [] 
        for hit in response["hits"]["hits"]: 
            doc = hit["_source"] 
            doc["video_id"] = hit["_id"] 
            results.append(doc) 
        return results
