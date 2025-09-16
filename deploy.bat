@echo off
setlocal enabledelayedexpansion

:: LightRAG Docker Deployment Script for Windows
:: Usage: deploy.bat [command] [env_file]

set "COMMAND=%1"
set "ENV_FILE=%2"

if "%COMMAND%"=="" (
    echo Usage: deploy.bat [command] [env_file]
    echo.
    echo Commands:
    echo   deploy [env_file]    Deploy LightRAG
    echo   logs [service]       Show logs
    echo   stop                 Stop all services
    echo   restart              Restart services
    echo   status               Show service status
    echo.
    echo Examples:
    echo   deploy.bat deploy .env.local
    echo   deploy.bat logs
    echo   deploy.bat stop
    goto :eof
)

if "%COMMAND%"=="deploy" (
    if "%ENV_FILE%"=="" set "ENV_FILE=.env.local"

    echo [INFO] Starting LightRAG deployment with %ENV_FILE%
    echo.

    :: Check if environment file exists
    if not exist "%ENV_FILE%" (
        echo [ERROR] Environment file %ENV_FILE% not found!
        echo Run configure-local.bat first to create it.
        goto :eof
    )

    :: Copy environment file
    echo [INFO] Copying environment configuration...
    copy "%ENV_FILE%" .env >nul

    :: Create necessary directories
    if not exist "data" mkdir data
    if not exist "data\rag_storage" mkdir data\rag_storage
    if not exist "data\inputs" mkdir data\inputs
    if not exist "logs" mkdir logs

    :: Build and start services
    echo [INFO] Building and starting Docker services...
    docker-compose up -d --build

    :: Wait a moment for services to start
    timeout /t 5 /nobreak >nul

    :: Check if services are running
    docker-compose ps | findstr "Up" >nul
    if errorlevel 1 (
        echo [ERROR] Services failed to start. Check logs with: deploy.bat logs
        goto :eof
    )

    echo.
    echo [SUCCESS] LightRAG deployment completed!
    echo.
    echo Access your application at:
    echo   Web UI: http://localhost:9621
    echo   API Docs: http://localhost:9621/docs
    echo   Health Check: http://localhost:9621/health
    echo.
    echo To view logs: deploy.bat logs
    echo To stop services: deploy.bat stop

    goto :eof
)

if "%COMMAND%"=="logs" (
    set "SERVICE=%2"
    if "%SERVICE%"=="" (
        echo [INFO] Showing all service logs...
        docker-compose logs -f
    ) else (
        echo [INFO] Showing logs for service: %SERVICE%
        docker-compose logs -f %SERVICE%
    )
    goto :eof
)

if "%COMMAND%"=="stop" (
    echo [INFO] Stopping all services...
    docker-compose down
    echo [SUCCESS] Services stopped.
    goto :eof
)

if "%COMMAND%"=="restart" (
    echo [INFO] Restarting services...
    docker-compose restart
    echo [SUCCESS] Services restarted.
    goto :eof
)

if "%COMMAND%"=="status" (
    echo [INFO] Service status:
    docker-compose ps
    goto :eof
)

echo [ERROR] Unknown command: %COMMAND%
echo Use 'deploy.bat' without arguments to see available commands.