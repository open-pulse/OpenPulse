import logging
import typing
from contextlib import contextmanager
from functools import wraps
from time import perf_counter

logger = logging.getLogger(__name__)


def function_timer(func):
    """
    Decorator to log the time of a given function.

    Example:
    ```
    @function_timer
    def long_function():
        ...

    $ INFO:root:long_function took 0.601s
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        msg = f"{func.__name__} took {elapsed:.3f}s"
        logger.info(msg)
        print(msg)
        return result

    return wrapper


@contextmanager
def context_timer(name: str, /):
    """
    Context manager to log the time of a code snippet.

    Example:
    ```
    with context_timer(name="My code snippet"):
        long_function()
        short_function()
        another_long_function()
        ...

    $ INFO:root:My code snippet took 0.601s
    ```
    """

    start = perf_counter()
    yield start
    elapsed = perf_counter() - start
    msg = f"{name} took {elapsed:.3f}s"
    logger.info(msg)
    print(msg)


@typing.overload
def warn_delays(time=0.1, /): ...


def warn_delays(arg=None, /):
    """
    Warn if a given function is taking too long to run.

    The default time considered to be long is 100 ms, or 0.1 s.
    This can be customized

    Example:
    ```
    @warn_delays
    def short_function():
        ...

    @warn_delays(0.5)
    def long_function():
        ...
    ```
    """

    if callable(arg):
        function = arg
        maximum_time = 0.1
    else:
        function = None
        maximum_time = arg

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = perf_counter()
            result = func(*args, **kwargs)
            elapsed = perf_counter() - start

            if elapsed >= maximum_time:
                logger.warning(f"{func.__name__} took {elapsed:.3f}s. It should be less than {maximum_time:.3f}s.")

            return result

        return wrapper

    # This is a trick to allow for arguments in the decorator
    if function is not None:
        return decorator(function)
    else:
        return decorator
