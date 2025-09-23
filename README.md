# FastAPI Route Middleware

A dependency free™ middleware system for adding middleware to specific FastAPI routes. I just like how node express works.

## Installation

```bash
pip install fastapi_route_middleware
```

but actually I know you're using `uv`, so:

```bash
uv add fastapi_route_middleware
```

## Usage

The `add_middleware` decorator allows you to apply middleware functions to specific FastAPI routes, giving you fine-grained control over which middleware runs on which endpoints. Middlewares can access FastAPI Request and Response even if the original route does not. If a middleware returns anything, it will trigger an early return and won't cause the original route handler to be called.

### Basic Example

```python
from fastapi import FastAPI
from fastapi_route_middleware import add_middleware

app = FastAPI()

# Define a simple middleware function
def log_request(request_id: str):
    print(f"Processing request {request_id}")

# Apply middleware to specific route
@app.get("/items/{item_id}")
@add_middleware(log_request)
async def get_item(item_id: int, request_id: str):
    return {"item_id": item_id}
```

### Async Middleware Example

```python
from fastapi import FastAPI
from fastapi_route_middleware import add_middleware
import asyncio

app = FastAPI()

# Define an async middleware function
async def async_auth_middleware(user_id: str):
    # Simulate async authentication check
    await asyncio.sleep(0.1)
    print(f"Authenticated user {user_id}")

@app.get("/protected")
@add_middleware(async_auth_middleware)
async def protected_route(user_id: str, data: str):
    return {"message": f"Hello {user_id}", "data": data}
```

### Multiple Middleware Example

```python
from fastapi import FastAPI
from fastapi_route_middleware import add_middleware

app = FastAPI()

def rate_limit_middleware(api_key: str):
    print(f"Rate limiting for API key: {api_key}")

def audit_middleware(user_id: str):
    print(f"Auditing action for user: {user_id}")

# Stack multiple middlewares
@app.post("/api/data")
@add_middleware(rate_limit_middleware)
@add_middleware(audit_middleware)
async def create_data(api_key: str, user_id: str, payload: dict):
    return {"status": "created", "data": payload}
```

## How It Works

The `add_middleware` decorator:

1. Executes the middleware before calling the original route handler
2. Supports both sync and async middleware functions
3. Preserves the original function's signature for FastAPI's dependency injection

## Requirements

- Python >= 3.8
- FastAPI >= 0.68.0

## License

MIT
