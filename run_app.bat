@echo off
call conda activate bot_bq
set PYTHONPATH=%CD%
echo Starting ADK API Server on http://localhost:8000 ...
python -m google.adk.cli web agents --port 8000
pause
