import pytest
from app.main import app, store
from app.storage import URLStore
from app.utils import generate_short_code, is_valid_url
# No need to import URLStore again; it's already imported from app.storage above.
@pytest.fixture(autouse=True)
def setup_test_client():
    store._data.clear()  # Reset in-memory store before each test
    with app.test_client() as client:
        yield client

def test_health_check(setup_test_client):
    """Health check should return status ok"""
    res = setup_test_client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_shorten_valid_url(setup_test_client):
    """Should return short code for valid URL"""
    res = setup_test_client.post("/api/shorten", json={"url": "https://example.com"})
    data = res.get_json()
    assert res.status_code == 201
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(setup_test_client):
    """Should reject invalid URL"""
    res = setup_test_client.post("/api/shorten", json={"url": "not-a-valid-url"})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_shorten_missing_json(setup_test_client):
    """Should reject request with no JSON"""
    res = setup_test_client.post("/api/shorten")
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_redirect_valid_code(setup_test_client):
    """Should redirect to original URL using valid short code"""
    post = setup_test_client.post("/api/shorten", json={"url": "https://example.com"})
    code = post.get_json()["short_code"]

    redirect_res = setup_test_client.get(f"/{code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["Location"] == "https://example.com"

def test_redirect_invalid_code(setup_test_client):
    """Should return 404 for invalid short code"""
    res = setup_test_client.get("/invalidcode")
    assert res.status_code == 404
    assert "error" in res.get_json()

def test_stats(setup_test_client):
    """Should return click stats for a valid short code"""
    post = setup_test_client.post("/api/shorten", json={"url": "https://example.com"})
    code = post.get_json()["short_code"]
    setup_test_client.get(f"/{code}")  # simulate 1 click

    stats = setup_test_client.get(f"/api/stats/{code}")
    data = stats.get_json()
    assert stats.status_code == 200
    assert data["clicks"] == 1
    assert data["url"] == "https://example.com"

def test_home_endpoint(setup_test_client):
    """Should return list of all shortened URLs"""
    setup_test_client.post("/api/shorten", json={"url": "https://site1.com"})
    setup_test_client.post("/api/shorten", json={"url": "https://site2.com"})

    res = setup_test_client.get("/")
    urls = res.get_json()
    assert res.status_code == 200
    assert isinstance(urls, list)
    assert len(urls) == 2
@pytest.fixture(autouse=True)
def setup_test_client():
    store.reset()  # ✅ Clear data safely
    with app.test_client() as client:
        yield client
