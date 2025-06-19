"""Tests for JWT authentication functionality."""

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from auth.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)
from main import app

client = TestClient(app)


def test_create_access_token():
    """Test creating JWT access token."""
    data = {"sub": "testuser"}
    token = create_access_token(data)

    # Decode and verify the token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "testuser"
    assert "exp" in payload


def test_create_access_token_with_expiration():
    """Test creating JWT access token with custom expiration."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data, expires_delta)

    # Decode and verify the token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "testuser"
    assert "exp" in payload


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)

    # Verify the hash
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_login_success():
    """Test successful login."""
    response = client.post("/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failure():
    """Test failed login attempts."""
    # Test with wrong password
    response = client.post(
        "/token", data={"username": "johndoe", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

    # Test with non-existent user
    response = client.post(
        "/token", data={"username": "nonexistent", "password": "secret"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_protected_endpoint_with_token():
    """Test accessing protected endpoint with valid token."""
    # First, get a token
    login_response = client.post(
        "/token", data={"username": "johndoe", "password": "secret"}
    )
    token = login_response.json()["access_token"]

    # Test protected endpoint
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "johndoe"
    assert user_data["email"] == "johndoe@example.com"


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_protected_endpoint_with_invalid_token():
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_token_expiration():
    """Test token expiration."""
    # Create a token that expires immediately
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(microseconds=1))

    # Wait a moment to ensure token expires
    import time

    time.sleep(0.1)

    # Try to use the expired token
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.parametrize(
    "endpoint,method",
    [
        ("/generate", "post"),
        ("/resolve/some-uuid", "get"),
    ],
)
def test_api_endpoint_authentication(endpoint, method):
    """Test that API endpoints require authentication."""
    # Test without token
    request_func = getattr(client, method)
    response = request_func(endpoint)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    # Test with invalid token
    response = request_func(endpoint, headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "detail" in response.json()


def test_generate_endpoint_with_auth():
    """Test the generate endpoint with authentication."""
    # Get token
    login_response = client.post(
        "/token", data={"username": "johndoe", "password": "secret"}
    )
    token = login_response.json()["access_token"]

    # Test generate endpoint
    response = client.post(
        "/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={"value": "test-value"},
    )
    assert response.status_code == 200
    assert "uuid" in response.json()


def test_resolve_endpoint_with_auth():
    """Test the resolve endpoint with authentication."""
    # Get token
    login_response = client.post(
        "/token", data={"username": "johndoe", "password": "secret"}
    )
    token = login_response.json()["access_token"]

    # First generate a UUID
    gen_response = client.post(
        "/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={"value": "test-value"},
    )
    uuid = gen_response.json()["uuid"]

    # Test resolve endpoint
    response = client.get(
        f"/resolve/{uuid}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["value"] == "test-value"
