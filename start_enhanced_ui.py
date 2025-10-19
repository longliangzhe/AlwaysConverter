#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AlwaysConverter 增强版UI启动脚本
此脚本会自动将 ui/enhanced.py 复制为 ui/main.py 并启动图形界面
"""

import os
import sys
import shutil
import subprocess

def main():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义文件路径
    enhanced_ui_path = os.path.join(current_dir, "ui", "enhanced.py")
    ui_path = os.path.join(current_dir, "ui", "main.py")
    backup_path = os.path.join(current_dir, "ui", "backup.py")
    
    # 检查增强版UI文件是否存在
    if not os.path.exists(enhanced_ui_path):
        print("❌ 错误: 找不到增强版UI文件 ui/enhanced.py")
        print("请确保 ui/enhanced.py 文件在项目 ui 目录中")
        return 1
    
    try:
        # 如果已存在 ui/main.py 文件，先备份
        if os.path.exists(ui_path) and not os.path.exists(backup_path):
            shutil.copy2(ui_path, backup_path)
            print(f"📝 已备份现有 ui/main.py 文件到 ui/backup.py")
        
        # 复制增强版UI文件为 ui/main.py
        shutil.copy2(enhanced_ui_path, ui_path)
        print("✅ 已将 ui/enhanced.py 复制为 ui/main.py")
        
        # 启动主程序（会自动检测并启动UI）
        print("🚀 正在启动增强版图形界面...")
        env = os.environ.copy()
        env['ALWAYS_CONVERTER_UI'] = '1'
        result = subprocess.run([sys.executable, os.path.join(current_dir, "main.py"), "--gui"], env=env)
        
        # 恢复备份文件（如果存在）
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, ui_path)
            os.remove(backup_path)
            print("🔄 已恢复原始 ui/main.py 文件")
        elif os.path.exists(ui_path):
            # 如果没有备份但有ui/main.py文件，删除它
            os.remove(ui_path)
            print("🧹 已清理临时 ui/main.py 文件")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ 启动增强版UI时发生错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())