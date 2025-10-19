#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
视频转换器
支持MP4、AVI、MKV、MOV、WMV等视频格式转换
"""

import os
from core.base_converter import BaseConverter
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from moviepy.editor import VideoFileClip
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False
    logger.warning("MoviePy库未安装，视频转换功能将受限")


class VideoConverter(BaseConverter):
    """视频转换器"""
    
    def __init__(self, config):
        super().__init__(config)
        self.supported = HAS_MOVIEPY
    
    def convert(self, input_path: str, output_path: str, source_format: str, target_format: str) -> bool:
        """
        执行视频转换
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            source_format: 源文件格式
            target_format: 目标文件格式
            
        Returns:
            转换是否成功
        """
        if not self.supported:
            logger.error("缺少必要的视频处理库(MoviePy)")
            return False
        
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 加载视频文件
            with VideoFileClip(input_path) as video:
                # 导出为目标格式
                video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            logger.info(f"视频转换成功: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"视频转换失败: {str(e)}")
            return False