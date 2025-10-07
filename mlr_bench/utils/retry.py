"""Retry utilities for handling API errors."""

import asyncio
import time
from typing import TypeVar, Callable, Any
from functools import wraps
from loguru import logger

T = TypeVar('T')


def sync_retry_on_503(max_retries: int = 5, base_delay: float = 2.0):
    """Decorator to retry synchronous functions on 503 errors with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (will be exponentially increased)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e)

                    # Check if this is a 503 error
                    if '503' in error_str and 'UNAVAILABLE' in error_str:
                        if attempt < max_retries:
                            delay = base_delay * (2 ** attempt)  # Exponential backoff
                            logger.warning(
                                f"API overloaded (503), retrying in {delay:.1f}s "
                                f"(attempt {attempt + 1}/{max_retries})..."
                            )
                            time.sleep(delay)
                            continue

                    # If not a 503 or we've exhausted retries, raise the error
                    raise

            # Should never reach here, but just in case
            return func(*args, **kwargs)

        return wrapper
    return decorator


def async_retry_on_503(max_retries: int = 5, base_delay: float = 2.0):
    """Decorator to retry async functions on 503 errors with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (will be exponentially increased)
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e)

                    # Check if this is a 503 error
                    if '503' in error_str and 'UNAVAILABLE' in error_str:
                        if attempt < max_retries:
                            delay = base_delay * (2 ** attempt)  # Exponential backoff
                            logger.warning(
                                f"API overloaded (503), retrying in {delay:.1f}s "
                                f"(attempt {attempt + 1}/{max_retries})..."
                            )
                            await asyncio.sleep(delay)
                            continue

                    # If not a 503 or we've exhausted retries, raise the error
                    raise

            # Should never reach here, but just in case
            return await func(*args, **kwargs)

        return wrapper
    return decorator
