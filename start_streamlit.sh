#!/bin/bash
VENV_PYTHON="/var/www/chatbot/venv/bin/python3"
# Pythonスクリプトを実行
$VENV_PYTHON -m streamlit run /var/www/chat-agent/chat_agent.py --server.port 8501 --server.enableCORS false




