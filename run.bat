@echo off
:start
ECHO.
ECHO 1. Run Server
ECHO 2. Run Client1
ECHO 3. Quit
set choice=
set /p choice=Type the number to run file: 
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='1' goto Server
if '%choice%'=='2' goto Client1
if '%choice%'=='3' goto Quit
ECHO "%choice%" is not valid, try again
ECHO.
goto start
:Server
cd %cd%\Server0
start python Main.py
cd ..
goto start
:Client1
cd %cd%\Client_1
start python Main.py
cd ..
goto start
:Quit