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
        "vtkmodules.util.execution_model",
        "vtkmodules.util.data_model",
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
    [],
    exclude_binaries=True,
    name='OpenPulse.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['pulse.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OpenPulse',
)
