@echo off
chcp 65001 >nul 2>&1
title Gestion Pro — Installation

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   GESTION PRO — HAFIANE MOUNIR       ║
echo  ║   Installation en cours...           ║
echo  ╚══════════════════════════════════════╝
echo.

:: Get current directory
set "INSTALL_DIR=%~dp0"
set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
set "HTML_FILE=%INSTALL_DIR%\index.html"

:: Check if index.html exists
if not exist "%HTML_FILE%" (
    echo [ERREUR] index.html introuvable dans ce dossier!
    echo Assurez-vous que tous les fichiers sont dans le meme dossier.
    pause
    exit /b 1
)

echo [1/3] Fichiers verifies...

:: Create desktop shortcut using VBScript
set "SHORTCUT=%USERPROFILE%\Desktop\Gestion Pro.lnk"
set "VBS=%TEMP%\create_shortcut.vbs"

:: Find Edge or Chrome
set "BROWSER="
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)
if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    set "BROWSER=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    if "%BROWSER%"=="" set "BROWSER=C:\Program Files\Google\Chrome\Application\chrome.exe"
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    if "%BROWSER%"=="" set "BROWSER=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

if "%BROWSER%"=="" (
    echo [AVERT] Edge et Chrome non trouves. Utilisation du navigateur par defaut.
    :: Create shortcut opening HTML directly
    echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS%"
    echo sLinkFile = "%SHORTCUT%" >> "%VBS%"
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS%"
    echo oLink.TargetPath = "%HTML_FILE%" >> "%VBS%"
    echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%VBS%"
    echo oLink.Description = "Gestion Pro - Hafiane Mounir" >> "%VBS%"
    echo oLink.Save >> "%VBS%"
) else (
    :: Create shortcut with browser app mode
    echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS%"
    echo sLinkFile = "%SHORTCUT%" >> "%VBS%"
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS%"
    echo oLink.TargetPath = "%BROWSER%" >> "%VBS%"
    echo oLink.Arguments = "--app=file:///%HTML_FILE:\=/%  --start-maximized" >> "%VBS%"
    echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%VBS%"
    echo oLink.Description = "Gestion Pro - Hafiane Mounir" >> "%VBS%"
    echo oLink.WindowStyle = 3 >> "%VBS%"
    echo oLink.Save >> "%VBS%"
)

cscript //nologo "%VBS%"
del "%VBS%" 2>nul

echo [2/3] Raccourci bureau cree...

:: Create start.bat for easy launch
echo @echo off > "%INSTALL_DIR%\start.bat"
echo chcp 65001 ^>nul 2^>^&1 >> "%INSTALL_DIR%\start.bat"
if not "%BROWSER%"=="" (
    echo start "" "%BROWSER%" --app="file:///%HTML_FILE:\=/%" --start-maximized >> "%INSTALL_DIR%\start.bat"
) else (
    echo start "" "%HTML_FILE%" >> "%INSTALL_DIR%\start.bat"
)

:: Create uninstall
echo @echo off > "%INSTALL_DIR%\uninstall.bat"
echo del "%SHORTCUT%" 2^>nul >> "%INSTALL_DIR%\uninstall.bat"
echo echo Raccourci supprime. >> "%INSTALL_DIR%\uninstall.bat"
echo pause >> "%INSTALL_DIR%\uninstall.bat"

echo [3/3] Installation terminee!
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   ✅ INSTALLATION REUSSIE!                   ║
echo  ║                                              ║
echo  ║   📌 Raccourci cree sur le Bureau:           ║
echo  ║      "Gestion Pro"                           ║
echo  ║                                              ║
echo  ║   🚀 Double-cliquez pour lancer!             ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Ask to launch now
set /p LAUNCH=Lancer Gestion Pro maintenant? (O/N): 
if /i "%LAUNCH%"=="O" (
    if not "%BROWSER%"=="" (
        start "" "%BROWSER%" --app="file:///%HTML_FILE:\=/%" --start-maximized
    ) else (
        start "" "%HTML_FILE%"
    )
)
echo.
pause
