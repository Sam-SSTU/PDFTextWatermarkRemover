import PyInstaller.__main__
import sys
import os

def build_app():
    # Determine the appropriate icon file extension based on the OS
    if sys.platform == 'darwin':  # macOS
        icon_file = 'icon.icns'
    elif sys.platform == 'win32':  # Windows
        icon_file = 'icon.ico'
    else:  # Linux
        icon_file = 'icon.png'

    # PyInstaller command line arguments
    args = [
        'gui.py',  # Your main GUI script
        '--name=PDF-Watermark-Remover',  # Name of the output executable
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window when running the app
        '--clean',  # Clean PyInstaller cache and remove temporary files
        f'--icon={icon_file}' if os.path.exists(icon_file) else None,  # Add icon if it exists
        '--add-data=README.md:.',  # Include README file
    ]

    # Remove None values from args
    args = [arg for arg in args if arg is not None]

    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_app() 