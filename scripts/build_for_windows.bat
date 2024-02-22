if not exist "build" mkdir build
poetry run nuitka pulse/launch.py^
 --onefile^
 --disable-console^
 --assume-yes-for-downloads^
 --file-version=2.0^
 --company-name=MOPT^
 --product-name=OpenPulse^
 --output-filename=OpenPulse.exe^
 --enable-plugin=pyqt5^
 --windows-icon-from-ico=data/icons/pulse.ico^
 --include-data-dir=data/icons/=data/icons/^
 --include-data-dir=data/symbols/=data/symbols/^
 --include-data-dir=pulse/interface/ui_files/=pulse/interface/ui_files/^
 --include-data-dir=pulse/lib/=pulse/lib/^
 
@REM  --onefile-windows-splash-screen-image=data/icons/OpenPulse_logo_black.png
 