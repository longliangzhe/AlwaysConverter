#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AlwaysConverter PyQt5 增强图形界面
注意：请将此文件重命名为 ui.py 才能使用图形界面功能

功能：
1. 支持多种文件格式转换
2. 可视化界面操作
3. 转换进度显示
4. 日志信息展示
5. 增强UI设计（圆角按钮、图标等）
6. 多标签页设计（转换、设置、关于）
7. 高级设置选项
"""

import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QComboBox, QFileDialog, 
    QTextEdit, QProgressBar, QMessageBox, QGroupBox, QGridLayout,
    QCheckBox, QTabWidget, QListWidget, QSpinBox, QDoubleSpinBox,
    QSlider, QRadioButton, QButtonGroup, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QColor

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
    
    def __init__(self, input_file, output_file, target_format, options):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.target_format = target_format
        self.options = options
        
    def run(self):
        try:
            # 模拟转换过程
            self.log_updated.emit(f"开始转换: {self.input_file}")
            self.log_updated.emit(f"目标格式: {self.target_format}")
            
            # 显示转换选项
            if self.options:
                self.log_updated.emit("转换选项:")
                for key, value in self.options.items():
                    self.log_updated.emit(f"  {key}: {value}")
            
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

class RoundedButton(QPushButton):
    """圆角按钮类"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

class IconButton(QPushButton):
    """带图标的按钮类"""
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            
            QPushButton:hover {
                background-color: #1976D2;
            }
            
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        # 如果提供了图标路径，设置图标
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))

class AlwaysConverterUI(QMainWindow):
    """主界面类"""
    
    def __init__(self):
        super().__init__()
        self.conversion_thread = None
        self.initUI()
        
    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle('AlwaysConverter - 增强版通用文件格式转换工具')
        self.setGeometry(100, 100, 900, 700)
        
        # 设置样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: #e0e0e0;
                border-radius: 4px;
            }
            
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 8px;
                top: -1px;
            }
            
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #cccccc;
                border-bottom-color: #cccccc;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 5px;
            }
            
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom-color: #ffffff;
            }
            
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel('AlwaysConverter 增强版')
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 10px;
                margin: 5px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 创建标签页
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # 文件转换标签页
        self.create_conversion_tab(tab_widget)
        
        # 设置标签页
        self.create_settings_tab(tab_widget)
        
        # 关于标签页
        self.create_about_tab(tab_widget)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
        
        # 菜单栏
        self.create_menu()
        
    def create_conversion_tab(self, parent):
        """创建转换标签页"""
        conversion_tab = QWidget()
        parent.addTab(conversion_tab, "文件转换")
        
        layout = QVBoxLayout(conversion_tab)
        
        # 文件选择区域
        file_group = QGroupBox("文件选择")
        file_layout = QGridLayout(file_group)
        
        # 输入文件
        input_label = QLabel('输入文件:')
        self.input_line = QLineEdit()
        input_button = IconButton('浏览', None)
        input_button.clicked.connect(self.select_input_file)
        
        file_layout.addWidget(input_label, 0, 0)
        file_layout.addWidget(self.input_line, 0, 1)
        file_layout.addWidget(input_button, 0, 2)
        
        # 输出文件
        output_label = QLabel('输出文件:')
        self.output_line = QLineEdit()
        output_button = IconButton('浏览', None)
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
        
        layout.addWidget(file_group)
        
        # 转换控制区域
        control_layout = QHBoxLayout()
        self.convert_button = RoundedButton('开始转换')
        self.convert_button.clicked.connect(self.start_conversion)
        self.cancel_button = RoundedButton('取消')
        self.cancel_button.clicked.connect(self.cancel_conversion)
        self.cancel_button.setEnabled(False)
        
        control_layout.addWidget(self.convert_button)
        control_layout.addWidget(self.cancel_button)
        layout.addLayout(control_layout)
        
        # 进度区域
        progress_group = QGroupBox("转换进度")
        progress_layout = QVBoxLayout(progress_group)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        layout.addWidget(progress_group)
        
        # 日志区域
        log_group = QGroupBox("转换日志")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_group)
        
    def create_settings_tab(self, parent):
        """创建设置标签页"""
        settings_tab = QWidget()
        parent.addTab(settings_tab, "设置")
        
        layout = QVBoxLayout(settings_tab)
        
        # 常规设置
        general_group = QGroupBox("常规设置")
        general_layout = QVBoxLayout(general_group)
        
        self.auto_output_check = QCheckBox("自动设置输出文件名")
        self.auto_output_check.setChecked(True)
        general_layout.addWidget(self.auto_output_check)
        
        self.preserve_folder_check = QCheckBox("保持文件夹结构")
        general_layout.addWidget(self.preserve_folder_check)
        
        layout.addWidget(general_group)
        
        # 高级设置
        advanced_group = QGroupBox("高级设置")
        advanced_layout = QVBoxLayout(advanced_group)
        
        quality_layout = QHBoxLayout()
        quality_label = QLabel("图像质量:")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(95)
        self.quality_value = QLabel("95")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_value.setText(str(v))
        )
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value)
        advanced_layout.addLayout(quality_layout)
        
        # 线程数设置
        thread_layout = QHBoxLayout()
        thread_label = QLabel("转换线程数:")
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 16)
        self.thread_spin.setValue(4)
        thread_layout.addWidget(thread_label)
        thread_layout.addWidget(self.thread_spin)
        advanced_layout.addLayout(thread_layout)
        
        layout.addWidget(advanced_group)
        
        # 日志设置
        log_group = QGroupBox("日志设置")
        log_layout = QVBoxLayout(log_group)
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["INFO", "DEBUG", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText("INFO")
        log_layout.addWidget(QLabel("日志级别:"))
        log_layout.addWidget(self.log_level_combo)
        
        self.save_log_check = QCheckBox("保存日志到文件")
        log_layout.addWidget(self.save_log_check)
        
        layout.addWidget(log_group)
        
        # 占位符以填充空间
        layout.addStretch()
        
    def create_about_tab(self, parent):
        """创建关于标签页"""
        about_tab = QWidget()
        parent.addTab(about_tab, "关于")
        
        layout = QVBoxLayout(about_tab)
        
        # 标题
        title_label = QLabel('AlwaysConverter 增强版')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 功能列表
        features_group = QGroupBox("主要功能")
        features_layout = QVBoxLayout(features_group)
        
        features = [
            "支持文档格式: PDF, DOCX, TXT, RTF, ODT",
            "支持图片格式: JPG, PNG, GIF, BMP, TIFF, WEBP",
            "支持音频格式: MP3, WAV, FLAC, AAC, OGG",
            "支持视频格式: MP4, AVI, MKV, MOV",
            "支持压缩格式: ZIP, RAR, 7Z",
            "增强UI设计（圆角按钮、图标等）",
            "多标签页设计（转换、设置、关于）",
            "高级设置选项",
            "转换进度显示",
            "实时日志信息"
        ]
        
        for feature in features:
            label = QLabel(f"• {feature}")
            label.setWordWrap(True)
            features_layout.addWidget(label)
            
        layout.addWidget(features_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.about_button = RoundedButton("关于")
        self.about_button.clicked.connect(self.show_about)
        button_layout.addWidget(self.about_button)
        
        self.github_button = IconButton("GitHub", None)
        self.github_button.clicked.connect(self.open_github)
        button_layout.addWidget(self.github_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 占位符以填充空间
        layout.addStretch()
        
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
        
        # 设置菜单
        settings_menu = menubar.addMenu('设置')
        
        settings_action = settings_menu.addAction('设置')
        settings_action.triggered.connect(self.show_settings)
        
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
            
            # 如果启用了自动输出文件名，自动生成输出文件名
            if self.auto_output_check.isChecked():
                self.auto_generate_output_file(file_path)
            
    def auto_generate_output_file(self, input_file):
        """自动生成输出文件名"""
        if input_file:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            target_format = self.format_combo.currentText()
            output_file = f"{base_name}.{target_format}"
            self.output_line.setText(output_file)
            
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
            
    def get_conversion_options(self):
        """获取转换选项"""
        options = {
            "图像质量": self.quality_slider.value(),
            "线程数": self.thread_spin.value(),
            "保持文件夹结构": self.preserve_folder_check.isChecked(),
            "日志级别": self.log_level_combo.currentText()
        }
        return options
            
    def start_conversion(self):
        """开始转换"""
        input_file = self.input_line.text()
        output_file = self.output_line.text()
        target_format = self.format_combo.currentText()
        options = self.get_conversion_options()
        
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
            input_file, output_file, target_format, options
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
            "关于 AlwaysConverter 增强版",
            "AlwaysConverter 增强版 v1.0.0\n\n"
            "一个通用文件格式转换工具，支持多种文档、图片、音频、视频和压缩文件格式的转换。\n\n"
            "主要功能：\n"
            "- 支持多种文档格式转换\n"
            "- 图片格式转换\n"
            "- 音频格式转换\n"
            "- 视频格式转换\n"
            "- 压缩文件处理\n"
            "- 命令行和图形界面双模式\n"
            "- 增强UI设计（圆角按钮、图标等）\n"
            "- 多标签页设计（转换、设置、关于）\n"
            "- 高级设置选项"
        )
        
    def open_github(self):
        """打开GitHub页面"""
        QMessageBox.information(
            self, 
            "GitHub", 
            "AlwaysConverter 项目地址:\n"
            "https://github.com/AlwaysConverter/AlwaysConverter"
        )
        
    def show_settings(self):
        """显示设置对话框"""
        # 这里可以实现一个更复杂的设置对话框
        QMessageBox.information(
            self, 
            "设置", 
            "设置功能已在设置标签页中提供。"
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