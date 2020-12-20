#!/usr/bin/env python

# Source: https://stackoverflow.com/a/44176794/9235421


import asyncio
import time
from contextlib import contextmanager
from functools import wraps
import logging


# Setup logging
logger = logging.getLogger(__name__)


def duration(func):
    @contextmanager
    def wrapping_logic():
        logger.debug(f"Starting {func.__name__}")
        s = time.perf_counter_ns()
        yield
        e = time.perf_counter_ns() - s
        logger.debug(f"Left {func.__name__} after {e/10**6:.0f} ms")
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return (await func(*args, **kwargs))
            return tmp()
    return wrapper


if __name__ == "__main__":
    pass
