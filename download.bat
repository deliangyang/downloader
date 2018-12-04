
@echo off
:begin
title 伴奏下载器
set input=
set /p input=请将Excel文件拖拽入框内（Enter）:

echo 当前目录为：%input%

run.exe %input%

echo 下载的数据放置在data目录下，data/export为导出的Excel
pause