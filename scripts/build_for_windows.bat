mkdir build
poetry run nuitka3 pulse/launch.py\
    --company-name=MOPT\
    --product-name=OpenPulse\
    --output-filename=build/OpenPulse.bin\
    --windows-icon-from-ico=data/icons/pulse.ico\
    --onefile-windows-splash-screen-image=data/icons/OpenPulse_logo_black.png