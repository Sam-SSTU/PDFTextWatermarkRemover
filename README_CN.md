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

## 常见问题

1. **程序无法启动**
   - Windows：确保安装了 Visual C++ 运行库
   - Mac：如果提示"无法打开"，请按以下步骤操作：
     1. 在 Finder 中找到应用程序
     2. 按住 Control 键并点击应用程序图标
     3. 从菜单中选择"打开"
     4. 在弹出的对话框中点击"打开"
     
     或者：
     1. 打开"系统偏好设置" > "安全性与隐私"
     2. 点击"通用"标签
     3. 点击左下角的锁图标并输入密码
     4. 选择"仍要打开"或"允许"

2. **无法检测到水印**
   - 检查水印关键词设置
   - 确认 PDF 文件没有加密

3. **处理后的文件很大**
   - 这是正常现象，因为需要保持文档质量

## 技术实现

程序使用多种技术来处理水印：

- 文本分析：使用正则表达式识别水印文本
- 表单处理：检测和过滤表单对象中的水印
- 元数据处理：清理文档元数据中的水印信息
- 资源管理：处理文档资源字典
- 内容处理：分析和修改内容流

## 开发计划

- [ ] 添加批量处理功能
- [ ] 支持图片水印识别
- [ ] 添加处理进度显示
- [ ] 优化处理速度
- [ ] 添加更多语言支持

## 注意事项

1. 使用前请确保：
   - 您有权修改要处理的 PDF 文件
   - 已经备份原始文件
   - 遵守相关法律法规

2. 安全建议：
   - 不要处理来源不明的 PDF 文件
   - 定期更新程序到最新版本
   - 在处理重要文件时先进行测试

## 技术支持

- 提交问题：通过 GitHub Issues
- 功能建议：欢迎提交 Pull Request
- 使用咨询：可以通过 Discussions 讨论

## 致谢

感谢以下开源项目：
- [pikepdf](https://github.com/pikepdf/pikepdf)：PDF 处理核心库
- [tkinter](https://docs.python.org/3/library/tkinter.html)：GUI 框架
- 其他贡献者和开源社区

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。 