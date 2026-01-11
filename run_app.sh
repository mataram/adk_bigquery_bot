#!/bin/bash
source ~/.bashrc
conda activate bot_bq
export PYTHONPATH=$(pwd)
echo "Starting ADK API Server on http://localhost:8000 ..."
python -m google.adk.cli web agents --port 8000
