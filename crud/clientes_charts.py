from database_creation.criar_db import connectionDB
from datetime import datetime


# Esta função retorna os top 'N' clientes com as maiores compras na base de dados. Ela estabelece 
# uma conexão com a base de dados, cria um cursor e, em seguida, executa uma consulta para selecionar 
# o nome do cliente, o ID da encomenda, a quantidade de cada produto comprado, o preço de cada produto 
# comprado, e o total gasto em cada encomenda realizada por um cliente. A função então retorna os resultados 
# da consulta classificados pelo total gasto em cada encomenda em ordem decrescente e limitados ao número 
# especificado pelo argumento 'num'. Finalmente, a função fecha a conexão com a base de dados.
def get_top_clientes(num):
    con = connectionDB()
    cur = con.cursor()
    select = f"""
                select  u.nome, e.id 'id_encomenda', enc.quantidade,  sum(p.preco) 'preco_produto', sum((p.preco*enc.quantidade)) 'total_produto'
                from utilizador u
                inner join  encomenda  e on u.id = e.id_utilizador
                inner join encomenda_produto enc on e.id = enc.id_encomenda
                inner join produto p on p.id = enc.id_produto group by u.nome  order by total_produto DESC limit {num};
              """
    cur.execute(select)
    resultado = cur.fetchall()
    con.close()
    return resultado

# Esta função retorna a lista de meses em que houve vendas e um dicionário com informações sobre as vendas de 
# cada cliente. Ela estabelece uma conexão com a base de dados, cria um cursor e, em seguida, executa uma 
# consulta para selecionar o nome do cliente, o mês da encomenda, e o total de cada encomenda realizada por 
# um cliente. A função então itera sobre os resultados da consulta, adiciona cada mês único à lista 'meses' 
# e adiciona as informações sobre as vendas de cada cliente ao dicionário 'clientes'. Finalmente, a função 
# classifica a lista 'meses' e fecha a conexão com a base de dados antes de retornar 'meses' e 'clientes'.
def get_vendas_clientes_mes():
  con = connectionDB()
  cur = con.cursor()
  select = f"""
              select   u.nome, substr(e.data_encomenda, 4, 2) as 'Mes',  sum(p.preco*enc.quantidade) 'total'
              from utilizador u
              inner join  encomenda  e on u.id = e.id_utilizador
              inner join encomenda_produto enc on e.id = enc.id_encomenda
              inner join produto p on p.id = enc.id_produto group by e.id  ;
            """
  cur.execute(select)
  resultado = cur.fetchall()
  meses = []
  clientes = {}
  for item in resultado:
    if item[1] not in meses:
      meses.append(int(item[1])-1)
    
    if item[0] not in clientes.keys():
      clientes[item[0]] = { "vendas": [int(item[2])], "mes": [int(item[1])], }  
    else:
      clientes[item[0]]["vendas"].append(int(item[2]))
      clientes[item[0]]["mes"].append(int(item[1]))
  
  meses.sort()

  con.close()
  return meses, clientes
  

# Esta função retorna a porcentagem de encomendas realizadas por utilizadores registrados e a porcentagem 
# de encomendas realizadas por utilizadores não registrados. Ela estabelece uma conexão com a base de dados, 
# cria dois cursores e, em seguida, executa duas consultas. A primeira consulta seleciona a contagem de 
# encomendas realizadas por utilizadores não registrados e a segunda consulta seleciona a contagem de encomendas 
# realizadas por utilizadores registrados. A função então calcula a porcentagem de encomendas realizadas por cada 
# tipo de utilizador em relação ao total de encomendas e retorna essas porcentagens. Se ocorrer uma exceção 
# durante o cálculo da porcentagem, a função retorna None para ambas as porcentagens.
def users_naousers():
  con = connectionDB()
  cur = con.cursor()
  cur_2 = con.cursor()
  select_nao_users = """
                        select count(id)  as 'Contador'
                        from encomenda
                        where id_utilizador is NULL;
                        
                     """
  select_users = """
                        select count(id)  as 'Contador'
                        from encomenda
                        where id_utilizador is not NULL;
                        
                     """
  cur.execute(select_nao_users)
  cur_2.execute(select_users)
  
  n_nao_users = cur.fetchall()
  n_users = cur_2.fetchall()
  
  total = n_nao_users[0][0]+n_users[0][0]

  try:
    users_p = round(n_users[0][0]/total*100,2)
    nao_users_p = round(n_nao_users[0][0]/total*100, 2)
  except:
    users_p = None
    nao_users_p = None

  return users_p, nao_users_p