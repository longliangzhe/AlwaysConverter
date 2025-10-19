#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
音频转换器
支持MP3、WAV、FLAC、AAC、OGG等音频格式转换
"""

import os
from core.base_converter import BaseConverter
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False
    logger.warning("PyDub库未安装，音频转换功能将受限")


class AudioConverter(BaseConverter):
    """音频转换器"""
    
    def __init__(self, config):
        super().__init__(config)
        self.supported = HAS_PYDUB
    
    def convert(self, input_path: str, output_path: str, source_format: str, target_format: str) -> bool:
        """
        执行音频转换
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            source_format: 源文件格式
            target_format: 目标文件格式
            
        Returns:
            转换是否成功
        """
        if not self.supported:
            logger.error("缺少必要的音频处理库(PyDub)")
            return False
        
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 加载音频文件
            audio = AudioSegment.from_file(input_path, format=source_format)
            
            # 导出为目标格式
            audio.export(output_path, format=target_format)
            
            logger.info(f"音频转换成功: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"音频转换失败: {str(e)}")
            return False