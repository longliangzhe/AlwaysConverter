#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AlwaysConverter 测试文件
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.converter import FileConverter
from utils.config import load_config


class TestFileConverter(unittest.TestCase):
    """文件转换器测试类"""
    
    def setUp(self):
        """测试初始化"""
        config = load_config()
        self.converter = FileConverter(config)
    
    def test_supported_formats(self):
        """测试支持的格式"""
        # 测试文档格式
        self.assertTrue(self.converter.is_format_supported('pdf', 'input'))
        self.assertTrue(self.converter.is_format_supported('docx', 'input'))
        self.assertTrue(self.converter.is_format_supported('txt', 'input'))
        
        # 测试图片格式
        self.assertTrue(self.converter.is_format_supported('jpg', 'input'))
        self.assertTrue(self.converter.is_format_supported('png', 'input'))
        self.assertTrue(self.converter.is_format_supported('gif', 'input'))
        
        # 测试音频格式
        self.assertTrue(self.converter.is_format_supported('mp3', 'input'))
        self.assertTrue(self.converter.is_format_supported('wav', 'input'))
        
        # 测试视频格式
        self.assertTrue(self.converter.is_format_supported('mp4', 'input'))
        self.assertTrue(self.converter.is_format_supported('avi', 'input'))
        
        # 测试压缩格式
        self.assertTrue(self.converter.is_format_supported('zip', 'input'))
        self.assertTrue(self.converter.is_format_supported('rar', 'input'))
    
    def test_converter_initialization(self):
        """测试转换器初始化"""
        self.assertIsNotNone(self.converter)
        self.assertIsNotNone(self.converter.config)
        self.assertGreater(len(self.converter.converters), 0)
    
    @patch('converters.document_converter.DocumentConverter.convert')
    def test_document_conversion(self, mock_convert):
        """测试文档转换"""
        mock_convert.return_value = True
        result = self.converter.convert('test.docx', 'test.pdf', 'docx', 'pdf')
        self.assertTrue(result)
    
    @patch('converters.image_converter.ImageConverter.convert')
    def test_image_conversion(self, mock_convert):
        """测试图片转换"""
        mock_convert.return_value = True
        result = self.converter.convert('test.jpg', 'test.png', 'jpg', 'png')
        self.assertTrue(result)
    
    @patch('converters.audio_converter.AudioConverter.convert')
    def test_audio_conversion(self, mock_convert):
        """测试音频转换"""
        mock_convert.return_value = True
        result = self.converter.convert('test.mp3', 'test.wav', 'mp3', 'wav')
        self.assertTrue(result)
    
    @patch('converters.video_converter.VideoConverter.convert')
    def test_video_conversion(self, mock_convert):
        """测试视频转换"""
        mock_convert.return_value = True
        result = self.converter.convert('test.mp4', 'test.avi', 'mp4', 'avi')
        self.assertTrue(result)
    
    @patch('converters.archive_converter.ArchiveConverter.convert')
    def test_archive_conversion(self, mock_convert):
        """测试压缩文件转换"""
        mock_convert.return_value = True
        result = self.converter.convert('test.zip', 'test.tar', 'zip', 'tar')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()