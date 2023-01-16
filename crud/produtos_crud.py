# Importação das bibliotecas
from database_creation.criar_db import connectionDB
from flask import flash


# Define uma função chamada "get_all_produtos" que não aceita nenhum parametro.
#  A função cria uma conexão com a base de dados, utilizando uma função chamada
#  "connectionDB", e cria um cursor para essa conexão. Em seguida, define uma string
#  de consulta SQL para selecionar todos os campos (*) de todas as linhas da tabela
#  "produto". A função executa então a consulta, usando o cursor, e armazena o resultado
#  na variável "produtos". Por fim, a função retorna o resultado da consulta e a conexão
#  com a base de dados.
def get_all_produtos():
    con = connectionDB()
    cur = con.cursor()
    query = ''' select * from produto'''
    produtos = cur.execute(query)
    return produtos, con

# Define uma função chamada "dicionario_produtos" que não aceita nenhum parametro. A função
#  chama outra função chamada "get_all_produtos" para obter todos os produtos da base de dados
#  e armazena o resultado numa lista chamada "produtos". Em seguida, a função percorre cada produto
#  da lista de produtos e cria um dicionário para cada um deles com os valores dos campos "id",
#  "nome", "descricao", "unidades", "preco" e "imagem". A função adiciona cada dicionário de um
#  produto numa lista e, por fim, retorna a lista de dicionários de produtos. A função também
#  fecha a conexão com a base de dados.
def dicionario_produtos():
    query_produtos, con = get_all_produtos()
    produtos = []
    for produto in query_produtos:
        novo_produto = {'id': produto[0],
                        'nome':produto[1],
                        'descricao':produto[2],
                        'unidades':produto[3],
                        'preco':produto[4],
                        'imagem':produto[5] }
        produtos.append(novo_produto)
    con.close()
    return produtos

# Define uma função chamada "criar_produto" que aceita um parametro chamado "produto". A função tenta
#  criar uma conexão com a base de dados, utilizando uma função chamada "connectionDB", e cria um cursor
#  para essa conexão. Em seguida, define uma string de inserção SQL para inserir valores nas colunas
#  "nome", "descricao", "unidades", "preco" e "imagem" da tabela "produto". A função executa então a
#  string de inserção, utilizando o cursor, e passa os valores dos campos do dicionário "produto" como
#  argumentos. A função faz commit da transação e fecha a conexão com a base de dados. Se a operação de
#  inserção falhar, a função lança uma exceção e mostra uma mensagem de erro. Se a operação de inserção
#  for bem-sucedida, a função mostra uma mensagem de sucesso.
def criar_produto(produto):
    try:
        con = connectionDB()
        cur = con.cursor()
        insert = """INSERT INTO produto(nome,descricao,unidades,preco,imagem) 
                VALUES (?,?,?,?,?);"""

        cur.execute(insert, (produto['nome'], produto['descricao'],produto['unidades'], 
                                produto['preco'], produto['imagem']))
        con.commit()
        con.close()
        flash('Produto Inserido com sucesso', 'success')
    except:
        flash('Produto já existente, altere apenas a quantidade', 'error')

# Define uma função chamada "get_produto" que aceita um parametro chamado "id". A função cria uma conexão
#  com a base de dados e cria um cursor para executar uma consulta SQL. A consulta seleciona todas as
#  colunas da tabela "produto" onde o "id" é igual ao valor passado como parametro para a função. O resultado
#  da consulta é guardado na variável "produto" e a função retorna o valor de "produto" e a conexão com a base de dados.
def get_produto(id):
        con = connectionDB()
        cur = con.cursor()
        select = f"""select * from produto where id = {id};"""
        produto = cur.execute(select)
        return produto, con

# Define uma função chamada "del_produto" que aceita um parametro chamado "id". A função tenta criar uma conexão
#  com a base de dados e criar um cursor para executar uma consulta SQL. A consulta remove a linha da tabela
#  "produto" onde o "id" é igual ao valor passado como parametro para a função. Se a consulta for bem sucedida,
#  o commit é executado e uma mensagem de sucesso é exibida. Se houver algum erro, uma mensagem de erro é exibida.
#  Independentemente do sucesso ou falha da operação, a conexão com a base de dados é fechada no final.
def del_produto(id):
    try:
        con = connectionDB()
        cur = con.cursor()
        select = f"""Delete from produto where id = {id};"""
        cur.execute(select)
        con.commit()
        flash('Produto Removido com sucesso', 'success')
    except:
        flash('Não foi possível apagar o produto', 'error')
    finally:
        con.close()

# Define uma função chamada "update_produto" que aceita os parametros chamados "id" e "produto_com_update".
#  A função tenta criar uma conexão com a base de dados e criar um cursor para executar uma consulta SQL de
#  atualização. A consulta atualiza os valores da tabela "produto" onde o "id" é igual ao valor passado como
#  parametro para a função. Os novos valores são fornecidos pelo parametro "produto_com_update", que é um
#  dicionário que contem os campos a serem atualizados. Se a consulta for bem sucedida, o commit é executado
#  e uma mensagem de sucesso é exibida. Se houver algum erro, uma mensagem de erro é exibida. Independentemente
#  do sucesso ou falha da operação, a conexão com a base de dados é fechada no final.
def update_produto(id, produto_com_update):
    try:
        con = connectionDB()
        cur = con.cursor()
        update = f"""UPDATE produto
                     SET nome = ?, descricao = ?,
                         unidades = ?, preco = ?,
                         imagem = ?
                     WHERE id = ?;
                  """
        cur.execute(update, (produto_com_update['nome'],produto_com_update['descricao'], 
                             produto_com_update['unidades'],produto_com_update['preco'], 
                             produto_com_update['imagem'], id))
        con.commit()
        flash('Produto Atualizado com sucesso', 'success')
    except:
        flash('Não foi possível Atualizar o produto', 'error')
    finally:
        con.close()

# Define uma função chamada "select_top_four". Ela cria uma conexão com a base de dados e cria um cursor para
#  executar uma consulta SQL. A consulta seleciona todas as colunas da tabela "produto" e retorna apenas os 4
#  primeiros resultados (LIMIT 4). O resultado da consulta é guardado na variável "top4_produtos" e a função
#  retorna o valor de "top4_produtos" e a conexão com a base de dados.
def select_top_four():
    con = connectionDB()
    cur = con.cursor()
    select = f"""SELECT * FROM produto LIMIT 4;"""
    top4_produtos = cur.execute(select)
    return top4_produtos, con

# Define uma função chamada "select_by_id_and_top_four" que aceita um parametro chamado "id". Ela cria uma conexão
#  com a base de dados e cria dois cursores. O primeiro cursor é utilizado para executar uma consulta SQL que
#  seleciona todas as colunas da tabela "produto" e retorna apenas os 4 primeiros resultados (LIMIT 4). O resultado
#  da consulta é guardado na variável "top4". O segundo cursor é utilizado para executar uma consulta SQL que seleciona
#  todas as colunas da tabela "produto" onde o "id" é igual ao valor passado como parametro para a função. O resultado
#  da consulta é guardado na variável "prod". A função retorna os valores de "prod", "top4" e a conexão com a base de dados.
def select_by_id_and_top_four(id):
    con = connectionDB()
    cur = con.cursor() 
    cur1 = con.cursor()
    select = f"""SELECT * FROM produto LIMIT 4;"""
    top4 = cur.execute(select)
    select1 = f"""select * from produto where id = {id};"""
    prod = cur1.execute(select1)
    return prod, top4, con
