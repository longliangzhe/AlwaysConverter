#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AlwaysConverter PyQt5 基础图形界面
注意：请将此文件重命名为 ui.py 才能使用图形界面功能

功能：
1. 支持多种文件格式转换
2. 可视化界面操作
3. 转换进度显示
4. 日志信息展示
"""

import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QComboBox, QFileDialog, 
    QTextEdit, QProgressBar, QMessageBox, QGroupBox, QGridLayout,
    QCheckBox, QTabWidget, QListWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

# 检查文件名，确保已重命名为ui.py或通过环境变量绕过检查
if os.path.basename(__file__) != "ui.py" and not os.environ.get('ALWAYS_CONVERTER_UI'):
    print("请将此文件重命名为 ui.py 才能使用图形界面功能")
    sys.exit(1)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversionWorker(QThread):
    """转换工作线程"""
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)
    conversion_finished = pyqtSignal(bool, str)
    
    def __init__(self, input_file, output_file, target_format):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.target_format = target_format
        
    def run(self):
        try:
            # 模拟转换过程
            self.log_updated.emit(f"开始转换: {self.input_file}")
            self.log_updated.emit(f"目标格式: {self.target_format}")
            
            for i in range(101):
                # 模拟转换进度
                self.progress_updated.emit(i)
                if i % 20 == 0:
                    self.log_updated.emit(f"转换进度: {i}%")
                self.msleep(50)  # 模拟处理时间
                
            self.log_updated.emit(f"转换完成: {self.output_file}")
            self.conversion_finished.emit(True, "文件转换成功!")
            
        except Exception as e:
            self.log_updated.emit(f"转换失败: {str(e)}")
            self.conversion_finished.emit(False, f"转换失败: {str(e)}")

class AlwaysConverterUI(QMainWindow):
    """主界面类"""
    
    def __init__(self):
        super().__init__()
        self.conversion_thread = None
        self.initUI()
        
    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('AlwaysConverter - 通用文件格式转换工具')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel('AlwaysConverter')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QGridLayout(file_group)
        
        # 输入文件
        input_label = QLabel('输入文件:')
        self.input_line = QLineEdit()
        input_button = QPushButton('浏览')
        input_button.clicked.connect(self.select_input_file)
        
        file_layout.addWidget(input_label, 0, 0)
        file_layout.addWidget(self.input_line, 0, 1)
        file_layout.addWidget(input_button, 0, 2)
        
        # 输出文件
        output_label = QLabel('输出文件:')
        self.output_line = QLineEdit()
        output_button = QPushButton('浏览')
        output_button.clicked.connect(self.select_output_file)
        
        file_layout.addWidget(output_label, 1, 0)
        file_layout.addWidget(self.output_line, 1, 1)
        file_layout.addWidget(output_button, 1, 2)
        
        # 格式选择
        format_label = QLabel('目标格式:')
        self.format_combo = QComboBox()
        self.populate_format_combo()
        
        file_layout.addWidget(format_label, 2, 0)
        file_layout.addWidget(self.format_combo, 2, 1, 1, 2)
        
        main_layout.addWidget(file_group)
        
        # 转换控制区域
        control_layout = QHBoxLayout()
        self.convert_button = QPushButton('开始转换')
        self.convert_button.clicked.connect(self.start_conversion)
        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.cancel_conversion)
        self.cancel_button.setEnabled(False)
        
        control_layout.addWidget(self.convert_button)
        control_layout.addWidget(self.cancel_button)
        main_layout.addLayout(control_layout)
        
        # 进度区域
        progress_group = QGroupBox("转换进度")
        progress_layout = QVBoxLayout(progress_group)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        main_layout.addWidget(progress_group)
        
        # 日志区域
        log_group = QGroupBox("转换日志")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        main_layout.addWidget(log_group)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
        
        # 菜单栏
        self.create_menu()
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        open_action = file_menu.addAction('打开文件')
        open_action.triggered.connect(self.select_input_file)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('退出')
        exit_action.triggered.connect(self.close)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = help_menu.addAction('关于')
        about_action.triggered.connect(self.show_about)
        
    def populate_format_combo(self):
        """填充格式选择下拉框"""
        formats = [
            "pdf", "docx", "txt", "rtf", "odt",
            "jpg", "png", "gif", "bmp", "tiff", "webp",
            "mp3", "wav", "flac", "aac", "ogg",
            "mp4", "avi", "mkv", "mov",
            "zip", "rar", "7z"
        ]
        
        self.format_combo.addItems(formats)
        
    def select_input_file(self):
        """选择输入文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择输入文件", 
            "", 
            "所有文件 (*.*)"
        )
        
        if file_path:
            self.input_line.setText(file_path)
            self.statusBar().showMessage(f'已选择输入文件: {file_path}')
            
    def select_output_file(self):
        """选择输出文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "选择输出文件", 
            "", 
            "所有文件 (*.*)"
        )
        
        if file_path:
            self.output_line.setText(file_path)
            self.statusBar().showMessage(f'已选择输出文件: {file_path}')
            
    def start_conversion(self):
        """开始转换"""
        input_file = self.input_line.text()
        output_file = self.output_line.text()
        target_format = self.format_combo.currentText()
        
        # 验证输入
        if not input_file:
            QMessageBox.warning(self, "警告", "请选择输入文件")
            return
            
        if not output_file:
            QMessageBox.warning(self, "警告", "请选择输出文件")
            return
            
        if not os.path.exists(input_file):
            QMessageBox.critical(self, "错误", "输入文件不存在")
            return
            
        # 禁用转换按钮，启用取消按钮
        self.convert_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # 清空日志
        self.log_text.clear()
        
        # 启动转换线程
        self.conversion_thread = ConversionWorker(
            input_file, output_file, target_format
        )
        self.conversion_thread.progress_updated.connect(self.update_progress)
        self.conversion_thread.log_updated.connect(self.update_log)
        self.conversion_thread.conversion_finished.connect(self.conversion_finished)
        self.conversion_thread.start()
        
        self.statusBar().showMessage("正在转换...")
        
    def cancel_conversion(self):
        """取消转换"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.terminate()
            self.conversion_thread.wait()
            
        self.convert_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.statusBar().showMessage("转换已取消")
        self.log_text.append("转换已取消")
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        
    def update_log(self, message):
        """更新日志"""
        self.log_text.append(message)
        # 自动滚动到最新日志
        self.log_text.moveCursor(self.log_text.textCursor().End)
        
    def conversion_finished(self, success, message):
        """转换完成回调"""
        self.convert_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if success:
            self.statusBar().showMessage("转换完成")
            QMessageBox.information(self, "成功", message)
        else:
            self.statusBar().showMessage("转换失败")
            QMessageBox.critical(self, "错误", message)
            
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于 AlwaysConverter",
            "AlwaysConverter v1.0.0\n\n"
            "一个通用文件格式转换工具，支持多种文档、图片、音频、视频和压缩文件格式的转换。\n\n"
            "主要功能：\n"
            "- 支持多种文档格式转换\n"
            "- 图片格式转换\n"
            "- 音频格式转换\n"
            "- 视频格式转换\n"
            "- 压缩文件处理\n"
            "- 命令行和图形界面双模式"
        )

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("AlwaysConverter")
    app.setApplicationVersion("1.0.0")
    
    # 创建并显示主窗口
    window = AlwaysConverterUI()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()