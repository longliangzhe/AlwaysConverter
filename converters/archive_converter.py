#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
压缩文件转换器
支持ZIP、RAR、7Z、TAR、GZ等压缩格式转换
"""

import os
import zipfile
import tarfile
from core.base_converter import BaseConverter
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    import rarfile
    HAS_RARFILE = True
except ImportError:
    HAS_RARFILE = False
    logger.warning("rarfile库未安装，RAR格式支持将受限")

try:
    import py7zr
    HAS_PY7ZR = True
except ImportError:
    HAS_PY7ZR = False
    logger.warning("py7zr库未安装，7Z格式支持将受限")


class ArchiveConverter(BaseConverter):
    """压缩文件转换器"""
    
    def __init__(self, config):
        super().__init__(config)
        self.has_rar = HAS_RARFILE
        self.has_7z = HAS_PY7ZR
    
    def convert(self, input_path: str, output_path: str, source_format: str, target_format: str) -> bool:
        """
        执行压缩文件转换
        
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
            
            # 根据源格式和目标格式选择转换方法
            if source_format == 'zip' and target_format == 'tar':
                return self._zip_to_tar(input_path, output_path)
            elif source_format == 'tar' and target_format == 'zip':
                return self._tar_to_zip(input_path, output_path)
            elif source_format == 'zip' and target_format == 'gz':
                return self._zip_to_tar_gz(input_path, output_path)
            else:
                logger.warning(f"不支持的压缩文件转换: {source_format} -> {target_format}")
                return False
                
        except Exception as e:
            logger.error(f"压缩文件转换失败: {str(e)}")
            return False
    
    def _zip_to_tar(self, input_path: str, output_path: str) -> bool:
        """ZIP转TAR"""
        try:
            # 创建临时目录解压ZIP文件
            temp_dir = "temp_extract"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # 解压ZIP文件
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 创建TAR文件
            with tarfile.open(output_path, 'w') as tar_ref:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, temp_dir)
                        tar_ref.add(file_path, arcname=arc_name)
            
            # 清理临时目录
            self._cleanup_temp_dir(temp_dir)
            
            logger.info(f"ZIP转TAR成功: {input_path} -> {output_path}")
            return True
        except Exception as e:
            logger.error(f"ZIP转TAR失败: {str(e)}")
            return False
    
    def _tar_to_zip(self, input_path: str, output_path: str) -> bool:
        """TAR转ZIP"""
        try:
            # 创建临时目录解压TAR文件
            temp_dir = "temp_extract"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # 解压TAR文件
            with tarfile.open(input_path, 'r') as tar_ref:
                tar_ref.extractall(temp_dir)
            
            # 创建ZIP文件
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, temp_dir)
                        zip_ref.write(file_path, arcname=arc_name)
            
            # 清理临时目录
            self._cleanup_temp_dir(temp_dir)
            
            logger.info(f"TAR转ZIP成功: {input_path} -> {output_path}")
            return True
        except Exception as e:
            logger.error(f"TAR转ZIP失败: {str(e)}")
            return False
    
    def _zip_to_tar_gz(self, input_path: str, output_path: str) -> bool:
        """ZIP转TAR.GZ"""
        try:
            # 创建临时目录解压ZIP文件
            temp_dir = "temp_extract"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # 解压ZIP文件
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 创建TAR.GZ文件
            with tarfile.open(output_path, 'w:gz') as tar_ref:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, temp_dir)
                        tar_ref.add(file_path, arcname=arc_name)
            
            # 清理临时目录
            self._cleanup_temp_dir(temp_dir)
            
            logger.info(f"ZIP转TAR.GZ成功: {input_path} -> {output_path}")
            return True
        except Exception as e:
            logger.error(f"ZIP转TAR.GZ失败: {str(e)}")
            return False
    
    def _cleanup_temp_dir(self, temp_dir: str):
        """清理临时目录"""
        try:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"清理临时目录失败: {str(e)}")