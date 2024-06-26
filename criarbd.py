# Importando SQlite
import sqlite3 as lite

# criando conexão
con = lite.connect('dados.db')

# Criando tabela de categoria
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT )")

    # Criando tabela de receitas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Receitas(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL )")

        # Criando tabela de Gastos
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Gastos(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL )")
    

