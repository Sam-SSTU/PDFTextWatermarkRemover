import os
import sys
import shutil
import platform
import subprocess
import PyInstaller.__main__
import time

def clean_build_directories():
    """清理构建目录"""
    directories = ['build', 'dist']
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)

def sign_mac_app():
    """为 Mac 应用程序签名并设置权限"""
    if sys.platform == "darwin":
        try:
            # 设置应用程序权限
            app_path = 'dist/PDF-Watermark-Remover.app'
            
            # 添加必要的权限到 entitlements 文件
            entitlements_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>'''
            
            with open('entitlements.plist', 'w') as f:
                f.write(entitlements_content)
            
            # 移除所有现有的扩展属性
            subprocess.run(['xattr', '-cr', app_path], check=True)
            
            # 使用 codesign 进行签名
            subprocess.run([
                'codesign',
                '--force',
                '--deep',
                '--sign',
                '-',  # 使用临时证书
                '--entitlements',
                'entitlements.plist',
                '--options', 'runtime',
                app_path
            ], check=True)
            
            # 验证签名
            subprocess.run(['codesign', '--verify', '--verbose', app_path], check=True)
            
            # 清理临时文件
            if os.path.exists('entitlements.plist'):
                os.remove('entitlements.plist')
                
            print("Mac 应用签名完成")
            print("提示: 首次运行时，请在 Finder 中右键点击应用程序，选择'打开'")
            
        except subprocess.CalledProcessError as e:
            print(f"Mac 应用签名失败: {e}")
            print("提示: 您仍可以通过右键点击应用程序并选择'打开'来运行")

def create_dmg():
    """创建 DMG 文件"""
    if platform.system() != 'Darwin':
        return

    try:
        # 创建临时目录
        dmg_temp = 'dmg_temp'
        if os.path.exists(dmg_temp):
            shutil.rmtree(dmg_temp)
        os.makedirs(dmg_temp)

        # 复制应用程序到临时目录
        shutil.copytree('dist/PDF-Watermark-Remover.app', os.path.join(dmg_temp, 'PDF-Watermark-Remover.app'))

        # 使用 create-dmg 创建 DMG 文件
        subprocess.run([
            'create-dmg',
            '--volname', 'PDF-Watermark-Remover',
            '--window-pos', '200', '120',
            '--window-size', '600', '300',
            '--icon-size', '100',
            '--icon', 'PDF-Watermark-Remover.app', '175', '120',
            '--hide-extension', 'PDF-Watermark-Remover.app',
            '--app-drop-link', '425', '120',
            'dist/PDF-Watermark-Remover.dmg',
            dmg_temp
        ], check=True)

        # 清理临时目录
        shutil.rmtree(dmg_temp)
        print("DMG 文件创建成功！")

    except subprocess.CalledProcessError as e:
        print(f"创建 DMG 文件失败: {e}")
        print("请确保已安装 create-dmg 工具：brew install create-dmg")
    except Exception as e:
        print(f"创建 DMG 文件时发生错误: {e}")

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
        
        # 如果是 Mac 平台，进行签名和打包
        if target_platform == "darwin":
            sign_mac_app()
            create_dmg()  # 创建 DMG 文件
        
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