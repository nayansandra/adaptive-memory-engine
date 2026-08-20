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

#PATCH/memory-items/{id} test cases
def test_update_memory_success():
    create_response = client.post(
        "/memory-items",
        json={
            "content": "Original content"
        }
    )

    memory_id = create_response.json()["id"]

    response = client.patch(
        f"/memory-items/{memory_id}",
        json={
            "title": "Updated title"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == memory_id
    assert data["title"] == "Updated title"

def test_update_memory_empty_request():
    create_response = client.post(
        "/memory-items",
        json={
            "content": "Patch test"
        }
    )

    memory_id = create_response.json()["id"]

    response = client.patch(
        f"/memory-items/{memory_id}",
        json={}
    )

    assert response.status_code == 400

def test_update_memory_not_found():
    response = client.patch(
        "/memory-items/999999",
        json={
            "title": "Updated title"
        }
    )

    assert response.status_code == 404

#DELETE/memory-items/{id} test cases
def test_delete_memory_success():
    create_response = client.post(
        "/memory-items",
        json={
            "content": "Memory to delete"
        }
    )

    memory_id = create_response.json()["id"]

    response = client.delete(
        f"/memory-items/{memory_id}"
    )

    assert response.status_code == 204

def test_delete_memory_not_found():
    response = client.delete(
        "/memory-items/999999"
    )

    assert response.status_code == 404

#GET/memory-items/{id} access count test cases
def test_get_memory_increments_access_count():
    create_response = client.post(
        "/memory-items",
        json={
            "content": "Access tracking test"
        }
    )

    memory_id = create_response.json()["id"]

    response = client.get(
        f"/memory-items/{memory_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_count"] == 1

def test_multiple_get_requests_increment_access_count():

    create_response = client.post(
        "/memory-items",
        json={
            "content": "Multiple access test"
        }
    )

    memory_id = create_response.json()["id"]

    client.get(f"/memory-items/{memory_id}")

    response = client.get(
        f"/memory-items/{memory_id}"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["access_count"] == 2

#access updates importance score test cases
def test_first_access_updates_importance_score():

    create_response = client.post(
        "/memory-items",
        json={
            "content": "Importance score test"
        }
    )

    memory_id = create_response.json()["id"]

    response = client.get(
        f"/memory-items/{memory_id}"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["access_count"] == 1
    assert data["importance_score"] == 1

def test_multiple_accesses_update_importance_score():

    create_response = client.post(
        "/memory-items",
        json={
            "content": "Multiple importance test"
        }
    )

    memory_id = create_response.json()["id"]

    client.get(f"/memory-items/{memory_id}")

    response = client.get(
        f"/memory-items/{memory_id}"
    )

    data = response.json()

    assert response.status_code == 200
    assert data["access_count"] == 2
    assert data["importance_score"] == 2

#ranked memories test cases
def test_ranked_memories_are_sorted_by_score():

    memory_a = client.post(
        "/memory-items",
        json={"content": "Memory A"}
    ).json()

    memory_b = client.post(
        "/memory-items",
        json={"content": "Memory B"}
    ).json()

    client.get(f"/memory-items/{memory_a['id']}")
    client.get(f"/memory-items/{memory_a['id']}")

    client.get(f"/memory-items/{memory_b['id']}")

    response = client.get("/memory-items/ranked")

    assert response.status_code == 200

    memories = response.json()

    a_index = next(
        i for i, memory in enumerate(memories)
        if memory["id"] == memory_a["id"]
    )

    b_index = next(
        i for i, memory in enumerate(memories)
        if memory["id"] == memory_b["id"]
    )

    assert a_index < b_index

#search test cases
def test_search_returns_matching_memories():

    client.post(
        "/memory-items",
        json={"content": "I studied PostgreSQL indexing"}
    )

    client.post(
        "/memory-items",
        json={"content": "I need to buy groceries"}
    )

    response = client.get(
        "/memory-items/search?query=postgres"
    )

    assert response.status_code == 200

    memories = response.json()

    assert len(memories) >= 1

    assert any(
        "postgres" in memory["content"].lower()
        for memory in memories
    )

def test_search_rejects_whitespace_query():

    response = client.get(
        "/memory-items/search?query=   "
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Search query cannot be empty or whitespace."
    }