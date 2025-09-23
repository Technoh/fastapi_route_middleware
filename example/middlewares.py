import asyncio

from fastapi import Request, Response


async def logger(request: Request):
    print(f"Request: {request.method} {request.url}")


async def delayed_logger(request: Request):
    async def delayed_log():
        await asyncio.sleep(1)
        print(f"Delayed log: {request.method} {request.url} processed")

    asyncio.create_task(delayed_log())


def set_cookie(response: Response):
    response.set_cookie(key="my_cookie", value="cookie_value")


def exit_if_test(route: str):
    if route == "test":
        return {"message": "Exiting early for test route!"}


def add_context(message: str):
    def middleware(request: Request):
        request.state.custom_value = message

    return middleware


def read_context(request: Request):
    print(f"Custom value from context: {request.state.custom_value}")
