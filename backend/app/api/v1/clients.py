from fastapi import APIRouter, Depends, Query 
from datetime import datetime 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch
from app.models.schemas import ClientCreate 
from app.repositories.client_repository import ClientRepository 
from app.api.dependencies import get_opensearch_db
# router clients
router = APIRouter(prefix="/clients", tags=["Clients"])
# function create client
@router.post("/", status_code=201) 
def create_client(client: ClientCreate, db: OpenSearch = Depends(get_opensearch_db)): 
    repo = ClientRepository(client=db) 
    doc = client.model_dump() 
    doc["registered_at"] = datetime.utcnow().isoformat() 
    doc["is_blocked"] = False 
    client_id = f"cli_{int(datetime.utcnow().timestamp())}" 
    repo.index_document(client_id, doc) 
    doc["client_id"] = client_id 
    return doc 
# function get nearby clients
@router.get("/nearby") 
def get_nearby_clients( 
    lat: float = Query(..., ge=-90.0, le=90.0), 
    lon: float = Query(..., ge=-180.0, le=180.0), 
    radius_km: float = Query(5.0, gt=0), 
    db: OpenSearch = Depends(get_opensearch_db) 
): 
    repo = ClientRepository(client=db) 
    return repo.search_by_location(lat=lat, lon=lon, distance_km=radius_km)
