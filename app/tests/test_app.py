from app import app


def client():
    app.testing = True
    return app.test_client()


def test_index():
    resp = client().get("/")
    assert resp.status_code == 200
    assert resp.get_json()["message"].startswith("Hello")


def test_health():
    resp = client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_add():
    resp = client().get("/add/2/3")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["sum"] == 5
