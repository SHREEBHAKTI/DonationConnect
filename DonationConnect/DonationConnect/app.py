from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    address TEXT,
                    item TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS recipients (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    organization TEXT,
                    need TEXT,
                    contact TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        item = request.form['item']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO donors (name, email, address, item) VALUES (?, ?, ?, ?)",
                  (name, email, address, item))
        conn.commit()
        conn.close()
        flash('Donor information submitted successfully!')
        return redirect(url_for('index'))
    return render_template('donor.html')

@app.route('/recipient', methods=['GET', 'POST'])
def recipient():
    if request.method == 'POST':
        name = request.form['name']
        organization = request.form['organization']
        need = request.form['need']
        contact = request.form['contact']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO recipients (name, organization, need, contact) VALUES (?, ?, ?, ?)",
                  (name, organization, need, contact))
        conn.commit()
        conn.close()
        flash('Recipient information submitted successfully!')
        return redirect(url_for('index'))
    return render_template('recipient.html')

@app.route('/match')
def match():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    donors = c.fetchall()
    c.execute("SELECT * FROM recipients")
    recipients = c.fetchall()
    conn.close()
    return render_template('match.html', donors=donors, recipients=recipients)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
