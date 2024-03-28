# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pulse/launch.py'],
    pathex=[],
    binaries=[],
    # I have no idea why, but we need 
    # to add data in pairs
    datas=[
        ('data/', 'data/'),
        ('pulse/interface/data/', 'pulse/interface/data/'),
        ('pulse/interface/ui_files/', 'pulse/interface/ui_files/'),
        ('pulse/interface/icons/', 'pulse/interface/icons/'),
        ('pulse/libraries/', 'pulse/libraries/'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
splash = Splash(
    'pulse/interface/data/icons/logos/OpenPulse_logo_black.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    splash,
    splash.binaries,
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
