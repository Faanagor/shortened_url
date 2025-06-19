from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_generate_endpoint() -> None:
    """Test the generate endpoint with valid input."""
    # Test successful UUID generation
    response = client.post("/generate", json={"value": "test123"})
    assert response.status_code == HTTPStatus.OK
    assert "uuid" in response.json()

    # Store UUID for later tests
    generated_uuid = response.json()["uuid"]

    # Test resolving the generated UUID
    resolve_response = client.get(f"/resolve/{generated_uuid}")
    assert resolve_response.status_code == HTTPStatus.OK
    assert resolve_response.json() == {"value": "test123"}


def test_generate_endpoint_invalid_input() -> None:
    """Test the generate endpoint with invalid input."""
    # Test missing value field
    response = client.post("/generate", json={})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Test invalid JSON
    response = client.post("/generate", data="invalid json")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_resolve_endpoint_not_found() -> None:
    """Test the resolve endpoint with non-existent UUID."""
    # Test non-existent UUID
    response = client.get("/resolve/nonexistent-uuid")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "UUID not found"


def test_multiple_generations() -> None:
    """Test generating and resolving multiple UUIDs."""
    value1 = "first value"
    value2 = "second value"

    # Generate first UUID
    response1 = client.post("/generate", json={"value": value1})
    assert response1.status_code == HTTPStatus.OK
    uuid1 = response1.json()["uuid"]

    # Generate second UUID
    response2 = client.post("/generate", json={"value": value2})
    assert response2.status_code == HTTPStatus.OK
    uuid2 = response2.json()["uuid"]

    # Verify UUIDs are different
    assert uuid1 != uuid2

    # Verify correct resolution for both UUIDs
    resolve1 = client.get(f"/resolve/{uuid1}")
    assert resolve1.json()["value"] == value1

    resolve2 = client.get(f"/resolve/{uuid2}")
    assert resolve2.json()["value"] == value2
