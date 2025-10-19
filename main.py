#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AlwaysConverter - 一个支持超过80种文件类型的Python文件转换器
主程序入口
"""

import os
import sys
import click
from core.converter import FileConverter
from utils.logger import get_logger
from utils.config import load_config

# 检查是否有图形界面支持
def has_gui():
    """检查是否存在ui.py文件"""
    return os.path.exists(os.path.join(os.path.dirname(__file__), 'ui', 'main.py'))

def launch_gui():
    """启动图形界面"""
    try:
        # 添加当前目录到Python路径
        sys.path.insert(0, os.path.dirname(__file__))
        
        # 设置环境变量以绕过文件名检查
        os.environ['ALWAYS_CONVERTER_UI'] = '1'
        
        # 直接调用UI的main函数
        from ui.main import main as ui_main
        ui_main()
        return True
    except ImportError as e:
        print(f"无法启动图形界面: {e}")
        return False
    except Exception as e:
        print(f"启动图形界面时发生错误: {e}")
        return False

logger = get_logger(__name__)


def show_supported_formats(config_path='config/config.yaml'):
    """显示支持的格式"""
    try:
        # 加载配置
        config_data = load_config(config_path)
        
        # 创建转换器实例
        converter = FileConverter(config_data)
        
        # 获取支持的格式
        supported_formats = converter.get_supported_formats()
        
        print("支持的文件格式:")
        print("=" * 50)
        
        for category, formats in supported_formats.items():
            print(f"\n{category.upper()}:")
            print(f"  输入格式: {', '.join(formats['input'])}")
            print(f"  输出格式: {', '.join(formats['output'])}")
    except Exception as e:
        logger.error(f"获取支持格式时发生错误: {str(e)}")
        sys.exit(1)


def interactive_mode(config_path='config/config.yaml'):
    """交互式模式"""
    try:
        # 加载配置
        config_data = load_config(config_path)
        
        # 创建转换器实例
        converter = FileConverter(config_data)
        
        print("AlwaysConverter 交互式模式")
        print("=" * 30)
        
        while True:
            print("\n请选择操作:")
            print("1. 转换文件")
            print("2. 查看支持的格式")
            print("3. 退出")
            
            choice = input("\n请输入选项 (1-3): ").strip()
            
            if choice == '1':
                input_path = input("请输入输入文件路径: ").strip()
                if not input_path:
                    print("错误: 输入文件路径不能为空")
                    continue
                    
                if not os.path.exists(input_path):
                    print(f"错误: 输入文件不存在: {input_path}")
                    continue
                    
                output_path = input("请输入输出文件路径: ").strip()
                if not output_path:
                    print("错误: 输出文件路径不能为空")
                    continue
                    
                # 确保输出目录存在
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    
                target_format = input("请输入目标格式 (可选，留空则从输出文件扩展名推断): ").strip()
                if not target_format:
                    _, ext = os.path.splitext(output_path)
                    target_format = ext[1:].lower() if ext else None
                    
                    if not target_format:
                        print("错误: 无法确定目标格式，请指定目标格式或在输出文件名中包含扩展名")
                        continue
                
                # 执行转换
                print(f"正在转换 {input_path} 到 {output_path}...")
                success = converter.convert(input_path, output_path, target_format)
                
                if success:
                    print(f"转换成功: {output_path}")
                else:
                    print(f"转换失败")
                
            elif choice == '2':
                show_supported_formats(config_path)
                
            elif choice == '3':
                print("再见!")
                break
                
            else:
                print("无效选项，请重新输入")
    except Exception as e:
        logger.error(f"交互式模式中发生错误: {str(e)}")
        sys.exit(1)


@click.command()
@click.option('--input', '-i', help='输入文件路径')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--format', '-f', help='目标文件格式')
@click.option('--config', '-c', default='config/config.yaml', help='配置文件路径')
@click.option('--list', '-l', is_flag=True, help='显示支持的格式')
@click.option('--interactive', '-I', is_flag=True, help='进入交互式模式')
@click.option('--gui', '-g', is_flag=True, help='启动图形界面')
def main(input, output, format, config, list, interactive, gui):
    """主程序入口"""
    # 如果指定了--gui参数，则启动图形界面
    if gui:
        if has_gui():
            if launch_gui():
                return
            else:
                print("启动图形界面失败")
                sys.exit(1)
        else:
            print("未找到图形界面文件")
            sys.exit(1)
    
    # 如果指定了--list参数，则显示支持的格式
    if list:
        show_supported_formats(config)
        return
    
    # 如果指定了--interactive参数，则进入交互式模式
    if interactive:
        interactive_mode(config)
        return
    
    # 如果指定了输入和输出文件，则执行转换
    if input and output and format:
        try:
            # 检查输入文件是否存在
            if not os.path.exists(input):
                logger.error(f"输入文件不存在: {input}")
                sys.exit(1)
            
            # 加载配置
            config_data = load_config(config)
            
            # 创建转换器实例
            converter = FileConverter(config_data)
            
            # 执行转换
            success = converter.convert(input, output, format)
            
            if success:
                logger.info(f"文件转换成功: {input} -> {output}")
                print(f"文件转换成功: {input} -> {output}")
            else:
                logger.error(f"文件转换失败: {input}")
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"转换过程中发生错误: {str(e)}")
            sys.exit(1)
    else:
        # 如果没有提供任何参数，检查是否有图形界面并启动
        if has_gui():
            if launch_gui():
                return
            else:
                print("启动图形界面失败")
        else:
            # 如果没有图形界面，显示帮助信息
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
            sys.exit(0)


if __name__ == '__main__':
    main()