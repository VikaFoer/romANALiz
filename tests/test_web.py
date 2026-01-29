"""Tests for web app (FastAPI)."""
from fastapi.testclient import TestClient

from airbot.web import app


def test_root_returns_html_or_json():
    with TestClient(app) as client:
        r = client.get("/")
    assert r.status_code == 200
    ct = r.headers.get("content-type", "")
    if "text/html" in ct:
        assert b"root" in r.content or b"Air-bot" in r.content
    else:
        assert b"Air-bot" in r.content  # JSON fallback when no static


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_post_events():
    with TestClient(app) as client:
        client.get("/health")
        r = client.post("/events", json={"id": "t1", "value": 50})
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "queued"
    assert data.get("id") == "t1"
