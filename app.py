from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import dill
import os

app = Flask(__name__)
app.secret_key = '9f1b8e34e25f90b6a37f16d0e0dd9e83a467c5ab00918a3e'

# Load the model
with open('insulin_model.pkl', 'rb') as f:
    model = dill.load(f)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                age INTEGER,
                height REAL,
                weight REAL,
                gender TEXT,
                hb1ac REAL,
                sugar_level REAL,
                prescribed_dose REAL,
                calories REAL,
                predicted_dose REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                flash("Account created successfully! Please log in.", "success")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Username already exists!", "danger")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    prediction = None
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            gender = request.form['gender']
            hb1ac = float(request.form['hb1ac'])
            sugar_level = float(request.form['sugar_level'])
            prescribed_dose = float(request.form['prescribed_dose'])
            calories = float(request.form['calories'])

            if sugar_level > 500 or prescribed_dose > 50 or calories > 1000:
                flash("One or more inputs exceeded the allowed limit.", "danger")
                return render_template('dashboard.html')
            
            
            prediction = model.predict(sugar_level, calories, prescribed_dose)


            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO records (
                        user_id, age, height, weight, gender, hb1ac,
                        sugar_level, prescribed_dose, calories, predicted_dose
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session['user_id'], age, height, weight, gender, hb1ac,
                    sugar_level, prescribed_dose, calories, prediction
                ))
                conn.commit()
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template('dashboard.html', prediction=prediction)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM records WHERE user_id = ?', (session['user_id'],))
        records = c.fetchall()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
