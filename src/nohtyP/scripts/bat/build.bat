@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 

goto :start

:clean
del /r /f LICENSES\
rmdir LICENSES
goto :eof

:copy_files
copy ...
exit /b

:start
set STARTDIR="%cd%"
(

)
call :clean
