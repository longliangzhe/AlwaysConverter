#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片转换器
支持JPG、PNG、GIF、BMP、TIFF、WEBP等图片格式转换
"""

import os
from core.base_converter import BaseConverter
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    logger.warning("Pillow库未安装，图片转换功能将受限")


class ImageConverter(BaseConverter):
    """图片转换器"""
    
    def __init__(self, config):
        super().__init__(config)
        self.supported = HAS_PILLOW
        # Pillow支持的格式映射
        self.format_map = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'gif': 'GIF',
            'bmp': 'BMP',
            'tiff': 'TIFF',
            'webp': 'WEBP'
        }
    
    def convert(self, input_path: str, output_path: str, source_format: str, target_format: str) -> bool:
        """
        执行图片转换
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            source_format: 源文件格式
            target_format: 目标文件格式
            
        Returns:
            转换是否成功
        """
        if not self.supported:
            logger.error("缺少必要的图片处理库(Pillow)")
            return False
        
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 打开图片
            with Image.open(input_path) as img:
                # 处理RGBA到RGB的转换（某些格式不支持透明度）
                if target_format in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # 保存图片
                save_format = self.format_map.get(target_format, target_format.upper())
                img.save(output_path, format=save_format)
            
            logger.info(f"图片转换成功: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"图片转换失败: {str(e)}")
            return False