from flask import Flask, render_template, request, redirect, url_for, send_file
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('postgresql://shopfi_db_user:KkEiHyzjqO9Pz5H83nNwj0fQhjdMZzbm@dpg-d1vmar2dbo4c73flg0k0-a.oregon-postgres.render.com/shopfi_db')


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


@app.before_first_request
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name) VALUES (%s);', (name,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('display', name=name))
    return render_template('form.html')


@app.route('/display/<name>')
def display(name):
    return render_template('display.html', name=name)


@app.route('/download')
def download():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM users;')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    with open('names.txt', 'w') as f:
        for row in rows:
            f.write(f"{row[0]}\n")

    return send_file('names.txt', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
