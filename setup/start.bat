@echo off

start cmd /k  "%~d0 &&cd %cd% &&type tips.txt &&cd .. &&python manage.py runserver 127.0.0.1:8008"

ping 127.0.0.1 -n 5

start /max %cd%\Application\115chrome.exe "http://127.0.0.1:8008"

popd  




