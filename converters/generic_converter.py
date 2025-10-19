#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
通用文件转换器
处理简单的文件复制和重命名操作
"""

import os
import shutil
from core.base_converter import BaseConverter
from utils.logger import get_logger

logger = get_logger(__name__)


class GenericConverter(BaseConverter):
    """通用文件转换器"""
    
    def __init__(self, config):
        super().__init__(config)
    
    def convert(self, input_path: str, output_path: str, source_format: str, target_format: str) -> bool:
        """
        执行通用文件转换（复制/重命名）
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            source_format: 源文件格式
            target_format: 目标文件格式
            
        Returns:
            转换是否成功
        """
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 如果源格式和目标格式相同，直接复制文件
            if source_format.lower() == target_format.lower():
                shutil.copy2(input_path, output_path)
                logger.info(f"文件复制成功: {input_path} -> {output_path}")
                return True
            
            # 如果只是更改扩展名，进行重命名
            name_without_ext = os.path.splitext(input_path)[0]
            new_file_path = f"{name_without_ext}.{target_format}"
            
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
            
            os.rename(input_path, new_file_path)
            
            # 再复制到目标路径
            shutil.copy2(new_file_path, output_path)
            
            logger.info(f"文件重命名并复制成功: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"通用文件转换失败: {str(e)}")
            return False