"""UUID Generator API.

This module implements a simple REST API that generates and resolves shortened UUID-based identifiers.
It provides endpoints for generating new UUIDs and resolving existing ones to their original values.
"""

import uuid
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from auth import User, auth_router, get_current_active_user

app = FastAPI(
    title="UUID Generator API",
    description="A simple API that generates and resolves shortened UUID-based identifiers",
    version="1.0.0",
)

# Include authentication routes
app.include_router(auth_router)

# In-memory storage for UUID mappings
uuid_store = {}


class GenerateRequest(BaseModel):
    """Request model for generating a new UUID.

    Attributes:
        value: The value to associate with the generated UUID.
    """

    value: str


class GenerateResponse(BaseModel):
    """Response model for UUID generation.

    Attributes:
        uuid: The generated UUID string.
    """

    uuid: str


class ResolveResponse(BaseModel):
    """Response model for UUID resolution.

    Attributes:
        value: The original value associated with the UUID.
    """

    value: str


@app.post("/generate", response_model=GenerateResponse)
def generate_id(
    request: GenerateRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> GenerateResponse:
    """Generate a new UUID and associate it with the provided value.

    Args:
        request: The request object containing the value to store.
        current_user: The authenticated user making the request.

    Returns:
        GenerateResponse: A response containing the generated UUID.

    Example:
        Request:
            POST /generate
            Authorization: Bearer <token>
            {
                "value": "example-value"
            }

        Response:
            {
                "uuid": "123e4567-e89b-12d3-a456-426614174000"
            }
    """
    new_uuid = str(uuid.uuid4())
    uuid_store[new_uuid] = request.value
    return {"uuid": new_uuid}


@app.get("/resolve/{uuid}", response_model=ResolveResponse)
def resolve_id(
    uuid: str, current_user: Annotated[User, Depends(get_current_active_user)]
) -> ResolveResponse:
    """Resolve a UUID to its associated value.

    Args:
        uuid: The UUID string to look up.
        current_user: The authenticated user making the request.

    Returns:
        ResolveResponse: A response containing the value associated with the UUID.

    Raises:
        HTTPException: If the UUID is not found (404).

    Example:
        Request:
            GET /resolve/123e4567-e89b-12d3-a456-426614174000
            Authorization: Bearer <token>

        Response:
            {
                "value": "example-value"
            }

        Error Response:
            {
                "detail": "UUID not found"
            }
    """
    value = uuid_store.get(uuid)
    if value is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="UUID not found")
    return {"value": value}
