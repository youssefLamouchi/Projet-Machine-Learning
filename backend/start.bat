@echo off
echo Installation des dependances Python...
py -m pip install -r requirements.txt

echo.
echo Demarrage du serveur Flask...
py app.py
