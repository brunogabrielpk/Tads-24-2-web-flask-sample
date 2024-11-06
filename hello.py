from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print('Database initialized')

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, age, email) VALUES (?, ?, ?)', (name, age, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_user.html')

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def update_user(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        cursor.execute('UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?', (name, age, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

