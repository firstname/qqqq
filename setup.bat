@echo off

rem 阅读安装须知  
type readme.txt
echo 如果你已经明白了安装要求
pause
echo .

rem 安装python 
start  %cd%\setup\python.msi
echo 安装完成python
pause
echo .

rem 使用国内pip源 
start  %cd%\setup\python建立pip.ini
echo 设置pip完成
pause
echo .

rem 安装django 
echo .
start cmd /c "pip install django==1.8"


rem 安装pandas 
echo .
start cmd /c "pip install pandas==0.18.1"

rem 安装xlrd 
echo .
start cmd /c "pip install xlrd==1.0.0"

rem 安装xlwt 
echo .
start cmd /c "pip install xlwt==1.1.2"


rem 创建程序快捷方式 
mshta VBScript:Execute("Set a=CreateObject(""WScript.Shell""):Set b=a.CreateShortcut(a.SpecialFolders(""Desktop"") & ""\mindbook.lnk""):b.TargetPath=""%cd%\setup\start.bat"":b.WorkingDirectory=""%cd%\setup\"":b.IconLocation=""%cd%\setup\01.ico"":b.Save:close")
echo .
echo 安装过程中如果弹出窗口中出现红色字体提示安装失败,请重新安装
echo .
echo 安装完成
echo 点击桌面快捷方式即可使用(如果没有快捷方式,请关掉360等再试)
pause