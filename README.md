# api-observability-starter

Drop-in observability for a Python (FastAPI) API: Prometheus metrics middleware, request-ID tracing, structured JSON logging, example alert rules, and a sample Grafana dashboard.

This is a starter template for demonstration purposes — tune buckets, thresholds, and cardinality for your workload before production use.

## RED vs USE (brief)

- **RED** (for request-driven services): **R**ate (requests/sec), **E**rrors (fraction of 5xx), **D**uration (latency distribution). This repo instruments exactly these three via the middleware.
- **USE** (for resources): **U**tilization, **S**aturation, **E**rrors — e.g. CPU utilization, queue saturation, disk errors. Pair this repo's RED metrics with node/cluster USE metrics from kube-state-metrics or node_exporter for full coverage.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

curl localhost:8000/demo/items
curl localhost:8000/metrics        # Prometheus exposition format
curl localhost:8000/healthz
```

Request IDs: every response carries `X-Request-ID` (generated if the client doesn't send one), and log lines include it, so you can correlate logs with metrics.

## Prometheus

Point Prometheus at the app (example `scrape_configs`):

```yaml
scrape_configs:
  - job_name: "api-observability-starter"
    static_configs:
      - targets: ["localhost:8000"]
    metrics_path: /metrics
```

Load the example alerts: `prometheus/prometheus.yml` can reference `prometheus/alerts.yml` via `rule_files`. Thresholds are starting points — adjust them.

## Grafana

Import `grafana/dashboard.json` (uses the `${DS_PROMETHEUS}` datasource variable).

## Tests

```bash
pip install pytest httpx
pytest -v
```
