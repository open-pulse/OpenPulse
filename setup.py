from cx_Freeze import setup, Executable


build_options = dict(
    packages = ['vtkmodules', 'scipy'],
    excludes = ['envpulse/', '.config'],
    include_files = [
        'data',
        'libs'
    ]
)

executable = [
    Executable(
        script = 'pulse.py',
        base = None,
        target_name = 'OpenPulse',
        icon = 'data/icons/pulse.png'
    )
]

setup(
    name = 'OpenPulse',
    version = '0.1.0',
    description = 'descrição do programa',
    options = dict(build_exe = build_options),
    executables = executable
)