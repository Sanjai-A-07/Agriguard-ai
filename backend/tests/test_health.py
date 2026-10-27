from tests.conftest import FakeModelService


def test_health_reports_model_available(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "model_available": True}


def test_health_reports_model_missing(make_client):
    c = make_client(FakeModelService(available=False))
    assert c.get("/health").json()["model_available"] is False


def test_crops_lists_supported_classes(client):
    r = client.get("/api/crops")
    assert r.status_code == 200
    tomato = r.json()[0]
    assert tomato["id"] == "tomato"
    assert "Tomato___healthy" in tomato["classes"]
    assert len(tomato["classes"]) == 5
