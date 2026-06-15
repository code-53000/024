@echo off
chcp 65001 >nul
echo ========================================
echo   矿物晶体收藏管理系统 - 停止脚本
echo ========================================
echo.

echo 正在停止所有服务...
docker-compose down

echo.
echo [完成] 所有服务已停止
echo.
pause
