#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础转换器类
所有具体转换器都应该继承此类
"""

from abc import ABC, abstractmethod
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseConverter(ABC):
    """基础转换器抽象类"""
    
    def __init__(self, config: dict):
        """
        初始化转换器
        
        Args:
            config: 转换器配置
        """
        self.config = config
        self.name = config.get('name', self.__class__.__name__)
        self.input_formats = config.get('input_formats', [])
        self.output_formats = config.get('output_formats', [])
    
    @abstractmethod
    def convert(self, input_path: str, output_path: str, source_format: str, target_format: str) -> bool:
        """
        执行转换操作（抽象方法，子类必须实现）
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            source_format: 源文件格式
            target_format: 目标文件格式
            
        Returns:
            转换是否成功
        """
        pass
    
    def can_convert(self, source_format: str, target_format: str) -> bool:
        """
        检查是否可以执行指定的转换
        
        Args:
            source_format: 源文件格式
            target_format: 目标文件格式
            
        Returns:
            是否可以转换
        """
        source_format = source_format.lower()
        target_format = target_format.lower()
        
        # 检查源格式是否支持
        source_supported = False
        for fmt in self.input_formats:
            if fmt.lower() == source_format or fmt.lower() == '*':
                source_supported = True
                break
        
        # 检查目标格式是否支持
        target_supported = False
        for fmt in self.output_formats:
            if fmt.lower() == target_format or fmt.lower() == '*':
                target_supported = True
                break
        
        return source_supported and target_supported
    
    def get_input_formats(self) -> List[str]:
        """
        获取支持的输入格式列表
        
        Returns:
            支持的输入格式列表
        """
        return self.input_formats.copy()
    
    def get_output_formats(self) -> List[str]:
        """
        获取支持的输出格式列表
        
        Returns:
            支持的输出格式列表
        """
        return self.output_formats.copy()