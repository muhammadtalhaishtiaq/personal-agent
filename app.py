from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import requests
import sqlite3
import uuid
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "2938dhjdbskjfksjdhfsjdf"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# API Configuration
API_KEY = "sk-1045e376ac5a444ab0cb458f2e7d1d1f"
QWEN_API_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# Database Configuration
DATABASE = 'chatbot.db'
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            tokens INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_chat_history(user_id, chat_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, content, tokens 
        FROM chats 
        WHERE user_id=? AND chat_id=?
        ORDER BY timestamp
    ''', (user_id, chat_id))
    history = [{"role": row[0], "content": row[1], "tokens": row[2]} for row in cursor.fetchall()]
    conn.close()
    return history

def save_to_chat_history(user_id, chat_id, role, content, tokens):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chats (user_id, chat_id, role, content, tokens)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, chat_id, role, content, tokens))
    conn.commit()
    conn.close()

@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_id = session['user_id']
    user_input = request.json.get('message')
    chat_id = request.json.get('chat_id') or str(uuid.uuid4())

    # Save user message with token count
    user_tokens = len(user_input.split())  # Approximate token count
    save_to_chat_history(user_id, chat_id, "user", user_input, user_tokens)

    # Call Qwen API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-plus",
        "input": {
            "messages": get_chat_history(user_id, chat_id)
        },
        "parameters": {
            "max_tokens": 500,
            "result_format": "message"
        }
    }

    response = requests.post(QWEN_API_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from Qwen"}), 500

    qwen_response = response.json()
    assistant_message = qwen_response['output']['choices'][0]['message']['content']
    assistant_tokens = qwen_response['usage']['output_tokens']

    # Save bot response with token count
    save_to_chat_history(user_id, chat_id, "assistant", assistant_message, assistant_tokens)

    return jsonify({
        "response": assistant_message,
        "chat_id": chat_id,
        "usage": qwen_response.get('usage', {}),
        "history": get_chat_history(user_id, chat_id)
    })

@app.route('/load_chats', methods=['GET'])
def load_chats():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get unique chat IDs
    cursor.execute('''
        SELECT DISTINCT chat_id 
        FROM chats 
        WHERE user_id=?
        ORDER BY timestamp DESC
    ''', (session['user_id'],))
    
    chat_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    return jsonify({"chat_ids": chat_ids})

@app.route('/load_chat/<chat_id>', methods=['GET'])
def load_chat(chat_id):
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    history = get_chat_history(session['user_id'], chat_id)
    return jsonify({
        "chat_id": chat_id,
        "history": history
    })

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session.permanent = True
            session['username'] = username
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error="Username already exists. Please choose another.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)