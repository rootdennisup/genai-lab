import logging
import sys

# 配置日志记录器
def setup_logger():
    # 创建记录器
    logger = logging.getLogger("LLM_App")
    logger.setLevel(logging.INFO)

    # 定义日志输出格式：时间 - 级别 - 消息
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # 1. 配置控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 2. 配置本地文件持久化存储 (app.log) 
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 添加处理器
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# 初始化单例 logger
logger = setup_logger()