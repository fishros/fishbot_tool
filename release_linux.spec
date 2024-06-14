# -*- mode: python ; coding: utf-8 -*-
import os
import platform

def get_platform_name():
    system = platform.system()
    if system == "Linux":
        if platform.machine() == "x86_64":
            return "linux_amd64"
        elif platform.machine() == "aarch64":
            return "linux_arm64"
  

# 从环境变量中获取版本号
version_name = os.getenv('GITHUB_REF_NAME', 'v1.0.0.alpha')  # 如果环境变量中没有设置版本号，则使用默认值'1.0.0'


def replace(file, value, new_value):
    data = ""
    with open(file, "r", encoding='utf-8') as f:
        data = f.read()
    data = data.replace(value, new_value)
    with open(file, "w", encoding='utf-8') as f:
        f.write(data)

replace("ui/main.ui", "VCODE", version_name)


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[''],
    binaries=[],
    datas=[('./esptool/esptool_linux_amd64', 'esptool'),('./stm32tool/stm32flash_linux_amd64', 'stm32tool'),('./ui/about.ui', 'ui'), ('./ui/main.ui', 'ui'), ('./ui/taobao.ui', 'ui'), ('./ui/assert/fishros.jpg', 'ui/assert'),('./ui/assert/taobao.jpeg', 'ui/assert')],
    hiddenimports=['yaml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=f'fishbot_tool.{version_name}.{get_platform_name()}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/assert/fishros.jpg',
)


replace("ui/main.ui", version_name, "VCODE")


