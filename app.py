from flask import Flask, redirect, request
import string
import random
import os
import psycopg2

# Conexión a la base de datos desde variable de entorno
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# Crear tabla si no existe
cur.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id SERIAL PRIMARY KEY,
        short VARCHAR(6) UNIQUE NOT NULL,
        original TEXT NOT NULL
    );
''')
conn.commit()

app = Flask(__name__)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()

        # Guardar en PostgreSQL
        cur.execute("INSERT INTO urls (short, original) VALUES (%s, %s)", (short_url, original_url))
        conn.commit()
        return f'Short URL: <a href="/{short_url}">/{short_url}</a>'

    return '''
        <form method="post">
            URL to shorten: <input type="text" name="url">
            <input type="submit" value="Shorten">
        </form>
    '''

@app.route('/<short_url>')
def redirect_to_url(short_url):
    cur.execute("SELECT original FROM urls WHERE short = %s", (short_url,))
    result = cur.fetchone()
    if result:
        return redirect(result[0])
    return 'URL not found', 404

from waitress import serve

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

