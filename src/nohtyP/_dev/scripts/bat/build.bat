:: no output by default
@echo off
:: enable vars expandable after execution
setlocal enabledelayedexpansion
:: UTF-8 codepage
chcp 65001 >nul

:: Build stage decl
setlocal "NOHTYP_STAGE=beta"

call :start
:: Ignore errors, exit immediately after anyways. best-effort imitation of set -euo pipefail. relies on goto returns and || rem no to ignore fails extra hard
set "RC=%ERRORLEVEL%"
call :cleanup
exit /b %RC%

:start
set "STARTDIR=%cd%"
set "_YP_BUILD_SUCCESS=0"
call :relocate
:: thusly executing from src dir
echo Removing pycache...
cmd /S /C .\nohtyP\_dev\scripts\bat\clean_cache.bat 2>nul
call :copy_files
call :create_venv
call :get_date
call :build
call :inspect
call :test_installs
:: cleanup removes venv and such so this is fine
goto :eof

:relocate
cd /d "%~dp0..\..\..\.."
:: move four dirs up relative to this file (to src)
goto :eof

:copy_files
echo Copying in licenses...
mkdir LICENSES
copy /Y /L ..\LICENSES\* LICENSES\ 1>nul
call :check_copy
echo Emptying build directory...
call :clear_dist
goto :eof

:check_copy
if not exist LICENSES (
    echo LICENSES directory failed creation >&2
    exit /b 1
)
for /f %%i in ('dir /b LICENSES 2^>nul') do goto :found
echo Failed to copy licenses >&2
exit /b 1
:found
goto :eof

:clear_dist
rmdir /s /q dist 1>nul
goto :eof

:create_venv
echo Creating venv...
set "TEMP_VENV=%TEMP%\venv_%RANDOM%"
python -m venv "%TEMP_VENV%"
call "%TEMP_VENV%\Scripts\activate.bat"
goto :eof

:get_date
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format ddMMyyyy"') do set "_N_formatted_date=%%i"
goto :eof

:build
echo Installing build dependencies...
:: Update venv pip and build, then build
python -m pip install --upgrade pip
python -m pip install hatch hatchling
echo Verifying dependecies...
:: make it shut up
python -m pip install --upgrade hatch hatchling 1>nul
python -m pip check
echo Building...
:: include an envvar for build hook
call :set_sourcish
set "_YP_HATCH_BUILD_MODE=sdist"
hatch build --target sdist
call :set_normal
set "_YP_HATCH_BUILD_MODE=release"
hatch build --target wheel
call :set_dev
set "_YP_HATCH_BUILD_MODE=dev"
hatch build --target wheel
goto :eof

:set_sourcish
(
    echo # modified by build script
    echo.
    echo class BUILD_DATA:
    echo ^    _BUILD_DATE = "!_N_formatted_date!"
    echo ^    _BUILD_DEVMODE = False
    echo ^    _BUILD_STAGE = "!NOHTYP_STAGE!"
    echo.
) > .\nohtyP\_buildinfo.py
goto :eof

:set_normal
(
    echo class BUILD_DATA:
    echo ^    _BUILD_DATE = "!_N_formatted_date!"
    echo ^    _BUILD_DEVMODE = False
    echo ^    _BUILD_STAGE = "!NOHTYP_STAGE!"
) > .\nohtyP\_buildinfo.py
goto :eof

:set_dev
(
    echo class BUILD_DATA:
    echo ^    _BUILD_DATE = "!_N_formatted_date!"
    echo ^    _BUILD_DEVMODE = True
    echo ^    _BUILD_STAGE = "!NOHTYP_STAGE!"
) > .\nohtyP\_buildinfo.py
goto :eof

:inspect
call :find
if "!_YP_BUILD_SUCCESS!" == "0" (
    call :inspect_whl
    call :inspect_dev
    call :inspect_tar
    echo.
    goto :eof
)
echo Skipping inspection... >&2
goto :eof

:find
set "latest_whl="
set "latest_dev="
set "latest_tar="
for %%F in (dist\nohtyP*.whl) do (
    echo %%~nxF | findstr /i "dev" >nul
    if errorlevel 1 if not defined latest_whl set "latest_whl=%%F"
)
for %%F in (dist\nohtyP*dev*.whl) do if not defined latest_dev set "latest_dev=%%F"
for %%F in (dist\nohtyP*.tar.gz) do if not defined latest_tar set "latest_tar=%%F"
if not defined latest_whl (
    echo Build failed: Release wheel not found >&2
    set "_YP_BUILD_SUCCESS=1"
)
if not defined latest_dev (
    echo Build failed: Dev wheel not found >&2
    set "_YP_BUILD_SUCCESS=1"
)
if not defined latest_tar (
    echo Build failed: Tarball not found >&2
    set "_YP_BUILD_SUCCESS=1"
)
goto :eof

:inspect_whl
echo.
echo === Inspecting production wheel^! ===
tar.exe -tf "!latest_whl!"
goto :eof

:inspect_dev
echo.
echo ====== Inspecting dev wheel^! ======
tar.exe -tf "!latest_dev!"
goto :eof

:inspect_tar
echo.
echo ======== Inspecting sdist^! ========
tar.exe -tf "!latest_tar!"
goto :eof

:test_installs
if "!_YP_BUILD_SUCCESS!" == "0" (
    :: get out of src
    cd ..
    :: necessary to make python use site-packages' nohtyP install
    call :test_install_normal
    call :test_install_dev
    goto :eof
)
echo Skipping installation... >&2
goto :eof

:test_install_normal
python -m pip install --no-cache-dir "src\!latest_whl!"
python -m nohtyP
echo Pip show status:
python -m pip show nohtyP
echo.
goto :eof

:test_install_dev
python -m pip uninstall -y nohtyP
python -m pip install --no-cache-dir "src\!latest_dev!"
python -m nohtyP
echo Pip show status:
python -m pip show nohtyP
echo.
goto :eof

:cleanup
:: move to src again
cd .\src || cd /d "%~dp0..\..\..\.."
echo Cleaning remains...
:: rm pycache
cmd /S /C .\nohtyP\_dev\scripts\bat\clean_cache.bat 2>nul
:: reset buildinfo file
call :reset_bi
:: remove the temp licenses
rmdir /s /q LICENSES
:: delete the venv
call :rm_venv
:: return
cd "!STARTDIR!"
goto :eof

:reset_bi
(
    echo #! modified by build script
    echo.
    echo class BUILD_DATA:
    echo ^    _BUILD_DATE = ""
    echo ^    _BUILD_DEVMODE = False
    echo ^    _BUILD_STAGE = "!NOHTYP_STAGE!"
    echo.
) > ./nohtyP/_buildinfo.py
goto :eof

:rm_venv
:: deactivate venv
if defined VIRTUAL_ENV call deactivate
:: delete venv folder
rmdir /s /q "!TEMP_VENV!"
goto :eof
