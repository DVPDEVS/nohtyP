:: no output by default
@echo off
:: enable vars expandable after execution
setlocal enabledelayedexpansion
:: UTF-8 codepage
chcp 65001 >nul

call :start
:: Ignore errors, exit immediately after anyways
set "RC=%ERRORLEVEL%"
call :cleanup
exit /b %RC%

:start
set "STARTDIR=%cd%"
(
    call :relocate
    call :copy_files
    call :create_venv
    call :build
    call :inspect
    call :test_installs
    :: cleanup removes venv and such so this is fine
) || rem no
goto :eof

:relocate
(
    cd /d "%~dp0..\..\.."
    :: move three dirs up relative to this file (to src)
)
goto :eof

:copy_files
(
    mkdir LICENSES
    copy /Y /L ..\LICENSES\* LICENSES\
    call :check_copy
    call :clear_dist
)
goto :eof

:check_copy
(
    if not exist LICENSES (
        echo LICENSES directory failed creation >&2
        exit /b 1
    )
    :: set "_DIRL=0"
    :: for /f "delims=" %%i in ('dir /B LICENSES') do set /a _DIRL+=1
    :: if /i !_DIRL! LEQ 1 (
    ::     echo Failed to copy licenses! >&2
    ::     exit /b 1
    :: )
    for /f %%i in ('dir /b LICENSES 2^>nul') do goto :found
    echo Failed to copy licenses >&2
    exit /b 1
    :found
)
goto :eof

:clear_dist
(
    rmdir /s /q dist
)
goto :eof

:create_venv
(

)
goto :eof

:build
(
    python -m pip install build
    python -m build
)
goto :eof

:inspect
(
    call :find
    :: powershell unzip files
)
goto :eof

:find
:: 
goto :eof

:test_installs
(
    call :test_install_normal
    call :test_install_dev
)
goto :eof

:test_install_normal
(

)
goto :eof

:test_install_dev
(

)
goto :eof

:cleanup
(
    rmdir /s /q LICENSES
    call :rm_venv
    cd "!STARTDIR!"
) || rem no
goto :eof

:rm_venv
(

)
goto :eof
