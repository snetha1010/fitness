from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = '123',  # <-- Comma added here to fix syntax error

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('database.db')

@app.route('/chat')
def chat():
    return render_template('chat.html')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/frondend_coding')
def frondend_coding():
    return render_template('frondend_coding.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        with connect_db() as conn:
            cursor = conn.cursor()

            # Retrieve user from the database
            cursor.execute("SELECT * FROM users1 WHERE username=?", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['logged_in'] = True
                return redirect('/')
            else:
                return 'Incorrect username or password'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS users1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );""")

            # Check if the username already exists
            cursor.execute("SELECT * FROM users1 WHERE username=?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return 'Username already exists!'
            else:
                # Insert new user into the database
                cursor.execute("INSERT INTO users1 (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
                conn.commit()
                return redirect(url_for('login'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
