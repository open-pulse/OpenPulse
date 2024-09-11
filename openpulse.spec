# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files


datas = [
    # we need to add the paths in pairs
    ('pulse/interface/data/', 'pulse/interface/data/'),
    ('pulse/libraries/', 'pulse/libraries/'),
]
datas += collect_data_files('molde')
datas += collect_data_files('opps')

a = Analysis(
    ['pulse/launch.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "vtk",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OpenPulse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)