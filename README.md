# PDF Text Watermark Remover｜PDF水印文字移除工具
<img width="712" alt="image" src="https://github.com/user-attachments/assets/278df6e5-20cb-4b19-9add-d490554a270c" />
<img width="568" alt="image" src="https://github.com/user-attachments/assets/c983825b-59b2-4648-a313-4da8ab82b139" />

[English](README.md) | [中文说明](README_CN.md)

A powerful desktop application that intelligently removes text-based watermarks from PDF files while preserving the original content. The application features a user-friendly GUI and supports customizable watermark detection.

## Features

- 🔍 Smart watermark detection based on customizable keywords
- 🗑️ Selective removal of text watermarks without affecting document content
- 🖼️ Handles both text and form-based watermarks
- 🎯 Preserves document quality and formatting
- 🔧 User-friendly graphical interface
- ⚙️ Customizable watermark keywords
- 📊 Detailed watermark detection reports
- 💾 Batch processing support

## Quick Start

### Method 1: Using Pre-built Executables (Recommended)

1. Download the latest release for your platform from the [releases page](https://github.com/yourusername/pdf-watermark-remover/releases):
   - Windows: `PDF-Watermark-Remover.exe`
   - macOS: `PDF-Watermark-Remover.app`

2. Run the application:
   - Windows: Double-click the `.exe` file
   - macOS: Double-click the `.app` file
     > Note: If you see "app can't be opened" on macOS, follow these steps:
     > 1. Find the app in Finder
     > 2. Control-click the app icon
     > 3. Choose "Open" from the menu
     > 4. Click "Open" in the dialog box
     >
     > Or:
     > 1. Open "System Preferences" > "Security & Privacy"
     > 2. Click the "General" tab
     > 3. Click the lock icon and enter your password
     > 4. Click "Open Anyway"

### Method 2: Installing from Source

1. Ensure you have Python 3.7 or higher installed
2. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-watermark-remover.git
cd pdf-watermark-remover
```

3. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python gui.py
```

### Building from Source

To create your own executable:
```bash
python build.py
```
The executable will be created in the `dist` directory.

## Usage Guide

1. After launching, the interface is straightforward:
   - File selection area at the top
   - Progress display in the middle
   - Function buttons at the bottom

2. Basic workflow:
   - Click "Browse" to select your PDF file
   - Click "Check Watermarks" to preview watermarks
   - Click "Remove Watermarks" to process
   - Choose where to save the processed file

3. Watermark keyword management:
   - Click "Manage Keywords" to open settings
   - Add or remove keywords (one per line)
   - Supports both English and other languages
   - Click "Save" to apply changes

## Default Watermark Keywords

The application comes with pre-configured keywords for common watermarks:
```
- Review Copy
- University Press
- Copyright Material
- Review Only
- Not for Redistribution
- International
```

## Acknowledgments

- [pikepdf](https://github.com/pikepdf/pikepdf) for PDF processing
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
- [gaoconghui](https://gist.github.com/gaoconghui/f21057c41c9386d0dcf32691c2d24692)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 


