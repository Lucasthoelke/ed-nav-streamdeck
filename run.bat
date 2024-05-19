@echo off

SET PYTHON_COMMAND=C:\Users\lucas\AppData\Local\Programs\Python\Python39\python.exe
SET PYTHON_OK_VERSION=Python 3
SET PYTHON_MINIMUM_VERSION=3.8

SET BASE_PATH=%~dp0
SET PLUGIN_DIR_PATH=%BASE_PATH:~0,-1%
for %%I in ("%PLUGIN_DIR_PATH%") do set PLUGIN_NAME=%%~nxI
SET PLUGIN_LOGS_DIR_PATH=%PLUGIN_DIR_PATH%\logs
SET PYTHON_INIT_PATH=%PLUGIN_DIR_PATH%\init.py

SET PLUGIN_CODE_DIR_PATH=%PLUGIN_DIR_PATH%
SET PLUGIN_CODE_REQUIREMENTS_PATH=%PLUGIN_CODE_DIR_PATH%\requirements.txt
SET PLUGIN_CODE_PATH=%PLUGIN_CODE_DIR_PATH%\main.py

SET PLUGIN_CODE_VENV_DIR_PATH=%PLUGIN_CODE_DIR_PATH%\venv
SET PLUGIN_CODE_VENV_ACTIVATE=%PLUGIN_CODE_VENV_DIR_PATH%\Scripts\Activate
SET PLUGIN_CODE_VENV_PYTHON=%PLUGIN_CODE_VENV_DIR_PATH%\Scripts\python.exe

echo "Command: %PYTHON_COMMAND%"
echo "Ok version: %PYTHON_OK_VERSION%"
echo "Min version: %PYTHON_MINIMUM_VERSION%"

echo "Base: %BASE_PATH%"
echo "Dir: %PLUGIN_DIR_PATH%"
echo "Name: %PLUGIN_NAME%"
echo "Logs: %PLUGIN_LOGS_DIR_PATH%"
echo "Init: %PYTHON_INIT_PATH%"

echo "Code dir: %PLUGIN_CODE_DIR_PATH%"
echo "Req dir: %PLUGIN_CODE_REQUIREMENTS_PATH%"
echo "Code path: %PLUGIN_CODE_PATH%"

echo "Venv dir: %PLUGIN_CODE_VENV_DIR_PATH%"
echo "Venv activate: %PLUGIN_CODE_VENV_ACTIVATE%"
echo "Venv python: %PLUGIN_CODE_VENV_PYTHON%"

FOR /F "tokens=* USEBACKQ" %%F IN (`%PYTHON_COMMAND% -V`) DO SET PYTHON_VERSION=%%F

echo "version: %PYTHON_VERSION%"

IF "%PYTHON_VERSION%" == "" (
echo "bad python (no version)"
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('%PYTHON_OK_VERSION% not installed', 'StreamDeck \"%PLUGIN_NAME%\" plugin ERROR', 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);}"
exit
)

IF NOT "%PYTHON_VERSION:~0,8%" == "%PYTHON_OK_VERSION%" (
echo "bad python (wrong version)"
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('%PYTHON_OK_VERSION% not installed', 'StreamDeck \"%PLUGIN_NAME%\" plugin ERROR', 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);}"
exit
)

FOR /F "tokens=* USEBACKQ" %%F IN (`%PYTHON_COMMAND% "%PYTHON_INIT_PATH%"`) DO SET INIT_RESULT=%%F
echo "Init result: %INIT_RESULT%"

IF NOT "%INIT_RESULT%" == "True" (
echo "bad python (init fail)"
powershell -Command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('%INIT_RESULT%', 'StreamDeck \"%PLUGIN_NAME%\" plugin ERROR', 'OK', [System.Windows.Forms.MessageBoxIcon]::Information);}"
exit
)

SET PYTHONPATH="%PLUGIN_CODE_DIR_PATH%"
echo "%PYTHONPATH%"

"%PLUGIN_CODE_VENV_PYTHON%" "%PLUGIN_CODE_PATH%" %*
