import os
from fastapi import FastAPI
from opensearchpy import OpenSearch

# 📦 Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Club de Videos API",
    description="Backend NoSQL de Alta Disponibilidad con FastAPI y OpenSearch",
    version="1.0.0"
)

# 🔒 Variables de configuración importadas desde .env
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://haproxy:9200")

# 🔌 Función para obtener el cliente de OpenSearch
def get_opensearch_client() -> OpenSearch:
    return OpenSearch(
        hosts=[OPENSEARCH_HOST],
        use_ssl=False,
        verify_certs=False,
        ssl_show_warn=False
    )

#  Endpoint raíz para verificar el estado del sistema
@app.get("/", tags=["Root"])
def read_root():
    return {
        "system": "Club de Videos API",
        "status": "online",
        "architecture": "Alta Disponibilidad (HAProxy + OpenSearch Multi-Node)",
        "version": "1.0.0"
    }

# 🏥 Healthcheck: Verifica la conexión con OpenSearch
@app.get("/health", tags=["Healthcheck"])
def health_check():
    client = get_opensearch_client()
    try:
        health = client.cluster.health()
        return {
            "status": "healthy",
            "cluster_name": health.get("cluster_name"),
            "cluster_status": health.get("status"),
            "number_of_nodes": health.get("number_of_nodes"),
            "active_primary_shards": health.get("active_primary_shards"),
            "active_shards": health.get("active_shards")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }