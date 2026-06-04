:: no output by defult
@echo off
:: enable vars expandable after execution
setlocal enabledelayedexpansion
:: UTF-8 codepage
chcp 65001 >nul

call :start
set "RC=%ERRORLEVEL%"
call :clean
exit /b %RC%

:start
set "STARTDIR=%cd%"
(
    :: do stuff
) || rem no
goto :eof

:copy_files
(
    copy ...
)
goto :eof

:clean
(
    rmdir /s /q LICENSES
    cd !STARTDIR!
) || rem no
:: Ignore errors, exit immediately after anyways
goto :eof
