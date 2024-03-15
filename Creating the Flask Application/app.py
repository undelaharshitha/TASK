# app.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            dob DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        dob = request.form['dob']

        try:
            age = int(age)
        except ValueError:
            return "Age must be a number."

        conn = sqlite3.connect('userdata.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, age, dob) VALUES (?, ?, ?, ?)', (name, email, age, dob))
        conn.commit()
        conn.close()
        
        return redirect(url_for('get_users'))

@app.route('/users')
def get_users():
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
