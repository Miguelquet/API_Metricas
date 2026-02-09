## Telemetry API (Portfolio Project)

A production-style (but simple) telemetry collector:
- Ingest **metrics** (numeric) and **events** (text + severity)
- Store in PostgreSQL
- Query with filters (service, time range, name, tags)
- Stats endpoint (min/max/avg/count)
- API Key auth (read/write)
- Retention script (30 days)
- Tests + CI

### Run locally

1) Create env file:
```bash
cp .env.example .env
2) Start:
docker compose up --build
3) Docs:
http://localhost:8000/docs
X-API-Key: <your_key>
Example curl

Create a metric:

curl -X POST http://localhost:8000/v1/metrics \
  -H "Content-Type: application/json" \
  -H "X-API-Key: write_key_change_me" \
  -d '{
    "service": "api-gateway",
    "name": "http_latency_ms",
    "value": 123.4,
    "unit": "ms",
    "tags": {"env":"dev","region":"eu","version":"0.1.0"}
  }'


Create an event:
