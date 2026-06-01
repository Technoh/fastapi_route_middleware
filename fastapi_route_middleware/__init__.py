from asyncio import Future, iscoroutinefunction
from inspect import Parameter, signature
from typing import Any, Callable


async def _return_unknown_fn(fn, **kwargs) -> Any:
    """Helper function to call a function that may be synchronous or asynchronous."""
    if iscoroutinefunction(fn):
        return await fn(**kwargs)
    else:
        return fn(**kwargs)


def add_middleware(
    middleware: Callable[..., Any] | Callable[..., Future[Any]],
) -> Callable[[Callable[..., Any]], Callable[..., Future[Any]]]:
    """
    Decorator to add middleware functionality to FastAPI route handlers.

    This decorator wraps the original function with the middleware, allowing for
    pre-processing and post-processing of the request and response.

    Args:
        middleware: A callable that takes the same parameters as the route handler.
    Returns:
        A decorator that can be applied to FastAPI route handlers.
    """
    middleware_signature = signature(middleware)

    def _decorator(
        original_function: Callable[..., Any],
    ) -> Callable[..., Future[Any]]:
        original_signature = signature(original_function)
        complete_params = {
            **middleware_signature.parameters,
            **original_signature.parameters,
        }
        # Sort parameters without defaults first, then those with defaults.
        # Otherwise we get "ValueError: non-default argument follows default argument".
        sorted_params = sorted(
            complete_params.values(),
            key=lambda p: p.default is Parameter.empty and p.kind not in (
                Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD
            ),
            reverse=True,
        )

        complete_signature = original_signature.replace(parameters=sorted_params)
        async def _wrapper(*args, **kwargs) -> Any:
            middleware_args = {
                name: kwargs[name]
                for name in middleware_signature.parameters
                if name in kwargs
            }
            original_function_args = {
                name: kwargs[name]
                for name in original_signature.parameters
                if name in kwargs
            }
            early_return = await _return_unknown_fn(middleware, **middleware_args)
            if early_return is not None:
                return early_return
            return await _return_unknown_fn(original_function, **original_function_args)

        _wrapper.__signature__ = complete_signature
        return _wrapper

    return _decorator


__all__ = ["add_middleware"]
