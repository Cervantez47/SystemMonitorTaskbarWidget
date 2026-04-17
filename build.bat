@echo off
echo Building SystemMonitorTaskbarWidget.exe ...
pyinstaller --onefile ^
            --windowed ^
            --name SystemMonitorTaskbarWidget ^
            --icon NONE ^
            main.py
echo.
echo Done. Output: dist\SystemMonitorTaskbarWidget.exe
pause
