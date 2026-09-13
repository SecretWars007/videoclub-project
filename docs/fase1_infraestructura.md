# Bitácora de Infraestructura (Fase 1: Alta Disponibilidad)

## Componentes Desplegados

1. **HAProxy (2.8)**: Escuchando en el puerto `9200` y balanceando en modo *Round-Robin* hacia los dos nodos de OpenSearch.
2. **OpenSearch Multi-nodo**: Nodos `opensearch-node1` y `opensearch-node2` en cluster coordinado.
3. **OpenSearch Dashboards**: Interfaz gráfica en el puerto `5601`.
4. **Backend FastAPI**: Servidor Python con verificación de salud hacia HAProxy (`http://haproxy:9200`).

## Comandos de Control (Ejecutar desde `containers/`)

- Levantar cluster: `docker compose up --build -d`
- Ver estado de contenedores: `docker compose ps`
- Ver estadísticas de HAProxy: `http://localhost:8404`
