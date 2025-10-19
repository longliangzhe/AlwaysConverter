#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件工具模块
提供文件相关的工具函数
"""

import os
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)

# 尝试导入magic库
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False
    logger.warning("未安装python-magic库，将使用基础文件类型检测")


def get_file_type(file_path: str) -> Optional[str]:
    """
    获取文件类型（扩展名）
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件扩展名（小写，不包含点号）或None
    """
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return None
    
    # 首先尝试从文件扩展名获取
    _, ext = os.path.splitext(file_path)
    if ext:
        return ext[1:].lower()
    
    # 如果无法从扩展名获取，则使用magic库检测
    if HAS_MAGIC:
        try:
            mime = magic.from_file(file_path, mime=True)
            # 根据MIME类型映射到文件扩展名
            mime_to_ext = {
                'application/pdf': 'pdf',
                'application/msword': 'doc',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
                'text/plain': 'txt',
                'application/rtf': 'rtf',
                'application/vnd.oasis.opendocument.text': 'odt',
                'image/jpeg': 'jpg',
                'image/png': 'png',
                'image/gif': 'gif',
                'image/bmp': 'bmp',
                'image/tiff': 'tiff',
                'image/webp': 'webp',
                'audio/mpeg': 'mp3',
                'audio/wav': 'wav',
                'audio/flac': 'flac',
                'audio/aac': 'aac',
                'video/mp4': 'mp4',
                'video/x-msvideo': 'avi',
                'video/x-matroska': 'mkv',
                'application/zip': 'zip',
                'application/x-rar': 'rar',
                'application/x-7z-compressed': '7z',
                'application/x-tar': 'tar',
                'application/gzip': 'gz'
            }
            return mime_to_ext.get(mime, 'unknown')
        except Exception as e:
            logger.error(f"使用magic库获取文件类型失败: {e}")
            return None
    else:
        # 如果没有magic库，只能返回None
        logger.warning(f"无法从扩展名获取文件类型，且magic库不可用: {file_path}")
        return None


def get_file_size(file_path: str) -> Optional[int]:
    """
    获取文件大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件大小（字节）
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"获取文件大小失败: {str(e)}")
        return None


def is_file_supported(file_path: str, supported_formats: list) -> bool:
    """
    检查文件是否被支持
    
    Args:
        file_path: 文件路径
        supported_formats: 支持的格式列表
        
    Returns:
        文件是否被支持
    """
    file_type = get_file_type(file_path)
    if not file_type:
        return False
    
    return file_type.lower() in [fmt.lower() for fmt in supported_formats]


def get_file_name_without_extension(file_path: str) -> str:
    """
    获取不带扩展名的文件名
    
    Args:
        file_path: 文件路径
        
    Returns:
        不带扩展名的文件名
    """
    return os.path.splitext(os.path.basename(file_path))[0]