@echo off
cd /d "%~dp0"
python src/builder.py %*
