# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pulse/run.py'],
    pathex=[],
    binaries=[],
    datas=[
        # I have no idea why, but the paths need to be repeated
        ("data/", "data/"),
        ("pulse/interface/ui_files/", "pulse/interface/ui_files"),
        ("pulse/lib/", "pulse/lib/"),
    ],
    hiddenimports=[],
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
    icon="data/icons/pulse.ico",
)
