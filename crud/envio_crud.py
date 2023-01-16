# Importação das bibliotecas
from datetime import datetime
from database_creation.criar_db import connectionDB

# Define uma função chamada "criar_envio" que aceita três parametros: "jsInfo", "idUtilizador" e "idEnc",
#  seguido de uma conexão de base de dados "con". A função primeiro cria uma variável chamada "data_adicionado"
#  e atribui a ela a data atual no formato "dd/mm/aaaa hh:mm:ss". Em seguida, cria variáveis chamadas "morada",
#  "cidade", "localidade" e "codPostal" e atribui a elas os valores correspondentes dos elementos "Morada", "Morada2",
#  "Cidade", "Localidade" e "CodigoPostal", respectivamente, do dicionário "jsInfo". A função cria então um cursor
#  para a conexão da base de dados "con" e define a string de inserção SQL para inserir os valores das variáveis
#  "morada", "cidade", "localidade", "codPostal", "data_adicionado", "idUtilizador" e "idEnc" numa tabela chamada
#  "envio_info". Em seguida, a função executa a string de inserção utilizando o cursor e faz commit da transação.
#  Por fim, a função fecha a conexão com a base de dados.
def criar_envio(jsInfo, idUtilizador, idEnc, con):
    data_adicionado = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    morada = jsInfo['data']['Morada']+' - '+jsInfo['data']['Morada2']
    cidade = jsInfo['data']['Cidade']
    localidade = jsInfo['data']['Localidade']
    codPostal = jsInfo['data']['CodigoPostal']
    cursor = con.cursor()

    insert = f""" INSERT into envio_info
                  (morada, cidade, localidade, codigoPostal, 
                  data_adicionado, id_utilizador, id_encomenda) 
                  values ('{morada}', '{cidade}', '{localidade}', 
                  '{codPostal}', '{data_adicionado}',
                  {idUtilizador}, {idEnc});             
              """
    cursor.execute(insert)
    con.commit()
    con.close()

# Define uma função chamada "criar_envio_nouser" que aceita dois parametros: "jsInfo" e "idEnc". A função cria
#  uma variável chamada "data_adicionado" e atribui a ela a data atual no formato "dd/mm/aaaa hh:mm:ss". Em seguida,
#  cria variáveis chamadas "nome", "email", "morada", "cidade", "localidade" e "codPostal" e atribui a elas os
#  valores correspondentes dos elementos "Nome", "Email", "Morada", "Morada2", "Cidade", "Localidade" e "CodigoPostal",
#  respectivamente, do dicionário "jsInfo". A função cria então uma conexão com a base de dados, utilizando uma função
#  chamada "connectionDB", e cria um cursor para essa conexão. Em seguida, define a string de inserção SQL para inserir
#  os valores das variáveis "morada", "cidade", "localidade", "codPostal", "data_adicionado", "idEnc", "nome" e "email"
#  numa tabela chamada "envio_info". A função também insere "NULL" como valor para o campo "id_utilizador" na tabela.
#  Em seguida, a função executa a string de inserção utilizando o cursor e faz commit da transação. Por fim, a função
#  fecha a conexão com a base de dados.
def criar_envio_nouser(jsInfo, idEnc):
    nome = jsInfo['data']['Nome'] 
    email = jsInfo['data']['Email']
    morada = jsInfo['data']['Morada'] +" - "+jsInfo['data']['Morada2']
    cidade = jsInfo['data']['Cidade']
    localidade = jsInfo['data']['Localidade']
    codPostal = jsInfo['data']['CodigoPostal'] 
    data_adicionado = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    con = connectionDB()
    cursor = con.cursor()
    insert = f""" INSERT into envio_info
                  (morada, cidade, localidade, codigoPostal, 
                  data_adicionado, id_utilizador, id_encomenda, nome, email) 
                  values ('{morada}', '{cidade}', '{localidade}', 
                  '{codPostal}', '{data_adicionado}',
                  NULL, {idEnc}, '{nome}', '{email}');             
              """
    cursor.execute(insert)
    con.commit()
    con.close()