@echo off
(if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )

pip install -r requirements.txt
if %ERRORLEVEL% neq 0 goto error

echo SUCCESS
echo Module installation successful
Pause
goto exit

:error
echo ERROR
echo Module installation unsuccessful
Pause
goto exit

:exit
exit