@echo off
REM Reset transfer rules file to clean template
REM Usage: reset_to_template.bat [template_name] [target_file]
REM Example: reset_to_template.bat minimal_template.t1x ..\..\transfer_rules.t1x

setlocal

REM Default template if not specified
set TEMPLATE=%1
if "%TEMPLATE%"=="" set TEMPLATE=minimal_template.t1x

REM Default target if not specified
set TARGET=%2
if "%TARGET%"=="" set TARGET=..\..\transfer_rules.t1x

REM Check if template exists
if not exist "%TEMPLATE%" (
    echo ERROR: Template file "%TEMPLATE%" not found!
    echo Available templates:
    dir /B *.t1x
    exit /b 1
)

REM Backup existing file if it exists
if exist "%TARGET%" (
    set BACKUP=%TARGET%.backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set BACKUP=%BACKUP: =0%
    echo Creating backup: %BACKUP%
    copy "%TARGET%" "%BACKUP%"
)

REM Copy template to target
echo Copying %TEMPLATE% to %TARGET%
copy /Y "%TEMPLATE%" "%TARGET%"

if %ERRORLEVEL% EQU 0 (
    echo Success! Transfer rules reset to %TEMPLATE%
    echo.
    echo Next steps:
    echo 1. Run "Set Up Transfer Rule Categories and Attributes" to populate from FLEx
    echo 2. Run "Rule Assistant" to create your rules
) else (
    echo ERROR: Failed to copy template
    exit /b 1
)

endlocal
