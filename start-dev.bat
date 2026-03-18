@echo off
setlocal

cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
  echo [ERROR] uv is not installed or not in PATH.
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo [ERROR] npm is not installed or not in PATH.
  exit /b 1
)

echo [1/4] Initializing backend dependencies...
cd /d "%~dp0backend"
call uv sync --dev
if errorlevel 1 (
  echo [ERROR] Backend initialization failed.
  exit /b 1
)

echo [2/4] Initializing frontend dependencies...
cd /d "%~dp0frontend"
call npm install
if errorlevel 1 (
  echo [ERROR] Frontend initialization failed.
  exit /b 1
)

echo [3/4] Starting backend server in a new window...
start "hit-monittor-backend" cmd /k "cd /d %~dp0backend && uv run uvicorn app.main:app --reload"

echo [4/4] Starting frontend dev server in a new window...
start "hit-monittor-frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Backend and frontend startup commands were launched.
echo Backend:  http://127.0.0.1:8000
echo Frontend: check the Vite window for the local URL

endlocal
