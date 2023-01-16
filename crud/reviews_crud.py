from datetime import datetime
from database_creation.criar_db import connectionDB


# Funcao get_all_reviews recupera todas as revisões de um determinado produto a partir de uma base de dados. Ele
#  faz isso conectando-se à base de dados, criando um cursor e usando uma consulta SQL para selecionar todas as 
# revisões do produto com o ID especificado, juntamente com algumas informações adicionais sobre o usuário que fez 
# a revisão. Em seguida, o código executa a consulta e armazena o resultado em uma variável "resultado". Por fim, o 
# código fecha a conexão com a base de dados e retorna o resultado da consulta.
def get_all_reviews(id):
    con = connectionDB()
    cur = con.cursor()
    select = f"""
                select r.id, r.comentario, r.rating, r.data_adicionado, r.id_utilizador,r.id_produto, u.nome
                from review r
                inner join utilizador u on u.id = id_utilizador
                where id_produto = {int(id)};
              """
    cur.execute(select)
    result = cur.fetchall()
    return result


# Funcao gerar_review adiciona uma nova review para um produto em uma base de dados. Ele faz isso conectando-se à base de dados, 
# criando um cursor e usando uma consulta SQL para inserir uma nova linha na tabela de reviews com os valores especificados para 
# a classificação, comentário, data de adição, ID do usuário e ID do produto. Em seguida, o código executa a consulta e confirma 
# a alteração na base de dados. Por fim, o código fecha a conexão com a base de dados.
def gerar_review(rating, comentario, id_utilizador, id_produto):
    data_adicionado = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    con = connectionDB()
    cur = con.cursor()
    insert = f"""
                insert into review (comentario, rating, data_adicionado, id_utilizador, id_produto)
                values('{comentario}',{rating}, '{data_adicionado}', {id_utilizador}, {id_produto});
              """
    cur.execute(insert)
    con.commit()
    con.close()