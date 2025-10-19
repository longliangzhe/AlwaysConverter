#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化版文件工具模块
不依赖libmagic库，使用文件扩展名来判断文件类型
"""

import os

# 文件类型映射
FILE_TYPE_MAP = {
    # 文档格式
    'pdf': 'document',
    'doc': 'document',
    'docx': 'document',
    'txt': 'document',
    'rtf': 'document',
    'odt': 'document',
    'xls': 'document',
    'xlsx': 'document',
    'ppt': 'document',
    'pptx': 'document',
    
    # 图片格式
    'jpg': 'image',
    'jpeg': 'image',
    'png': 'image',
    'gif': 'image',
    'bmp': 'image',
    'tiff': 'image',
    'webp': 'image',
    'svg': 'image',
    'ico': 'image',
    
    # 音频格式
    'mp3': 'audio',
    'wav': 'audio',
    'flac': 'audio',
    'aac': 'audio',
    'ogg': 'audio',
    'wma': 'audio',
    'm4a': 'audio',
    'opus': 'audio',
    
    # 视频格式
    'mp4': 'video',
    'avi': 'video',
    'mkv': 'video',
    'mov': 'video',
    'wmv': 'video',
    'flv': 'video',
    'webm': 'video',
    'm4v': 'video',
    
    # 压缩格式
    'zip': 'archive',
    'rar': 'archive',
    '7z': 'archive',
    'tar': 'archive',
    'gz': 'archive',
    'bz2': 'archive',
}

# MIME类型映射
MIME_TYPE_MAP = {
    # 文档格式
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'rtf': 'application/rtf',
    'odt': 'application/vnd.oasis.opendocument.text',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    
    # 图片格式
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'tiff': 'image/tiff',
    'webp': 'image/webp',
    'svg': 'image/svg+xml',
    'ico': 'image/x-icon',
    
    # 音频格式
    'mp3': 'audio/mpeg',
    'wav': 'audio/wav',
    'flac': 'audio/flac',
    'aac': 'audio/aac',
    'ogg': 'audio/ogg',
    'wma': 'audio/x-ms-wma',
    'm4a': 'audio/mp4',
    'opus': 'audio/opus',
    
    # 视频格式
    'mp4': 'video/mp4',
    'avi': 'video/x-msvideo',
    'mkv': 'video/x-matroska',
    'mov': 'video/quicktime',
    'wmv': 'video/x-ms-wmv',
    'flv': 'video/x-flv',
    'webm': 'video/webm',
    'm4v': 'video/x-m4v',
    
    # 压缩格式
    'zip': 'application/zip',
    'rar': 'application/vnd.rar',
    '7z': 'application/x-7z-compressed',
    'tar': 'application/x-tar',
    'gz': 'application/gzip',
    'bz2': 'application/x-bzip2',
}


def get_file_type(file_path: str) -> str:
    """
    获取文件类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件类型字符串
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower().lstrip('.')
    
    # 根据扩展名判断文件类型
    return FILE_TYPE_MAP.get(ext, 'unknown')


def get_file_size(file_path: str) -> int:
    """
    获取文件大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件大小（字节）
    """
    try:
        return os.path.getsize(file_path)
    except:
        return 0


def is_file_supported(file_path: str, supported_formats: list) -> bool:
    """
    检查文件是否支持
    
    Args:
        file_path: 文件路径
        supported_formats: 支持的格式列表
        
    Returns:
        是否支持
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower().lstrip('.')
    
    return ext in supported_formats or '*' in supported_formats


def get_file_name_without_extension(file_path: str) -> str:
    """
    获取不带扩展名的文件名
    
    Args:
        file_path: 文件路径
        
    Returns:
        不带扩展名的文件名
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_mime_type(file_path: str) -> str:
    """
    获取文件MIME类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        MIME类型字符串
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower().lstrip('.')
    
    return MIME_TYPE_MAP.get(ext, 'application/octet-stream')