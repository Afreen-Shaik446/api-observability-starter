"""Application entrypoint with observability wired in."""
import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .logging_config import configure_logging
from .middleware import ObservabilityMiddleware

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="api-observability-starter",
    description="FastAPI app demonstrating Prometheus metrics, request-ID tracing, and structured logging",
    version="0.1.0",
)
app.add_middleware(ObservabilityMiddleware)


@app.get("/healthz", tags=["health"])
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/metrics", tags=["observability"], include_in_schema=False)
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/demo/items", tags=["demo"])
def demo_items() -> dict:
    logger.info("serving demo items")
    return {"items": [{"id": 1, "name": "widget"}, {"id": 2, "name": "gadget"}]}


@app.get("/demo/error", tags=["demo"])
def demo_error() -> dict:
    # Exercises the error-rate metrics/alerts.
    raise RuntimeError("demo error")
