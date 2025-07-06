from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Always ensure the table exists ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            task TEXT,
            due DATE
        )
    ''')
    conn.commit()
    conn.close()

# --- Home Page ---
@app.route('/')
def index():
    init_db()  # ensure table exists
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM homework ORDER BY due ASC")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# --- Add Task ---
@app.route('/add', methods=['POST'])
def add():
    subject = request.form['subject']
    task = request.form['task']
    due = request.form['due']

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO homework (subject, task, due) VALUES (?, ?, ?)",
              (subject, task, due))
    conn.commit()
    conn.close()
    return redirect('/')

# --- Delete Task ---
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM homework WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# --- Run the Site ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

