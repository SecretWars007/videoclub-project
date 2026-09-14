from fastapi import APIRouter, Depends, HTTPException, Query 
from typing import Optional, List 
from datetime import datetime
 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch
from app.models.schemas import VideoCreate
from app.repositories.video_repository import VideoRepository
from app.api.dependencies import get_opensearch_db
# router videos
router = APIRouter(prefix="/videos", tags=["Videos"])
# funcion para crear video
@router.post("/", status_code=201)
def create_video(video: VideoCreate, db: OpenSearch = Depends(get_opensearch_db)):
    repo = VideoRepository(client=db)
    doc = video.model_dump()
    doc["created_at"] = datetime.utcnow().isoformat()
    video_id = f"vid_{int(datetime.utcnow().timestamp())}"
    repo.index_document(video_id, doc)
    doc["video_id"] = video_id
    return doc

# funcion para buscar videos
@router.get("/search") 
def search_videos( 
    q: Optional[str] = Query(None, description="Término de búsqueda fuzzy sobre título, actores o títulos alternativos"), 
    genre: Optional[str] = Query(None, description="Filtro exacto por género"), 
    db: OpenSearch = Depends(get_opensearch_db) 
): 
    repo = VideoRepository(client=db) 
    return repo.search_videos(query_text=q, genre=genre)
