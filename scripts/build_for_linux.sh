mkdir -p build
poetry run nuitka3 pulse/launch.py\
    --company-name=MOPT\
    --product-name=OpenPulse\
    --output-filename=build/OpenPulse.bin\
    --linux-icon=data/icons/pulse.ico