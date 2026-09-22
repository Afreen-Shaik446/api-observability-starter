from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _metrics_text() -> str:
    response = client.get("/metrics")
    assert response.status_code == 200
    return response.text


def test_request_counter_increments():
    before = _metrics_text()
    client.get("/demo/items")
    after = _metrics_text()
    assert "http_requests_total" in after
    # A sample for the demo route must exist after the request.
    assert 'route="/demo/items"' in after
    assert len(after) >= len(before)


def test_duration_histogram_observes_requests():
    client.get("/demo/items")
    text = _metrics_text()
    assert "http_request_duration_seconds_bucket" in text


def test_request_id_is_generated_and_echoed():
    response = client.get("/demo/items")
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


def test_request_id_is_propagated():
    response = client.get("/demo/items", headers={"X-Request-ID": "trace-abc"})
    assert response.headers["X-Request-ID"] == "trace-abc"


def test_error_endpoint_records_5xx():
    no_raise_client = TestClient(app, raise_server_exceptions=False)
    response = no_raise_client.get("/demo/error")
    assert response.status_code == 500
    metrics_text = _metrics_text()
    assert 'status_code="500"' in metrics_text
