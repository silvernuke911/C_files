# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\verci\\Documents\\code\\c_files\\Python\\pygame_particle\\partikol2.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\verci\\Documents\\code\\c_files\\Python\\pygame_particle\\partikol 2.0 icon.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='partikol2',
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
    icon=['C:\\Users\\verci\\Documents\\code\\c_files\\Python\\pygame_particle\\partikol2.0.ico'],
)
