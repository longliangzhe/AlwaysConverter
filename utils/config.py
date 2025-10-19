#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
负责加载和管理配置文件
"""

import os
import yaml
from typing import Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    "converters": {
        "document": {
            "module": "converters.document_converter",
            "class": "DocumentConverter",
            "input_formats": ["pdf", "doc", "docx", "txt", "rtf", "odt"],
            "output_formats": ["pdf", "docx", "txt", "rtf", "odt"]
        },
        "image": {
            "module": "converters.image_converter",
            "class": "ImageConverter",
            "input_formats": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "svg"],
            "output_formats": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"]
        },
        "audio": {
            "module": "converters.audio_converter",
            "class": "AudioConverter",
            "input_formats": ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"],
            "output_formats": ["mp3", "wav", "flac", "aac", "ogg"]
        },
        "video": {
            "module": "converters.video_converter",
            "class": "VideoConverter",
            "input_formats": ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"],
            "output_formats": ["mp4", "avi", "mkv", "mov"]
        }
    },
    "logging": {
        "level": "INFO",
        "file": "logs/converter.log",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    }
}


def load_config(config_path: str = None) -> Dict[Any, Any]:
    """
    加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    # 如果没有指定配置文件路径，使用默认配置
    if not config_path or not os.path.exists(config_path):
        logger.info("未找到配置文件，使用默认配置")
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 合并默认配置和用户配置
        merged_config = merge_config(DEFAULT_CONFIG, config)
        logger.info(f"成功加载配置文件: {config_path}")
        return merged_config
        
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        return DEFAULT_CONFIG


def merge_config(default: Dict, user: Dict) -> Dict:
    """
    合并默认配置和用户配置
    
    Args:
        default: 默认配置
        user: 用户配置
        
    Returns:
        合并后的配置
    """
    result = default.copy()
    
    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    
    return result