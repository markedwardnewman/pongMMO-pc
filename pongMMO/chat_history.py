#  chat_history.py
import json
import os

HISTORY_FILE = "conversation_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            conversation_history = json.load(f)
    else:
        conversation_history = []
    return conversation_history

def save_history(conversation_history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(conversation_history, f)

