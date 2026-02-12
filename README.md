## Telemetry API (Portfolio Project) V1.0
 
 A production-style (but simple) telemetry collector:
 - Ingest **metrics** (numeric) and **events** (text + severity)
 - Store in PostgreSQL
 - Query with filters (service, time range, name, tags)
 - Stats endpoint (min/max/avg/count)
 - API Key auth (read/write)
 - Retention script (30 days)
 - Tests + CI


## Fase 1 completada: migraciones con Alembic

La aplicación ya no crea tablas en runtime con `create_all`. Ahora el esquema se versiona con Alembic.

### Comandos principales

```bash
cd proyect
alembic upgrade head
alembic downgrade -1
```

+### Flujo recomendado

1. Crear o ajustar modelos SQLAlchemy.
2. Generar una nueva migración (`alembic revision -m "..."` o autogenerate en fases posteriores).
3. Aplicar con `alembic upgrade head`.

Con Docker Compose, el servicio API ejecuta `alembic upgrade head` antes de levantar Uvicorn.


> Nota de compatibilidad: si ya existían tablas `metrics/events` creadas antes de Alembic, el arranque en Docker ejecuta un bootstrap que hace `alembic stamp head` automáticamente para evitar errores de tipo "relation already exists". En caso de que siga ocurriendo el error introduzca en la carpeta `*/proyecto/` el comando `docker compose down -v`y posteriormente vuelva a subir el contenedor de docker con `docker compose up --build` 

