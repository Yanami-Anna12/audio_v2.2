@echo off
chcp 65001 >nul
echo 正在准备打包音频卡顿分析工具...
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python。请先安装Python。
    pause
    exit /b 1
)

echo 检测到Python，正在安装依赖...
echo.

REM 安装依赖
pip install -r requirements.txt

if errorlevel 1 (
    echo 依赖安装失败，请检查网络连接或手动安装依赖
    pause
    exit /b 1
)

echo 依赖安装完成，开始打包项目...
echo.

REM 清理之前的构建文件
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM 使用PyInstaller打包
pyinstaller -D frame_to_wav_run.spec

if errorlevel 1 (
    echo 打包失败，尝试使用命令行方式...
    pyinstaller -D -w -i wav.ico --add-data "get_data;get_data" --add-data "gui;gui" --add-data "services;services" --add-data "utils;utils" --add-data "analysis;analysis" --add-data "business;business" --add-data "pakcet;pakcet" frame_to_wav_run.py
)

echo.
echo 打包完成！
echo 可执行文件位于 dist\frame_to_wav_run\ 目录下
echo.
pause