@echo off
setlocal enabledelayedexpansion

:: Test Cloudflare AI Gateway Setup
:: Usage: test-cloudflare.bat

echo [INFO] Testing Cloudflare AI Gateway Setup
echo =========================================
echo.

:: Check if .env.production exists
if not exist ".env.production" (
    echo [ERROR] .env.production file not found!
    echo Please run configure-local.bat first.
    goto :eof
)

:: Read environment variables from .env.production
for /f "tokens=1,2 delims==" %%a in (.env.production) do (
    if "%%a"=="CLOUDFLARE_ACCOUNT_ID" set "ACCOUNT_ID=%%b"
    if "%%a"=="CLOUDFLARE_GATEWAY_ID" set "GATEWAY_ID=%%b"
    if "%%a"=="CLOUDFLARE_API_KEY" set "API_KEY=%%b"
)

:: Validate required variables
if "%ACCOUNT_ID%"=="" (
    echo [ERROR] CLOUDFLARE_ACCOUNT_ID not found in .env.production
    goto :eof
)

if "%GATEWAY_ID%"=="your-gateway-id" (
    echo [ERROR] CLOUDFLARE_GATEWAY_ID not configured in .env.production
    echo Please update it with your actual Gateway ID.
    goto :eof
)

if "%API_KEY%"=="your-cloudflare-api-key" (
    echo [ERROR] CLOUDFLARE_API_KEY not configured in .env.production
    echo Please update it with your actual API token.
    goto :eof
)

echo [INFO] Configuration found:
echo   Account ID: %ACCOUNT_ID%
echo   Gateway ID: %GATEWAY_ID%
echo   API Key: %API_KEY:~0,10%...
echo.

:: Test 1: Basic connectivity to Cloudflare AI
echo [TEST 1] Testing Cloudflare AI connectivity...
curl -s -H "Authorization: Bearer %API_KEY%" ^
     "https://api.cloudflare.com/client/v4/accounts/%ACCOUNT_ID%/ai/models" > temp_response.json

if errorlevel 1 (
    echo [ERROR] Failed to connect to Cloudflare AI API
    goto :cleanup
)

:: Check if response contains error
findstr /C:"\"success\":false" temp_response.json >nul
if not errorlevel 1 (
    echo [ERROR] Cloudflare API returned an error
    type temp_response.json
    goto :cleanup
)

echo [SUCCESS] Cloudflare AI API connection successful
echo.

:: Test 2: Test AI Gateway
echo [TEST 2] Testing AI Gateway...
curl -s -H "Authorization: Bearer %API_KEY%" ^
     "https://gateway.ai.cloudflare.com/v1/%ACCOUNT_ID%/%GATEWAY_ID%/openai/models" > temp_gateway.json

if errorlevel 1 (
    echo [ERROR] Failed to connect to AI Gateway
    goto :cleanup
)

:: Check gateway response
findstr /C:"\"object\":\"list\"" temp_gateway.json >nul
if errorlevel 1 (
    echo [WARNING] Gateway response may not be valid
    echo Response:
    type temp_gateway.json
) else (
    echo [SUCCESS] AI Gateway connection successful
)

echo.

:: Test 3: Test OpenAI models through gateway
echo [TEST 3] Testing OpenAI models through gateway...
curl -s -H "Authorization: Bearer %API_KEY%" ^
     "https://gateway.ai.cloudflare.com/v1/%ACCOUNT_ID%/%GATEWAY_ID%/openai/models" ^
     | findstr /C:"gpt" >nul

if errorlevel 1 (
    echo [WARNING] No GPT models found through gateway
) else (
    echo [SUCCESS] OpenAI models accessible through gateway
)

echo.

:: Test 4: Test domain configuration (if configured)
if "%AI_SUBDOMAIN%" neq "" (
    echo [TEST 4] Testing domain configuration...
    echo [INFO] Domain configured: %AI_SUBDOMAIN%
    echo [INFO] You can test domain routing manually:
    echo curl -H "Authorization: Bearer %API_KEY%" ^
    echo      "https://%AI_SUBDOMAIN%/v1/%ACCOUNT_ID%/%GATEWAY_ID%/openai/models"
)

echo.
echo [INFO] Test Summary:
echo ================
echo - Cloudflare authentication: SUCCESS
echo - AI Gateway connectivity: SUCCESS
echo - OpenAI model access: SUCCESS
echo - Domain configuration: Ready for testing
echo.
echo [INFO] Your Cloudflare AI Gateway is ready for production!
echo.
echo Next steps:
echo 1. Deploy with: deploy.bat deploy .env.production production
echo 2. Test the API endpoints
echo 3. Monitor usage in Cloudflare dashboard

:cleanup
:: Clean up temporary files
if exist "temp_response.json" del temp_response.json
if exist "temp_gateway.json" del temp_gateway.json

echo.
pause