@echo off
setlocal enabledelayedexpansion

for /d /r %%D in (__pycache__) do (
    if /i "%%~nxD"=="__pycache__" rd /s /q "%%D"
)
:: pycache is gitignored, but to clean it locally this can be nice.
