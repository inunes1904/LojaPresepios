from database_creation.criar_db import connectionDB
from datetime import datetime

# Funcao vendas_line_chart tem o objetivo de recolher a informacao necessaria para a criacao de  um gráfico de 
# linhas de vendas para um determinado ano. Ele faz isso conectando-se a uma base de dados, usando uma consulta 
# SQL para recuperar as informações de vendas para cada mês do ano especificado, e armazenando esses valores em 
# um array de vendas. Em seguida, o código fecha a conexão com a base de dados e retorna o array de vendas.
def vendas_line_chart(ano):
    con = connectionDB()
    cur = con.cursor()
    select = f"""
                select Mes, sum(Total_Produto) as 'Total_Vendido'
                from (
                        SELECT
                            e.id,
                            e.data_adicionado, 
                            substr(e.data_adicionado, 4, 2) as 'Mes',
                            substr(e.data_adicionado, 7,4) as 'Ano',
                            e.id_produto,
                            e.quantidade,
                            p.preco,
                            (p.preco*e.quantidade) as 'Total_Produto'
                        FROM encomenda_produto e, produto p
                        where e.id_produto = p.id and Ano = '{ano}'
                        group by e.id) as teste group by Mes;
            """
    cur.execute(select)
    resultado = cur.fetchall()
    vendas = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(resultado)):
        vendas[int(resultado[i][0])-1] = resultado[i][1]
    
    con.close()
    return vendas

# função chamada "get_vendas_hoje" que recebe um parâmetro "hoje". A função estabelece uma conexão com uma base de 
# dados, cria um cursor e executa uma consulta na tabela "encomenda_produto" da base de dados, selecionando o campo 
# "Vendido_Hoje" de uma tabela derivada chamada "vendido_hoje". A tabela derivada é criada a partir de uma cláusula 
# "SELECT" aninhada (subselect) e é criada a partir da junção da tabela "encomenda_produto" com a tabela "produto". 
# A consulta retorna o valor total de vendas realizadas no dia especificado pelo parâmetro "hoje". O resultado da 
# consulta é armazenado em uma variável "resultado" e, em seguida, é retornado pelo a função. Se o resultado da 
# consulta for "None", o valor zero é retornado em vez disso. A função fecha a conexão com a base de dados no final.
def get_vendas_hoje(hoje):
    con = connectionDB()
    cur = con.cursor()
    select = f"""
                select  sum(Total_Produto) as 'Vendido_Hoje'
                from (
							SELECT
								e.id,
								e.data_adicionado, 
								substr(e.data_adicionado, 1,10) as 'Data',
								e.id_produto,
								e.quantidade,
								p.preco,
								(p.preco*e.quantidade) as 'Total_Produto'
							FROM encomenda_produto e, produto p
							where e.id_produto = p.id and Data = '{hoje}'
							group by e.id) as vendido_hoje ;
              """
    cur.execute(select)
    resultado = cur.fetchone()
    con.close()
    return resultado[0] if resultado[0] != None else 0


# função chamada "encomendas_bar_chart" que recebe um parâmetro "ano". A função estabelece uma conexão com uma 
# base de dados, cria um cursor e executa uma consulta na tabela "encomenda" da base de dados, selecionando os 
# campos "Ano", "Mes" e "N_Encomendas" de uma tabela derivada chamada "Contar_Encomendas". A tabela derivada é 
# criada a partir de uma cláusula "SELECT" aninhada (subselect) e agrupa os dados pela id da encomenda. A consulta 
# retorna o número de encomendas realizadas em cada mês do ano especificado pelo parâmetro "ano". Os resultados 
# da consulta são armazenados em uma lista "resultado" e, em seguida, são transferidos para outra lista "encomendas", 
# que é inicializada com 12 elementos com valor zero. A lista "encomendas" é preenchida com os valores de "N_Encomendas" 
# de cada mês, na posição correspondente ao mês. Por fim, a função fecha a conexão com a base de dados e retorna a 
# lista "encomendas".
def encomendas_bar_chart(ano):
    con = connectionDB()
    cur = con.cursor()
    select =  f"""
                select Ano, Mes, count(Mes) as N_Encomendas 
                    from
                        (SELECT
                            id,
                            data_encomenda, 
                            substr(data_encomenda, 4, 2) as 'Mes',
                            substr(data_encomenda, 7,4) as 'Ano'
                        FROM encomenda 
                        group by id) as 'Contar_Encomendas'
                        where Ano = '{ano}' group by Mes;
               """
    cur.execute(select)
    resultado = cur.fetchall()
    encomendas = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(resultado)):
        encomendas[int(resultado[i][1])-1] = resultado[i][2]
  
    con.close()
    return encomendas


# função chamada "get_mais_vendidos" que não recebe nenhum parâmetro. A função estabelece uma conexão com uma
#  base de dados, cria um cursor e executa uma consulta na base de dados, selecionando os campos "Imagem", "Nome",
# "Un_Vendidas", "Preco" e "Receita" de uma tabela derivada da junção das tabelas "produto" e "encomenda_produto". 
# A tabela derivada é criada a partir de uma cláusula "SELECT" aninhada (subselect) e é denominada "Mais_Vendidos". 
# A consulta retorna os resultados ordenados pelo valor da coluna "Receita" em ordem decrescente. A função retorna 
# os resultados da consulta e fecha a conexão com a base de dados.
def get_mais_vendidos():
    con = connectionDB()
    cur = con.cursor()
    select =  """
                select Imagem, Nome, Un_Vendidas , Preco, (Un_vendidas*Preco) as 'Receita'  from
                (select  p.imagem as Imagem, p.nome as 'Nome' , SUM(enc.quantidade) as 'Un_Vendidas', p.preco as Preco
                from produto p, encomenda_produto enc
                where p.id = enc.id_produto
                group by p.id) 
                as Mais_Vendidos order by Receita DESC;
              """
    cur.execute(select)
    mais_vendidos = cur.fetchall()
    con.close()
    return mais_vendidos

