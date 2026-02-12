# Telemetry API (Portfolio Project) — Fase 1
 
API de telemetría backend con enfoque de producto real:
- Ingesta de **métricas** (numéricas) y **eventos** (texto + severidad).
- Persistencia en **PostgreSQL**.
- Filtros por servicio/rango temporal/nombre/tags.
- Endpoint de estadísticas (min/max/avg/count).
- Autenticación por API Key (read/write).
- Retención de datos (script).
- Tests automáticos.
 
+## Estado del proyecto
 
+✅ **Fase 1 completada:** migraciones con Alembic (sin `create_all` como estrategia principal de evolución de esquema).
 
## Arquitectura (actual)

```text
Cliente -> FastAPI -> SQLAlchemy -> PostgreSQL
             |            |
             |            └-> Alembic (versionado de esquema)
             └-> API Key auth + endpoints health/metrics/events/stats
```
## Quickstart
### Opción A: local (sin Docker)
 
 ```bash
 cd proyect
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
 alembic upgrade head
uvicorn app.main:app --reload
```

### Opción B: Docker Compose

```bash
cd proyect
docker compose up --build
```

Si tienes estado antiguo de volúmenes/tablas y aparecen conflictos de esquema:

```bash
cd proyect
docker compose down -v
docker compose up --build
 ```
 
## Variables de entorno (mínimas sugeridas)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | Cadena de conexión PostgreSQL | `postgresql+psycopg2://user:pass@db:5432/telemetry` |
| `READ_API_KEY` | API key para lectura | `read_dev_key` |
| `WRITE_API_KEY` | API key para escritura | `write_dev_key` |
| `RETENTION_DAYS` | Días de retención de datos | `30` |

> Ajusta nombres/valores según `app/core/config.py`.

## Flujo de migraciones (Alembic)

```bash
cd proyect
alembic upgrade head
alembic downgrade -1
```

Flujo recomendado:
1. Ajustar modelos SQLAlchemy.
2. Crear migración (`alembic revision -m "..."`).
3. Aplicar con `alembic upgrade head`.
 
## Endpoints clave (ejemplo)

> Sustituye las API keys por tus valores reales.

### Health

```bash
curl -X GET http://localhost:8000/health
```

### Crear métrica

```bash
curl -X POST http://localhost:8000/metrics \
  -H "X-API-Key: write_dev_key" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "radio-link",
    "name": "latency_ms",
    "value": 23.5,
    "tags": {"site": "campus-a", "device_type": "ap"}
  }'
```

### Consultar métricas

```bash
curl -X GET "http://localhost:8000/metrics?service=radio-link&name=latency_ms" \
  -H "X-API-Key: read_dev_key"
```

### Estadísticas

```bash
curl -X GET "http://localhost:8000/metrics/stats?service=radio-link&name=latency_ms" \
  -H "X-API-Key: read_dev_key"
```

