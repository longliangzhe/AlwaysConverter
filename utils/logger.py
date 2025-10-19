#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日志模块
提供统一的日志记录功能
"""

import os
from loguru import logger
from typing import Optional

# 创建日志目录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def get_logger(name: Optional[str] = None):
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        日志记录器实例
    """
    # 移除默认的日志处理器
    logger.remove()
    
    # 添加文件日志处理器
    logger.add(
        "logs/converter.log",
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        encoding="utf-8"
    )
    
    # 添加控制台日志处理器
    logger.add(
        lambda msg: print(msg, end=''),
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    return logger