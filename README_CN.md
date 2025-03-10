# PDF 水印移除工具

[English](README.md) | 中文说明

一款功能强大的桌面应用程序，能够智能识别并移除 PDF 文件中的文字水印，同时保持原始内容不变。该应用程序具有用户友好的图形界面，支持自定义水印检测。

## 主要功能

- 🔍 基于自定义关键词的智能水印检测
- 🗑️ 选择性移除文字水印，不影响文档内容
- 🖼️ 支持文本和表单类型的水印
- 🎯 保持文档质量和格式
- 🔧 用户友好的图形界面
- ⚙️ 可自定义水印关键词
- 📊 详细的水印检测报告
- 💾 支持批量处理

## 快速开始

### 方法一：直接使用（推荐）

1. 从[发布页面](https://github.com/yourusername/pdf-watermark-remover/releases)下载最新版本：
   - Windows 用户：下载 `PDF-Watermark-Remover.exe`
   - macOS 用户：下载 `PDF-Watermark-Remover.app`

2. 双击运行程序即可使用

### 方法二：从源码运行

1. 确保已安装 Python 3.7 或更高版本
2. 克隆仓库并进入目录：
```bash
git clone https://github.com/yourusername/pdf-watermark-remover.git
cd pdf-watermark-remover
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行程序：
```bash
python gui.py
```

## 使用说明

1. 启动程序后，界面简单直观：
   - 顶部有文件选择区
   - 中部是进度显示区
   - 底部是功能按钮区

2. 基本操作流程：
   - 点击"浏览"选择需要处理的 PDF 文件
   - 点击"检查水印"可以预览文件中的水印
   - 点击"移除水印"开始处理
   - 选择保存位置，等待处理完成

3. 水印关键词管理：
   - 点击"管理关键词"打开设置窗口
   - 可以添加、删除或修改水印关键词
   - 每行输入一个关键词
   - 支持中英文关键词

## 默认水印关键词

预设的水印关键词包括：
```
- Review Copy
- University Press
- Copyright Material
- Review Only
- Not for Redistribution
- International
```

## 致谢

感谢以下开源项目：
- [pikepdf](https://github.com/pikepdf/pikepdf)：PDF 处理核心库
- [tkinter](https://docs.python.org/3/library/tkinter.html)：GUI 框架
- 其他贡献者和开源社区

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。 