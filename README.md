# PDF Text Watermark Remover

A powerful desktop application that intelligently removes text-based watermarks from PDF files while preserving the original content. The application features a user-friendly GUI and supports customizable watermark detection.

![Application Screenshot](screenshot.png)

## Features

- 🔍 Smart watermark detection based on customizable keywords
- 🗑️ Selective removal of text watermarks without affecting document content
- 🖼️ Handles both text and form-based watermarks
- 🎯 Preserves document quality and formatting
- 🔧 User-friendly graphical interface
- ⚙️ Customizable watermark keywords
- 📊 Detailed watermark detection reports
- 💾 Batch processing support

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

You can easily modify these keywords through the GUI interface.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Method 1: Using Pre-built Executables

1. Download the latest release for your platform:
   - Windows: `PDF-Watermark-Remover.exe`
   - macOS: `PDF-Watermark-Remover.app`

2. Double-click the executable to run the application

### Method 2: Installing from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-watermark-remover.git
cd pdf-watermark-remover
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python gui.py
```

### Building from Source

To create your own executable:
```bash
python build.py
```
The executable will be created in the `dist` directory.

## Usage

1. Launch the application
2. Click "Browse" to select your PDF file
3. (Optional) Click "Manage Keywords" to customize watermark detection
4. Click "Check Watermarks" to scan for watermarks in the document
5. Click "Remove Watermarks" to process the file
6. Select where to save the processed PDF

## Customizing Watermark Keywords

1. Click the "Manage Keywords" button
2. Add or remove keywords (one per line)
3. Click "Save" to apply changes
4. Click "Reset to Default" to restore original keywords

## Technical Details

The application uses several techniques to detect and remove watermarks:

- Text content analysis using regular expressions
- Form object detection and filtering
- Metadata cleaning
- Resource dictionary management
- Content stream processing

## Limitations

- Only removes text-based watermarks
- Does not affect image-based watermarks
- Cannot remove watermarks that are part of the main content
- May require multiple passes for complex documents

## Troubleshooting

### Common Issues

1. **Missing Text After Processing**
   - Check if watermark keywords are too generic
   - Adjust keywords to be more specific

2. **Watermarks Not Detected**
   - Verify that watermark text matches keywords
   - Try adding variations of the watermark text

3. **Application Won't Start**
   - Ensure Python and all dependencies are installed
   - Check system requirements

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [pikepdf](https://github.com/pikepdf/pikepdf) for PDF processing
- [tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Contact the maintainers

## Security Notice

This tool is designed for legitimate use cases only. Users are responsible for ensuring they have the right to modify PDF files they process. 

Ref:
https://gist.github.com/gaoconghui/f21057c41c9386d0dcf32691c2d24692
