from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

#GET/memory-items test cases
def test_get_memories():
    response = client.get("/memory-items")

    assert response.status_code == 200

#POST/memory-items test cases
def test_create_memory_success():
    response = client.post(
        "/memory-items",
        json={
            "content": "Test memory"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "Test memory"
    assert data["title"] == "Test memory"
    assert "id" in data

def test_create_memory_empty_content():
    response = client.post(
        "/memory-items",
        json={
            "content": ""
        }
    )

    assert response.status_code == 422

def test_create_memory_whitespace_only():
    response = client.post(
        "/memory-items",
        json={
            "content": "     "
        }
    )

    assert response.status_code == 422

def test_create_memory_trims_content():
    response = client.post(
        "/memory-items",
        json={
            "content": "   hello world   "
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "hello world"
    assert data["title"] == "hello world"

#GET/memory-items/{id} test cases
def test_get_memory_success():
    create_response = client.post(
        "/memory-items",
        json={
            "content": "Memory for GET test"
        }
    )

    memory_id = create_response.json()["id"]

    response = client.get(f"/memory-items/{memory_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == memory_id
    assert data["content"] == "Memory for GET test"

def test_get_memory_not_found():
    response = client.get("/memory-items/999999")

    assert response.status_code == 404