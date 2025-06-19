# UUID Generator API

A simple REST API that generates and resolves shortened UUID-based identifiers. This service provides endpoints for generating new UUIDs and resolving existing ones to their original values.

## Features

- Generate new UUIDs and associate them with values
- Resolve existing UUIDs to their original values
- In-memory storage for quick access
- FastAPI-powered with automatic OpenAPI documentation
- Docker support
- High-performance dependency management with uv

## Requirements

- Python 3.10 or higher
- Poetry for dependency management
- Pre-commit for code quality checks

## Development Setup

### Using uv (Recommended)

The project uses `uv` for fast dependency management. To set up the development environment:

1. Clone the repository:
```bash
git clone <repository-url>
cd shortened-url
```

2. Run the development setup script:
```bash
python scripts/dev_setup.py
```

3. Activate the virtual environment:
- Windows:
  ```bash
  .venv\Scripts\activate
  ```
- Unix/MacOS:
  ```bash
  source .venv/bin/activate
  ```

4. Start the development server:
```bash
uvicorn main:app --reload
```

### Docker Setup

1. Build the Docker image:
```bash
docker build -t shortened-url-api .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 --name shortened-url shortened-url-api
```

## Development

1. Run the development server:
```bash
poetry run uvicorn main:app --reload
```

2. Run tests:
```bash
poetry run pytest
```

3. Run linting:
```bash
poetry run ruff check .
```

4. Format code:
```bash
poetry run ruff format .
```

## API Endpoints

### Generate UUID

```http
POST /generate
Content-Type: application/json

{
    "value": "example-value"
}
```

Response:
```json
{
    "uuid": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Resolve UUID

```http
GET /resolve/123e4567-e89b-12d3-a456-426614174000
```

Response:
```json
{
    "value": "example-value"
}
```

## Documentation

Once the server is running, you can access:
- Interactive API documentation at: http://localhost:8000/docs
- Alternative API documentation at: http://localhost:8000/redoc

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and linting
4. Create a pull request

The pre-commit hooks will automatically check your code for:
- Code formatting (ruff)
- Linting issues (ruff)
- Common git issues (trailing whitespace, merge conflicts, etc.)
- Poetry configuration

## License

[Your License Here]
