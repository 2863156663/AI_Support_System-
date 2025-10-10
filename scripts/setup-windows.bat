@echo off
REM AI Support System Windows 环境设置脚本
REM 使用方法: setup-windows.bat

echo ========================================
echo AI Support System Windows 环境设置
echo ========================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo [信息] Python已安装

REM 检查Git是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Git未安装或未添加到PATH
    echo 请先安装Git
    pause
    exit /b 1
)

echo [信息] Git已安装

REM 创建虚拟环境
echo [信息] 创建Python虚拟环境...
cd /d "%~dp0..\app"
python -m venv venv
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)

echo [信息] 虚拟环境创建成功

REM 激活虚拟环境并安装依赖
echo [信息] 安装项目依赖...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [信息] 依赖安装成功

REM 创建启动脚本
echo [信息] 创建启动脚本...
echo @echo off > start-app.bat
echo cd /d "%%~dp0" >> start-app.bat
echo call venv\Scripts\activate.bat >> start-app.bat
echo python main.py >> start-app.bat
echo pause >> start-app.bat

echo [信息] 启动脚本创建成功

REM 创建测试脚本
echo [信息] 创建测试脚本...
echo @echo off > test-api.bat
echo cd /d "%%~dp0" >> test-api.bat
echo call venv\Scripts\activate.bat >> test-api.bat
echo python ..\fronted_api_test.py >> test-api.bat
echo pause >> test-api.bat

echo [信息] 测试脚本创建成功

echo ========================================
echo 环境设置完成！
echo ========================================
echo.
echo 使用方法:
echo 1. 启动应用: 双击 start-app.bat
echo 2. 测试API: 双击 test-api.bat
echo 3. 手动启动: 运行 python main.py
echo.
echo 注意事项:
echo - 确保端口5000未被占用
echo - 首次运行可能需要下载依赖包
echo - 如遇问题请检查Python和Git安装
echo.
pause
