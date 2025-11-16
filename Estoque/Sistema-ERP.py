#Tentando implementar Banco de Dados e biblioteca para registrar datas
import sqlite3
from datetime import datetime

def iniciar(conn, cursor):
    #Aqui vou inciar/verificar as tabelas que usarei no sistema
    cursor.execute("""CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor_unit REAL NOT NULL,
    quantidade INTEGER NOT NULL
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS movimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    datahora TEXT NOT NULL,
    quantidade_movimentada INTEGER NOT NULL,
    quantidade_final INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES estoque(id) ON DELETE CASCADE
)""")
    return conn, cursor

def cadastrar_item(conn, cursor, nome, categoria, valor_unit, quantidade):
    insert_estoque = ("""INSERT INTO estoque (nome, categoria, valor_unit, quantidade) VALUES (?, ?, ?, ?)""")
    cursor.execute(insert_estoque, (nome, categoria, valor_unit, quantidade))
    cursor.execute("SELECT id FROM estoque WHERE nome = ?", (nome, ))
    id_compact = cursor.fetchone()
    id = id_compact[0]
    insert_movimentos = ("INSERT INTO movimentos (item_id, tipo, datahora, quantidade_movimentada, quantidade_final) VALUES(?, ?, ?, ?, ?)")
    tipo = "Cadastro"
    data_n = datetime.now()
    datahora = data_n.strftime("%d/%m/%Y, %H:%M:%S")
    cursor.execute(insert_movimentos, (id, tipo, datahora, quantidade, quantidade))
    print(f"Produto {nome} adicionado com sucesso!")
    conn.commit()
    return

def verificar_estoque(conn, cursor): #def para verificar se há linhas no estoque
    cursor.execute("SELECT COUNT(*) FROM estoque")
    linhas_compact = cursor.fetchone()
    verificador = linhas_compact[0]
    if verificador == 0:
        return verificador
    return 1

def alerta_estoque(conn, cursor): #def para criar um alerta para o usuário caso o estoque esteja baixo
    verify_estoque = verificar_estoque(conn, cursor)
    if verify_estoque != 0:
        quantidade_alerta = 5
        cursor.execute("SELECT * FROM estoque WHERE quantidade <= ?", (quantidade_alerta, ))
        produtos_estoque_baixo = cursor.fetchall()
        for produto in produtos_estoque_baixo:
            print(f"ALERTA - Produto ID {produto['id']} - Nome: {produto['nome']} - ESTOQUE BAIXO {produto['quantidade']}")
            print("="*100)
        conn.commit()
        return


#Menu Principal do Sistema
print("--          Gerenciamento de Estoques          --")
print("="*50)
#Conexão com o banco de dados e cursor para executar os comandos SQL
conn = sqlite3.connect('estoque.db')
#Comando para formatar as saídas do banco de dados para um dicionário facilitando o manejo dos dados
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

iniciar(conn, cursor)
while True:
    alerta_estoque(conn, cursor)
    while True:
        try:
            verify = int(input("Digite qual operação você deseja fazer:\n1 - Cadastrar Produto\n2 - Sair do sistema\n"))
            break
        except ValueError:
            print("Digite uma opção válida!")
            continue
    if verify == 1:
        nome = input("Digite o nome do produto: ")
        categoria = input("Digite a categoria do produto(Limpeza, Alimentos, etc): ")
        while True:
            try:
                valor_unit = float(input("Digite o valor unitário dos produtos: "))
                quantidade = int(input("Digite a quantidade: "))
                break
            except ValueError:
                print("Entrada inválida! Tente novamente.")
                continue
            except Exception as e:
                print(f"Ocorreu um erro inesperado {e}")
                print("Tente Novamente.")
                continue
        cadastrar_item(conn, cursor, nome, categoria,valor_unit, quantidade)
        print("\n")
        
    elif verify == 2:
        print("Encerrando Operação...\nObrigado por usar nossos serviços.")
        conn.close()
        break

    else:
        print("Opção inválida. Escolha uma das opções válidas (1 e 2).")