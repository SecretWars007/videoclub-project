import os 
import json 
# pyrefly: ignore [missing-import]
from opensearchpy import OpenSearch 

# --- INICIALIZACIÓN DE ÍNDICES EN OPENSEARCH ---
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://haproxy:9200")
INDICES = ["videos", "copies", "clients", "loans", "pricing_config"]

# Inicializa los índices en OpenSearch
def init_opensearch_indices():
    client = OpenSearch(
        hosts=[OPENSEARCH_HOST],
        use_ssl=False,
        verify_certs=False,
        ssl_show_warn=False
    )
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../database/mappings"))
    for index_name in INDICES:
        mapping_file = os.path.join(base_dir, f"{index_name}.json")
        if not os.path.exists(mapping_file):
            print(f"⚠️ Archivo no encontrado: {mapping_file}")
            continue
        if not client.indices.exists(index=index_name):
            with open(mapping_file, "r", encoding="utf-8") as f:
                mapping_body = json.load(f)
            client.indices.create(index=index_name, body=mapping_body)
            print(f"✅ Índice '{index_name}' creado exitosamente.")
        else:
            print(f"ℹ️ El índice '{index_name}' ya existe.")

# Ejecuta la inicialización de índices
if __name__ == "__main__":
    init_opensearch_indices()