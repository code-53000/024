@echo off
chcp 65001 >nul
echo ========================================
echo   矿物晶体收藏管理系统 - 启动脚本
echo ========================================
echo.

echo [1/4] 检查 Docker 状态...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Docker，请先安装并启动 Docker Desktop
    pause
    exit /b 1
)
echo [OK] Docker 已安装
echo.

echo [2/4] 停止并清理旧容器...
docker-compose down >nul 2>&1
echo [OK] 清理完成
echo.

echo [3/4] 构建并启动所有服务...
echo.
docker-compose up -d --build
echo.

echo [4/4] 等待服务启动完成...
echo.
echo 正在等待数据库就绪...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo   服务启动完成！
echo ========================================
echo.
echo 访问地址：
echo   前端: http://localhost
echo   后端 API: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo.
echo 演示账号：
echo   管理员: admin / admin123
echo   藏家1: collector1 / 123456
echo   藏家2: collector2 / 123456
echo   藏家3: collector3 / 123456
echo.
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
echo ========================================
echo.
pause
