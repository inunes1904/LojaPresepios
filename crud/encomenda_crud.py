from database_creation.criar_db import connectionDB
from flask import flash, session, redirect, url_for
from datetime import datetime

# funcao create_encomenda_nouser cria uma nova encomenda no base de dados. Ela estabelece uma conexão com o base de dados,
#  cria um cursor e, em seguida, gera uma data e hora atual e armazena-a na variável 'data'. Em seguida, gera um ID de transação 
# usando a hora atual e armazena-o na variável 'transacao_id'. Em seguida, insere uma nova linha na tabela 'encomenda' com os valores 
# 'terminada' como 1, a 'data_encomenda' como a data atual, a 'transacao_id' como o ID de transação gerado e 'id_utilizador' como 
# nulo. Finalmente, a função retorna o ID da encomenda recém-inserida.
def create_encomenda_nouser():
    con = connectionDB()
    cur = con.cursor()
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    transacao_id = datetime.now().timestamp()
    insert = f""" insert into encomenda (terminada, data_encomenda, transacao_id, id_utilizador)
                    values ( 1, '{data}', '{transacao_id}', Null);"""
    cur.execute(insert)
    idenc = cur.lastrowid
    con.commit()
    con.close()
    return idenc

# Esta função adiciona um produto à uma encomenda específica no base de dados. Ela obtém a data atual e estabelece uma conexão com 
# o base de dados, cria um cursor e, em seguida, insere uma nova linha na tabela 'encomenda_produto' com os valores 'quantidade' como 
# a quantidade especificada pelo argumento, 'data_adicionado' como a data atual, 'id_encomenda' como o ID da encomenda especificado 
# pelo argumento e 'id_produto' como o ID do produto especificado pelo argumento. A função então salva as alterações no base de dados 
# e fecha a conexão.
def create_enc_prod_nouser(idenc, idproduto, quantidade):
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    con = connectionDB()
    cur = con.cursor()
    insert = f""" INSERT into encomenda_produto (quantidade, data_adicionado,
                  id_encomenda, id_produto) values({quantidade}, '{data}', {idenc},
                  {idproduto}); """
    cur.execute(insert)
    con.commit()
    con.close()


# Esta função procura ou cria uma encomenda para um determinado utilizador na base de dados. Ela estabelece uma conexão com a base de dados, 
# cria um cursor e, em seguida, verifica se o argumento 'lastrow' foi especificado. Se não foi, a função executa uma consulta para selecionar 
# todas as encomendas não terminadas para o utilizador especificado pelo argumento 'utilizadorId'. Se o argumento 'lastrow' foi especificado, a 
# função executa uma consulta para selecionar a encomenda com o ID especificado pelo argumento. Em seguida, a função verifica se há alguma 
# encomenda retornada pela consulta. Se não houver, a função gera uma nova data e hora atual e um ID de transação e insere uma nova linha 
# na tabela 'encomenda' com os valores 'terminada' como 0, 'data_encomenda' como a data atual, 'transacao_id' como o ID de transação gerado 
# e 'id_utilizador' como o ID do utilizador especificado pelo argumento. A função então chama a si mesma recursivamente, passando o ID da 
# encomenda recém-inserida como o argumento 'lastrow'. Se houver alguma encomenda retornada pela consulta, a função simplesmente retorna 
# essa encomenda e a conexão com o base de dados.
def get_or_create_encomenda(utilizadorId, lastrow=None):
    con = connectionDB()
    cur = con.cursor()
    if lastrow is None:
        select = f"""select * from encomenda where id_utilizador = {int(utilizadorId)} and terminada = 0;"""
    else:
        select = f"""select * from encomenda where id = {lastrow};"""
    cur.execute(select)
    encomenda = cur.fetchall()
    
    last = cur.lastrowid
    if not len(encomenda) > 0:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        transacao_id = datetime.now().timestamp()
        insert = f""" insert into encomenda (terminada, data_encomenda, transacao_id, id_utilizador)
                        values ( 0, '{data}', '{transacao_id}', {int(utilizadorId)}  );"""
        cur2 = con.cursor()
        cur2.execute(insert)
        con.commit()
        last = cur2.lastrowid
        con.close()
        get_or_create_encomenda(utilizadorId, lastrow=last)
    else:
        return encomenda, con

# Esta função procura ou cria um relacionamento entre uma encomenda e um produto específicos na base de dados. Ela 
# estabelece uma conexão com a base de dados, cria um cursor e, em seguida, executa uma consulta para selecionar 
# o relacionamento entre a encomenda com o ID especificado pelo argumento 'id_enc' e o produto com o ID especificado 
# pelo argumento 'id_prod'. Em seguida, a função verifica se há algum relacionamento retornado pela consulta. Se não 
# houver, a função gera uma nova data e hora atual e insere uma nova linha na tabela 'encomenda_produto' com os 
# valores 'quantidade' como 0, 'data_adicionado' como a data atual, 'id_encomenda' como o ID da encomenda 
# especificado pelo argumento e 'id_produto' como o ID do produto especificado pelo argumento. A função então chama 
# a si mesma recursivamente, passando os mesmos argumentos. Se houver algum relacionamento retornado pela consulta, 
# a função simplesmente retorna esse relacionamento e a conexão com a base de dados.
def get_or_create_enc_prod(id_enc, id_prod):
    
    con = connectionDB()
    cur = con.cursor()
    select = f"""select * from encomenda_produto where id_encomenda = {int(id_enc)} and id_produto = {int(id_prod)};"""
    cur.execute(select)
    enc_prod_obj = cur.fetchall()

    if not len(enc_prod_obj) > 0:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")      
        insert = f""" insert into encomenda_produto (quantidade, data_adicionado, id_encomenda, id_produto)
                        values ( 0, '{data}', '{int(id_enc)}', {int(id_prod)}  );"""
        cur2 = con.cursor()
        enc_prod_obj = cur2.execute(insert)
        con.commit()
        get_or_create_enc_prod(id_enc, id_prod)
    else:
        return enc_prod_obj, con

# Esta função atualiza a quantidade de um determinado produto em uma encomenda específica na base de dados. Ela estabelece 
# uma conexão com a base de dados, cria um cursor e, em seguida, atualiza a quantidade para o valor especificado pelo argumento 
# 'quantidade' para o relacionamento entre a encomenda com o ID especificado pelo argumento 'id_enc' e o produto com o ID 
# especificado pelo argumento 'produto_id'. A função então salva as alterações na base de dados e fecha a conexão. Finalmente, 
# a função retorna a quantidade atualizada.
def add_rem_quant_enc_prod(id_enc, quantidade, produto_id):
    con = connectionDB()
    cur = con.cursor()
    update = f"""UPDATE encomenda_produto
                     SET quantidade = {quantidade}
                     WHERE id_encomenda = {id_enc} and id_produto = {produto_id};
              """
    
    cur.execute(update)
    con.commit()
    con.close()
    return quantidade

# Esta função remove um relacionamento entre uma encomenda e um produto específicos da base de dados. Ela estabelece 
# uma conexão com a base de dados, cria um cursor e, em seguida, remove o relacionamento com o ID especificado pelo 
# argumento 'id_enc_prod' da tabela 'encomenda_produto'. A função então salva as alterações na base de dados e fecha
# a conexão.
def delete_enc_prod(id_enc_prod):
    con = connectionDB()
    cur = con.cursor()
    delete = f"""DELETE FROM encomenda_produto
                 WHERE id = {id_enc_prod};
              """
    cur.execute(delete)
    con.commit()
    con.close()


# Esta função retorna uma lista de produtos no carrinho de compras para um determinado utilizador na base de dados. 
# Ela estabelece uma conexão com a base de dados, cria um cursor e, em seguida, executa uma consulta para selecionar 
# todos os produtos relacionados a encomendas não terminadas para o utilizador especificado pelo argumento 'utilizadorID'.
# A função então retorna os produtos retornados pela consulta e a conexão com a base de dados.
def get_prods_cart(utilizadorID):
    con = connectionDB()  
    cur = con.cursor()
    select = f"""SELECT  ecp.id_produto,  ecp.quantidade , prod.nome, prod.preco, 
                 prod.imagem, enc.id_utilizador, enc.terminada, enc.id
                 FROM encomenda_produto ecp, produto prod, encomenda enc
                 JOIN produto ON prod.id = ecp.id_produto
                 WHERE  enc.terminada = 0 and enc.id_utilizador = {utilizadorID} and enc.id = id_encomenda
                 group by prod.nome order by ecp.id_produto;
                """
    cur.execute(select)
    produtos = cur.fetchall()
    return produtos, con
        
        
# Esta função remove um produto específico de uma encomenda específica da base de dados. Ela estabelece uma conexão 
# com a base de dados, cria um cursor e, em seguida, remove o relacionamento entre o produto com o ID especificado 
# pelo argumento 'id_Produto' e a encomenda com o ID especificado pelo argumento 'id_Encomenda' da tabela 
# 'encomenda_produto'. A função então salva as alterações na base de dados e fecha a conexão.
def delete_cart_item(id_Produto, id_Encomenda):
    con = connectionDB()
    cur = con.cursor() 
    delete = f""" DELETE FROM encomenda_produto where id_produto = {id_Produto} 
                  and id_encomenda = {id_Encomenda} ;
              """
    cur.execute(delete)
    con.commit()
    con.close()


# Esta função marca uma encomenda como terminada na base de dados e atribui um ID de transação a ela. Ela cria um 
# cursor com a conexão com a base de dados especificada pelo argumento 'con' e, em seguida, atualiza a coluna 'terminada' 
# para 1 e a coluna 'transacao_id' para o valor especificado pelo argumento 'id_transacao' para a encomenda com o ID especificado 
# pelo argumento 'id_Encomenda' na tabela 'encomenda'. A função então salva as alterações na base de dados e fecha a conexão.
def finalizar_encomenda(id_Encomenda, id_transacao, con):
    cur = con.cursor()
    update = f""" UPDATE encomenda
                  SET terminada = 1, transacao_id = {id_transacao}
                  where id = {id_Encomenda};"""
    cur.execute(update)
    con.commit()
    con.close()