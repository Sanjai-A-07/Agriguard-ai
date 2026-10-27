def test_known_class_returns_curated_advice(client):
    r = client.get("/api/advice/Tomato___Late_blight")
    assert r.status_code == 200
    body = r.json()
    assert body["disease_name"] == "Late blight"
    assert body["prevention"] and body["symptoms"]


def test_unknown_class_is_404(client):
    r = client.get("/api/advice/Banana___nothing")
    assert r.status_code == 404
    assert r.json()["error"] == "unknown_class"


def test_advice_contains_no_dosages(client):
    import re
    for cls in client.get("/api/crops").json()[0]["classes"]:
        text = str(client.get(f"/api/advice/{cls}").json())
        assert not re.search(r"\d+\s*(ml|g|kg|litre|liter|%)\b", text, re.I)
