from starlette.testclient import TestClient


def test_route(client: TestClient) -> None:
    """Test `rsserpent_plugin_admob_sdk_update.route`."""
    response = client.get("/admob/sdk-update/ios")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/xml"
    assert response.text.count("AdMob SDK iOS Update") == 1
    assert "<item>" in response.text
