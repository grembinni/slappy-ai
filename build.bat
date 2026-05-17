@echo off
echo Building GoblinVsSuperman...
pyinstaller slappy.spec --noconfirm
if %ERRORLEVEL% neq 0 (
    echo Build FAILED.
    exit /b 1
)
echo.
echo Build complete.
echo Executable: dist\GoblinVsSuperman\GoblinVsSuperman.exe
