@echo off

rem �Ķ���װ��֪  
type readme.txt
echo ������Ѿ������˰�װҪ��
pause
echo .

rem ��װpython 
start  %cd%\setup\python.msi
echo ��װ���python
pause
echo .

rem ʹ�ù���pipԴ 
start  %cd%\setup\python����pip.ini
echo ����pip���
pause
echo .

rem ��װdjango 
echo .
start cmd /c "pip install django==1.8"


rem ��װpandas 
echo .
start cmd /c "pip install pandas==0.18.1"

rem ��װxlrd 
echo .
start cmd /c "pip install xlrd==1.0.0"

rem ��װxlwt 
echo .
start cmd /c "pip install xlwt==1.1.2"


rem ���������ݷ�ʽ 
mshta VBScript:Execute("Set a=CreateObject(""WScript.Shell""):Set b=a.CreateShortcut(a.SpecialFolders(""Desktop"") & ""\mindbook.lnk""):b.TargetPath=""%cd%\setup\start.bat"":b.WorkingDirectory=""%cd%\setup\"":b.IconLocation=""%cd%\setup\01.ico"":b.Save:close")
echo .
echo ��װ������������������г��ֺ�ɫ������ʾ��װʧ��,�����°�װ
echo .
echo ��װ���
echo ��������ݷ�ʽ����ʹ��(���û�п�ݷ�ʽ,��ص�360������)
pause