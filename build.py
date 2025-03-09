import os
import sys
import shutil
import platform
import subprocess
import PyInstaller.__main__

def clean_build_directories():
    """清理构建目录"""
    directories = ['build', 'dist']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)

def sign_mac_app():
    """为 Mac 应用程序签名"""
    if sys.platform == "darwin":
        try:
            # 创建临时证书
            subprocess.run([
                'codesign',
                '--force',
                '--deep',
                '--sign',
                '-',  # 使用临时证书
                'dist/PDF-Watermark-Remover.app'
            ], check=True)
            print("Mac 应用签名完成")
        except subprocess.CalledProcessError as e:
            print(f"Mac 应用签名失败: {e}")

def build_for_platform(target_platform):
    """为指定平台构建应用程序"""
    app_name = "PDF-Watermark-Remover"
    if target_platform == "win32":
        app_name += ".exe"
    
    # 基本配置
    icon = None
    if target_platform == "darwin":
        icon = "icon.icns"
    elif target_platform == "win32":
        icon = "icon.ico"
    
    # PyInstaller参数
    args = [
        'gui.py',
        f'--name={app_name}',
        '--onefile',
        '--windowed',
        '--clean',
        '--add-data=README.md:.',
    ]
    
    # 如果有图标文件，添加图标
    if icon and os.path.exists(icon):
        args.append(f'--icon={icon}')
    
    # 为Windows构建时添加特殊参数
    if target_platform == "win32":
        args.extend([
            '--runtime-hook=win_runtime_hook.py',
        ])
    
    # 运行PyInstaller
    try:
        if target_platform == "win32" and sys.platform == "darwin":
            # 在Mac上使用wine构建Windows版本
            cmd = ['wine', 'python', '-m', 'PyInstaller'] + args
            subprocess.run(cmd, check=True)
        else:
            PyInstaller.__main__.run(args)
        
        # 如果是 Mac 平台，进行签名
        if target_platform == "darwin":
            sign_mac_app()
        
        print(f"为 {target_platform} 平台构建完成！")
    except Exception as e:
        print(f"构建 {target_platform} 版本时出错: {str(e)}")

def create_win_runtime_hook():
    """创建Windows运行时钩子文件"""
    with open('win_runtime_hook.py', 'w') as f:
        f.write('''
import os
import sys

# 确保在Windows上正确加载依赖
if sys.platform == 'win32':
    import tkinter
    import tkinter.ttk
''')

def build_application():
    """构建应用程序"""
    # 清理旧的构建文件
    clean_build_directories()
    
    # 创建Windows运行时钩子
    create_win_runtime_hook()
    
    # 检查是否安装了wine
    if sys.platform == "darwin":
        try:
            subprocess.run(['wine', '--version'], capture_output=True, check=True)
            has_wine = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            has_wine = False
            print("警告: 未检测到wine，无法构建Windows版本")
            print("请使用 'brew install wine' 安装wine")
    
    # 构建当前平台版本
    build_for_platform(sys.platform)
    
    # 如果在Mac上且安装了wine，构建Windows版本
    if sys.platform == "darwin" and has_wine:
        print("\n开始构建Windows版本...")
        build_for_platform("win32")
    
    print("\n所有构建任务完成！")
    print("可执行文件位于 dist 目录")

if __name__ == "__main__":
    build_application() 