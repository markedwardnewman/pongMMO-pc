# chat_history.py
import json
import os

CHAT_HISTORY_FILE = 'chat_history.json'

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, 'w') as file:
        json.dump(history, file)

def add_to_chat_history(message):
    history = load_chat_history()
    history.append(message)
    save_chat_history(history)
