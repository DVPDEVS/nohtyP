:: no output by default
@echo off
:: enable vars expandable after execution
setlocal enabledelayedexpansion
:: UTF-8 codepage
chcp 65001 >nul

call :start
:: Ignore errors, exit immediately after anyways. best-effort imitation of set -euo pipefail. relies on goto returns and || rem no to ignore fails extra hard
set "RC=%ERRORLEVEL%"
call :cleanup
exit /b %RC%

:start
set "STARTDIR=%cd%"
set "_YP_BUILD_SUCCESS=0"
call :relocate
start clean_cache.bat
call :copy_files
call :create_venv
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
mkdir LICENSES
copy /Y /L ..\LICENSES\* LICENSES\
call :check_copy
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
rmdir /s /q dist
goto :eof

:create_venv
set "TEMP_VENV=%TEMP%\venv_%RANDOM%"
python -m venv "%TEMP_VENV%"
call "%TEMP_VENV%\Scripts\activate.bat"
goto :eof

:build
:: Update venv pip and build, then build
python -m pip install --upgrade pip
python -m pip install hatch hatchling
python -m pip install --upgrade hatch hatchling
:: include an envvar for build hook
set "_YP_HATCH_BUILD_MODE=release"
hatch build --target wheel
set "_YP_HATCH_BUILD_MODE=sdist"
hatch build --target sdist
set "_YP_HATCH_BUILD_MODE=dev"
hatch build --target wheel
goto :eof

:inspect
call :find
call :inspect_whl
call :inspect_tar
goto :eof

:inspect_whl
if not defined latest_whl (
    echo Wheel not found, stopping inspection. >&2
    goto :eof
)
echo === Inspecting production wheel^! ===
tar.exe -tf "!latest_whl!"
goto :eof

:inspect_tar
if not defined latest_tar (
    echo Tarball not found, stopping inspection. >&2
    goto :eof
)
echo ======== Inspecting sdist^! ========
tar.exe -tf "!latest_tar!"
goto :eof

:find
set "latest_whl="
set "latest_dev="
set "latest_tar="
for %%F in (dist\nohtyP*release*.whl) do if not defined latest_whl set "latest_whl=%%F"
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

:test_installs
if defined latest_whl (
    call :test_install_normal
    call :test_install_dev
    goto :eof
)
echo Cannot test installation^! >&2
goto :eof

:test_install_normal
python -m pip install --no-cache-dir "!latest_whl!"
python -c "import nohtyP"
goto :eof

:test_install_dev
@REM python -m pip uninstall -y nohtyP
@REM python -m pip install --no-cache-dir "!latest_whl![dev]"
@REM python -c "import nohtyP"
goto :eof

:cleanup
:: remove the temp licenses
rmdir /s /q LICENSES
call :rm_venv
cd "!STARTDIR!"
goto :eof

:rm_venv
:: deactivate venv
if defined VIRTUAL_ENV call deactivate
:: delete venv folder
rmdir /s /q "!TEMP_VENV!"
goto :eof
