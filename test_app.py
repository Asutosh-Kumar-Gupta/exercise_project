from fastapi.testclient import TestClient
from main import app
from database import Base, engine

import pytest

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong!"}

def test_authorize(client):
    response = client.get("/authorize", headers={"key": "your_secret_key"})
    assert response.status_code == 200
    assert response.json() == {"message": "Authorization successful"}

def test_save_get_delete_flow(client):
    # Test saving a key-value pair
    response_save = client.post("/save", json={"key": "test_key", "value": "test_value"})
    assert response_save.status_code == 200
    assert response_save.json() == {"message": "Key-value pair saved successfully"}

    # Test getting the saved value
    response_get = client.get("/get/test_key")
    assert response_get.status_code == 200
    assert response_get.json() == {"key": "test_key", "value": "test_value"}

    # Test deleting the key
    response_delete = client.delete("/delete/test_key")
    assert response_delete.status_code == 200
    assert response_delete.json() == {"message": "Key 'test_key' deleted successfully"}

    # Test getting the deleted key (should return 404)
    response_get_deleted = client.get("/get/test_key")
    assert response_get_deleted.status_code == 404
    assert response_get_deleted.json() == {"detail": "Key not found in the database"}
