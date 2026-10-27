import io

from tests.conftest import FakeModelService, make_image_bytes


def post(client, content, name="leaf.jpg", ctype="image/jpeg", crop="tomato"):
    return client.post("/api/predict", files={"image": (name, content, ctype)}, data={"crop": crop})


def test_valid_upload_returns_prediction_and_guidance(client, jpeg_bytes):
    r = post(client, jpeg_bytes)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "confident"
    assert body["predicted_class"] == "Tomato___Early_blight"
    assert body["guidance"]["disease_name"] == "Early blight"
    assert body["scan_id"] and body["disclaimer"]


def test_png_and_webp_are_accepted(client):
    assert post(client, make_image_bytes("PNG"), "a.png", "image/png").status_code == 200
    assert post(client, make_image_bytes("WEBP"), "a.webp", "image/webp").status_code == 200


def test_uncertain_result_has_no_definitive_diagnosis(make_client, jpeg_bytes):
    c = make_client(FakeModelService(conf=0.41, status="uncertain"))
    body = post(c, jpeg_bytes).json()
    assert body["status"] == "uncertain"
    assert body["predicted_class"] is None
    assert body["guidance"] is None
    assert "Unable to identify reliably" in body["message"]


def test_blurry_image_downgrades_confident_result(client):
    flat = make_image_bytes("JPEG", textured=False)
    body = post(client, flat).json()
    assert body["status"] == "poor_image"
    assert body["predicted_class"] is None
    assert "blurry" in body["image_quality"]["warnings"]


def test_corrupted_image_rejected(client, jpeg_bytes):
    r = post(client, jpeg_bytes[:200])
    assert r.status_code == 400
    assert r.json()["error"] == "invalid_image"


def test_text_file_with_image_extension_rejected(client):
    r = post(client, b"hello, not an image", "fake.jpg", "image/jpeg")
    assert r.status_code == 400


def test_unsupported_format_rejected(client):
    r = post(client, make_image_bytes("GIF"), "a.gif", "image/gif")
    assert r.status_code == 415
    assert r.json()["error"] == "unsupported_type"


def test_empty_upload_rejected(client):
    r = post(client, b"")
    assert r.status_code == 400
    assert r.json()["error"] == "empty_upload"


def test_missing_file_is_422(client):
    assert client.post("/api/predict", data={"crop": "tomato"}).status_code == 422


def test_unsupported_crop_rejected(client, jpeg_bytes):
    r = post(client, jpeg_bytes, crop="banana")
    assert r.status_code == 400
    assert r.json()["error"] == "unsupported_crop"


def test_model_unavailable_returns_503(make_client, jpeg_bytes):
    c = make_client(FakeModelService(available=False))
    r = post(c, jpeg_bytes)
    assert r.status_code == 503
    assert r.json()["error"] == "model_unavailable"
