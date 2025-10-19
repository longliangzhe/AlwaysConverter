#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
核心转换器类
负责管理所有文件转换器并执行转换操作
"""

import os
import importlib
from typing import Dict, Any
from utils.logger import get_logger

# 尝试使用完整的文件工具模块，如果失败则使用简化版
try:
    from utils.file_utils import get_file_type
    USE_SIMPLE_FILE_UTILS = False
except ImportError:
    from utils.file_utils_simple import get_file_type
    USE_SIMPLE_FILE_UTILS = True

logger = get_logger(__name__)

if USE_SIMPLE_FILE_UTILS:
    logger.info("使用简化版文件工具模块")
else:
    logger.info("使用完整版文件工具模块")


class FileConverter:
    """文件转换器主类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化文件转换器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.converters = {}
        self._load_converters()
    
    def _load_converters(self):
        """加载所有可用的转换器"""
        converters_config = self.config.get('converters', {})
        
        for converter_name, converter_config in converters_config.items():
            try:
                # 动态导入转换器模块
                module_name = converter_config.get('module', f'converters.{converter_name}')
                module = importlib.import_module(module_name)
                
                # 获取转换器类
                class_name = converter_config.get('class', f'{converter_name.capitalize()}Converter')
                converter_class = getattr(module, class_name)
                
                # 实例化转换器
                converter_instance = converter_class(converter_config)
                self.converters[converter_name] = converter_instance
                
                logger.info(f"成功加载转换器: {converter_name}")
            except Exception as e:
                logger.error(f"加载转换器 {converter_name} 失败: {str(e)}")
    
    def convert(self, input_path: str, output_path: str, target_format: str) -> bool:
        """
        执行文件转换
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            target_format: 目标格式
            
        Returns:
            转换是否成功
        """
        try:
            # 检查输入文件
            if not os.path.exists(input_path):
                logger.error(f"输入文件不存在: {input_path}")
                return False
            
            # 获取源文件类型
            source_format = get_file_type(input_path)
            if not source_format:
                logger.error(f"无法识别文件类型: {input_path}")
                return False
            
            logger.info(f"检测到源文件类型: {source_format}")
            logger.info(f"目标文件类型: {target_format}")
            
            # 查找合适的转换器
            converter = self._find_converter(source_format, target_format)
            if not converter:
                logger.error(f"未找到支持 {source_format} 到 {target_format} 的转换器")
                return False
            
            # 执行转换
            success = converter.convert(input_path, output_path, source_format, target_format)
            return success
            
        except Exception as e:
            logger.error(f"转换过程中发生错误: {str(e)}")
            return False
    
    def _find_converter(self, source_format: str, target_format: str):
        """
        查找合适的转换器
        
        Args:
            source_format: 源格式
            target_format: 目标格式
            
        Returns:
            合适的转换器实例或None
        """
        # 首先查找专门处理该转换的转换器
        for converter in self.converters.values():
            if converter.can_convert(source_format, target_format):
                return converter
        
        # 如果没有找到专门的转换器，查找通用转换器
        for converter in self.converters.values():
            if converter.can_convert(source_format, target_format):
                return converter
        
        return None
    
    def get_supported_formats(self) -> Dict[str, list]:
        """
        获取所有支持的格式
        
        Returns:
            支持的格式字典
        """
        formats = {}
        for name, converter in self.converters.items():
            formats[name] = {
                'input': converter.get_input_formats(),
                'output': converter.get_output_formats()
            }
        return formats
    
    def is_format_supported(self, format_name: str, format_type: str) -> bool:
        """
        检查指定格式是否被支持
        
        Args:
            format_name: 格式名称（如 'pdf', 'jpg' 等）
            format_type: 格式类型 ('input' 或 'output')
            
        Returns:
            是否支持该格式
        """
        supported_formats = self.get_supported_formats()
        
        # 遍历所有转换器的支持格式
        for converter_formats in supported_formats.values():
            if format_type in converter_formats:
                if format_name.lower() in [fmt.lower() for fmt in converter_formats[format_type]]:
                    return True
        
        return False