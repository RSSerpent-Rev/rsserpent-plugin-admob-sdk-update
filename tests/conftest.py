import pytest
from rsserpent_rev import app
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Share one test client across the whole module with `pytest.fixture`."""
    return TestClient(app)
