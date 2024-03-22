from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

# Conexão com o banco de dados

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

# Criação de tabelas se não existir

cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    disponivel TEXT DEFAULT 'sim'
    )
               ''')

# Lista de produtos a serem inseridos
produtos = [
    ("Camisa Polo", "Camisa polo de algodão", 59.90, True),
    ("Calça Jeans", "Calça jeans azul", 79.90, True),
    ("Tênis Esportivo", "Tênis esportivo confortável", 99.90, True)
]

# Executar a consulta SQL para inserir os produtos
cursor.executemany(
    '''INSERT INTO produtos(nome, descricao, valor, disponivel) VALUES (?, ?, ?, ?)''', produtos)
conn.commit()
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos ORDER BY valor ASC')
    produtos = cursor.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos)


@app.route('/novo_paciente', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']
        disponivel = request.form.get('disponivel', False)

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO produtos(nome,descricao,valor,disponivel) VALUES (?,?,?,?)''',
                       (nome, descricao, valor, disponivel))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('novo_produto.html')


@app.route('/apagar_produtos')
def apagar_produtos():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute(''' DELETE FROM produtos ''')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
