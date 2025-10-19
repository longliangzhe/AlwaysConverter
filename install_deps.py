#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安装脚本
帮助用户安装所有必要的依赖
"""
import os
import sys
import platform
import subprocess
os.system("pip install loguru")
from utils.logger import get_logger

logger = get_logger(__name__)


def check_system():
    """检查操作系统类型"""
    system = platform.system().lower()
    if system == "windows":
        logger.info("检测到Windows系统")
        return "windows"
    elif system == "darwin":
        logger.info("检测到macOS系统")
        return "macos"
    elif system == "linux":
        logger.info("检测到Linux系统")
        return "linux"
    else:
        logger.warning(f"未知系统类型: {system}")
        return "unknown"


def install_system_deps(system):
    """安装系统依赖"""
    if system == "windows":
        logger.info("Windows系统无需额外系统依赖")
        return True
    elif system == "macos":
        logger.info("在macOS上安装libmagic...")
        try:
            # 检查是否安装了brew
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            # 安装libmagic
            subprocess.run(["brew", "install", "libmagic"], check=True)
            logger.info("libmagic安装成功")
            return True
        except subprocess.CalledProcessError:
            logger.error("安装libmagic失败，请确保已安装Homebrew")
            return False
        except FileNotFoundError:
            logger.error("未找到brew命令，请先安装Homebrew")
            return False
    elif system == "linux":
        logger.info("在Linux上安装libmagic...")
        try:
            # 尝试使用apt（Debian/Ubuntu）
            subprocess.run(["apt", "update"], check=True, capture_output=True)
            subprocess.run(["apt", "install", "-y", "libmagic1", "libmagic-dev"], check=True)
            logger.info("libmagic安装成功")
            return True
        except subprocess.CalledProcessError:
            try:
                # 尝试使用yum（CentOS/RHEL）
                subprocess.run(["yum", "install", "-y", "file-libs", "file-devel"], check=True)
                logger.info("libmagic安装成功")
                return True
            except subprocess.CalledProcessError:
                logger.error("安装libmagic失败，请手动安装")
                return False
        except FileNotFoundError:
            logger.error("未找到包管理器，请手动安装libmagic")
            return False
    return False


def install_python_deps():
    """安装Python依赖"""
    logger.info("安装Python依赖...")
    try:
        # 升级pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        # 安装requirements.txt中的依赖，指定编码方式
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            # 如果UTF-8编码失败，尝试其他编码方式
            logger.warning("使用UTF-8编码安装失败，尝试其他编码方式...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                   capture_output=True, text=True, encoding='latin1')
        
        if result.returncode == 0:
            logger.info("Python依赖安装成功")
            return True
        else:
            logger.error(f"安装Python依赖失败: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"安装Python依赖时发生异常: {e}")
        return False


def install_optional_deps():
    """安装可选依赖（如PyQt5用于图形界面）"""
    logger.info("安装可选依赖...")
    try:
        # 安装PyQt5
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"], check=True)
        logger.info("可选依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f"安装可选依赖失败: {e}")
        logger.warning("图形界面将无法使用，但命令行功能仍可正常使用")
        return False


def main():
    """主函数"""
    logger.info("开始安装AlwaysConverter依赖...")
    
    # 检查系统类型
    system = check_system()
    
    # 安装系统依赖
    if not install_system_deps(system):
        logger.warning("系统依赖安装失败，但将继续安装Python依赖")
    
    # 安装Python依赖
    if not install_python_deps():
        logger.error("依赖安装失败")
        sys.exit(1)
    
    # 安装可选依赖
    logger.info("是否安装图形界面依赖？(y/n): ")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            if install_optional_deps():
                logger.info("所有依赖（包括可选依赖）安装完成！")
                print("\n依赖安装成功！现在可以运行测试：")
                print("  python test_cli.py")
                print("或运行图形界面：")
                print("  python ui.py")
            else:
                logger.info("核心依赖安装完成，但可选依赖安装失败！")
                print("\n核心依赖安装成功！现在可以运行测试：")
                print("  python test_cli.py")
        else:
            logger.info("所有依赖安装完成！")
            print("\n依赖安装成功！现在可以运行测试：")
            print("  python test_cli.py")
    except (EOFError, KeyboardInterrupt):
        logger.info("跳过可选依赖安装")
        print("\n依赖安装成功！现在可以运行测试：")
        print("  python test_cli.py")


if __name__ == "__main__":
    main()