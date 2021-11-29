import os, sys
from pulse import __version__
from cx_Freeze import setup, Executable


shortcut_table = [
    (
        "DesktopShortcut",        # Shortcut
        "DesktopFolder",          # Directory_
        "Open Pulse",             # Name
        "TARGETDIR",              # Component_
        "[TARGETDIR]OpenPulse.exe",# Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
     )
]

build_exe_options = dict(
    packages = ['vtkmodules', 'scipy'],

    excludes = [
        'envpulse/', 
        '.config'
    ],

    include_files = [
        'data',
        'libs'
    ]
)

build_msi_options = dict(
    data = {'Shortcut':shortcut_table}
)

executable = [
    Executable(
        script = 'pulse.py',
        target_name = 'OpenPulse',
        icon = 'data/icons/pulse.ico'
    )
]

setup(
    name = 'OpenPulse',
    author = 'MOPT',
    version = __version__,
    description = 'A software written in Python for numerical modelling of low-frequency \
                   acoustically induced vibration in gas pipeline systems',
    options = dict(build_exe = build_exe_options,
                   bdist_msi = build_msi_options),
    executables = executable
)