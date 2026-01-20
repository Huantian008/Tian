@echo off
echo 开始清理 Java 项目...

REM 删除所有 out 目录
for /d /r %%d in (out) do @if exist "%%d" rd /s /q "%%d"
echo 已删除所有 out 目录

REM 删除所有 .class 文件
del /s /q *.class 2>nul
echo 已删除所有 .class 文件

REM 删除所有 bin 目录
for /d /r %%d in (bin) do @if exist "%%d" rd /s /q "%%d"
echo 已删除所有 bin 目录

echo 清理完成！
pause
