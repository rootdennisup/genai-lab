import time
from functools import wraps
from app.ef.logger_config import logger

def log_execution_info(func):
    """用于记录函数调用参数和执行耗时的装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 记录开始调用信息
        logger.info(f">>> 正在执行: {func.__name__} | 输入: {args} {kwargs}")
        
        start_time = time.perf_counter()
        try:
            # 执行原函数逻辑（业务逻辑）
            result = await func(*args, **kwargs)
            
            end_time = time.perf_counter()
            duration = end_time - start_time
            # 记录成功返回与性能统计
            logger.info(f"<<< 执行成功: {func.__name__} | 耗时: {duration:.4f}s")
            return result
        except Exception as e:
            # 异常追踪：记录错误信息
            logger.error(f"!!! 执行失败: {func.__name__} | 报错: {str(e)}")
            raise e
    return wrapper