#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
命令行测试脚本
用于测试AlwaysConverter的基本功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from core.converter import FileConverter
from utils.config import load_config
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """主函数"""
    print("AlwaysConverter 命令行测试工具")
    print("=" * 40)
    
    # 加载配置
    config = load_config()
    
    # 创建转换器实例
    converter = FileConverter(config)
    
    # 显示支持的格式
    print("\n支持的输入格式:")
    supported_formats = converter.get_supported_formats()
    for category, formats in supported_formats.items():
        print(f"  {category}: {', '.join(formats['input'])}")
    
    print("\n支持的输出格式:")
    for category, formats in supported_formats.items():
        print(f"  {category}: {', '.join(formats['output'])}")
    
    # 测试转换（模拟）
    print("\n\n模拟转换测试:")
    test_cases = [
        ("document.pdf", "document.docx"),
        ("image.jpg", "image.png"),
        ("audio.mp3", "audio.wav"),
        ("video.mp4", "video.avi"),
        ("archive.zip", "archive.tar")
    ]
    
    for input_file, output_file in test_cases:
        input_format = input_file.split('.')[-1]
        output_format = output_file.split('.')[-1]
        
        if converter.is_format_supported(input_format, 'input') and converter.is_format_supported(output_format, 'output'):
            print(f"  ✓ {input_file} -> {output_file} (支持)")
        else:
            print(f"  ✗ {input_file} -> {output_file} (不支持)")


if __name__ == "__main__":
    main()