import os 
from fastapi import FastAPI 
from app.api.v1 import videos, copies, clients, loans 
from app.core.database import get_db_client 
# 📦 Inicialización de la aplicación FastAPI 
app = FastAPI( title="Club de Videos API", description="Backend NoSQL de Alta Disponibilidad con FastAPI y OpenSearch", version="1.0.0" ) 
# 🔗 Registro de Routers REST API v1
# router videos 
app.include_router(videos.router, prefix="/api/v1")
# router copies
app.include_router(copies.router, prefix="/api/v1") 
# router clients
app.include_router(clients.router, prefix="/api/v1") 
# router loans
app.include_router(loans.router, prefix="/api/v1") 
# 🏠 Endpoint raíz para verificar el estado del sistema 
@app.get("/", tags=["Root"])
# function read root
def read_root(): 
    return { "system": "Club de Videos API", "status": "online", "architecture": "Alta Disponibilidad (HAProxy + OpenSearch Multi-Node)", "version": "1.0.0" } 
# 🏥 Healthcheck: Verifica la conexión con OpenSearch (Pool Singleton)
@app.get("/health", tags=["Healthcheck"])
# function health check
def health_check(): 
    try: 
        client = get_db_client() 
        health = client.cluster.health() 
        return { 
            "status": "healthy", 
            "cluster_name": health.get("cluster_name"), "cluster_status": health.get("status"), "number_of_nodes": health.get("number_of_nodes"), 
            "active_primary_shards": health.get("active_primary_shards"), 
            "active_shards": health.get("active_shards") 
        } 
    except Exception as e: 
        return { 
            "status": "unhealthy", 
            "error": str(e) 
        }