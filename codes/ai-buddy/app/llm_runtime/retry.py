import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

import httpx

from app.common.logger import logger

T = TypeVar("T")


class RetryConfig:
    """LLM 调用重试配置。"""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 0.5,
        max_delay: float = 8.0,
    ) -> None:
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay


class SoftFailureError(Exception):
    """HTTP 成功，但业务上认为模型响应不可用。"""


def is_retryable_http_error(error: httpx.HTTPStatusError) -> bool:
    """判断 HTTP 状态码是否值得重试。"""
    status_code = error.response.status_code

    if status_code == 429:
        return True

    if 500 <= status_code < 600:
        return True

    return False


def calculate_backoff_delay(
    attempt: int,
    config: RetryConfig,
) -> float:
    """指数退避 + 少量随机抖动，避免多次请求同时重试。"""
    delay = min(
        config.base_delay * (2 ** attempt),
        config.max_delay,
    )

    jitter = random.uniform(0, 0.2)

    return delay + jitter


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    config: RetryConfig | None = None,
) -> T:
    """通用异步重试器。"""
    retry_config = config or RetryConfig()
    last_error: Exception | None = None

    for attempt in range(retry_config.max_attempts):
        try:
            return await operation()

        except httpx.HTTPStatusError as error:
            last_error = error

            if not is_retryable_http_error(error):
                logger.warning(
                    "Non-retryable HTTP error status_code={} attempt={}/{}",
                    error.response.status_code,
                    attempt + 1,
                    retry_config.max_attempts,
                )
                raise

        except SoftFailureError as error:
            last_error = error

        except httpx.TimeoutException as error:
            last_error = error

        except httpx.TransportError as error:
            last_error = error

        if attempt == retry_config.max_attempts - 1:
            break

        delay = calculate_backoff_delay(attempt, retry_config)
        logger.warning(
            "Retrying operation attempt={}/{} delay={:.2f}s error_type={} error={}",
            attempt + 1,
            retry_config.max_attempts,
            delay,
            type(last_error).__name__ if last_error else "Unknown",
            last_error,
        )
        await asyncio.sleep(delay)

    assert last_error is not None
    logger.error(
        "Retry exhausted attempts={} final_error_type={} final_error={}",
        retry_config.max_attempts,
        type(last_error).__name__,
        last_error,
    )
    raise last_error
