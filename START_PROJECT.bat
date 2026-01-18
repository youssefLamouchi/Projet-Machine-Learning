@echo off
echo ========================================
echo   Steel Industry Energy Prediction
echo ========================================
echo.

echo [1/2] Demarrage du Backend Python...
start cmd /k "cd backend && py -m pip install -q -r requirements.txt && echo Backend pret ! && py app.py"

timeout /t 3 /nobreak >nul

echo [2/2] Demarrage du Frontend Angular...
start cmd /k "cd frontend && npm install && npm start"

echo.
echo ========================================
echo   Projet demarre !
echo ========================================
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:4200
echo ========================================
