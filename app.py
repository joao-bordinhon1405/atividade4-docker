import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quem-somos')
def quem_somos():
    return render_template('quemsomos.html')

@app.route('/contatos', methods=['GET', 'POST'])
def contatos():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO contatos (nome, email, mensagem) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nome, email, mensagem))
            conn.commit()
        finally:
            conn.close()

        return redirect(url_for('listar'))
    return render_template('contato.html')

@app.route('/listar')
def listar():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM contatos")
            registros = cursor.fetchall()
    finally:
        conn.close()

    return render_template('listar.html', registros=registros)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
