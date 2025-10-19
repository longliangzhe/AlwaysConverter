# AlwaysConverter

一个功能强大的多格式文件转换器，支持超过80种文件格式的转换。

## 🖼 图形界面

AlwaysConverter 提供了现代化的图形界面，方便用户进行文件格式转换操作。

### 使用方法

1. 将 `ui.example.py` 文件重命名为 `ui.py`
2. 运行命令：`python ui.py`

### 界面功能特点

- 拖拽文件支持
- 实时转换进度显示
- 转换日志查看
- 多种格式选择
- 美观的现代化界面设计

### 增强版图形界面

项目还提供了一个增强版的图形界面 `ui_enhanced.py`，包含更精美的圆角按钮和图标设计。

增强版界面特性：
- 圆角按钮设计，具有悬停和按下状态的视觉反馈
- 独特的图标按钮（📁📂🚀⏹️🔄等）
- 渐变背景和半透明组件
- 改进的颜色方案和字体样式
- 更直观的用户体验

#### 使用方法

有两种方式使用增强版界面：

**方法一：使用启动脚本（推荐）**
```bash
python start_enhanced_ui.py
```
此脚本会自动处理文件重命名并启动增强版界面。

**方法二：手动重命名**
1. 将 `ui_enhanced.py` 文件重命名为 `ui.py`
2. 运行命令：`python ui.py`

### 安装图形界面依赖

可以通过以下方式安装图形界面所需的依赖：

#### 使用安装脚本（推荐）

```bash
python install_deps.py
```

在安装过程中，选择安装图形界面依赖。

#### 手动安装

```bash
pip install PyQt5
```

## 功能特点

- 支持超过80种文件格式转换
- 模块化设计，易于扩展
- 命令行界面，操作简单
- 支持批量转换
- 详细的日志记录
- 配置文件驱动

## 支持的文件格式

### 文档格式
- PDF, DOC, DOCX, TXT, RTF, ODT
- XLS, XLSX, PPT, PPTX

### 图片格式
- JPG, JPEG, PNG, GIF, BMP, TIFF
- WEBP, SVG, ICO

### 音频格式
- MP3, WAV, FLAC, AAC, OGG
- WMA, M4A, OPUS

### 视频格式
- MP4, AVI, MKV, MOV, WMV
- FLV, WEBM, M4V

### 压缩格式
- ZIP, RAR, 7Z, TAR, GZ, BZ2

### 其他格式
- 支持通用文件格式转换

## 安装

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd AlwaysConverter
   ```

2. 安装系统依赖（根据操作系统）：
   - **Windows**:
     ```bash
     # 下载并安装libmagic库
     # 访问 https://github.com/pidydx/libmagicwin64 获取预编译的libmagic库
     ```
   - **macOS**:
     ```bash
     brew install libmagic
     ```
   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get update
     sudo apt-get install libmagic1 libmagic-dev
     ```
   - **CentOS/RHEL**:
     ```bash
     sudo yum install file-libs file-devel
     ```

3. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```

   或者使用安装脚本：
   ```bash
   python install_deps.py
   ```

## 使用方法

### 命令行使用
```bash
python main.py --input input_file.ext --output output_file.ext
```

### 编程接口
```python
from core.converter import FileConverter
from utils.config import load_config

# 加载配置
config = load_config()

# 创建转换器实例
converter = FileConverter(config)

# 执行转换
success = converter.convert('input.pdf', 'output.docx', 'pdf', 'docx')
```

## 项目结构

```
AlwaysConverter/
├── config/              # 配置文件
├── converters/          # 各种文件格式转换器
├── core/                # 核心模块
├── utils/               # 工具模块
├── tests/               # 测试文件
├── main.py             # 主程序入口
├── requirements.txt    # 依赖列表
└── README.md           # 说明文档
```

## 配置

配置文件位于 `config/config.yaml`，可以修改支持的格式和转换器设置。

## 测试

运行测试:
```
python -m pytest tests/
```

或运行测试脚本:
```
python test_cli.py
```

## 扩展

要添加新的文件格式支持:

1. 在 `converters/` 目录下创建新的转换器类
2. 继承 `BaseConverter` 类并实现 `convert` 方法
3. 在 `config/config.yaml` 中添加转换器配置
4. 在 `requirements.txt` 中添加必要的依赖

## 许可证

MIT License