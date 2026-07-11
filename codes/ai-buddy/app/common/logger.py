import sys

from loguru import logger


def setup_logger() -> None:
    """配置项目统一日志输出。"""
    logger.remove()

    logger.add(
        sys.stderr,
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )


__all__ = ["logger", "setup_logger"]
