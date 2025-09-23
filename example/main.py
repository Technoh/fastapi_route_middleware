from fastapi import FastAPI
from middlewares import (
    add_context,
    delayed_logger,
    exit_if_test,
    logger,
    read_context,
    set_cookie,
)

from fastapi_route_middleware import add_middleware

app = FastAPI(title="FastAPI Express", version="0.1.0")


@app.get("/")
@add_middleware(logger)
@add_middleware(set_cookie)
async def root():
    return {"message": "Hello!"}


@app.get("/{route}")
@add_middleware(add_context("Maronn"))
@add_middleware(exit_if_test)
@add_middleware(delayed_logger)
@add_middleware(read_context)
def route(route: str):
    return {"message": f"Hello, you're visiting {route}!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
