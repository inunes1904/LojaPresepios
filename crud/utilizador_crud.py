from database_creation.criar_db import connectionDB
from flask import flash, session, redirect, url_for

# função "get_user_function" e é usada para obter a função de um utilizador com base em seu ID. A função estabelece 
# uma conexão com o base de dados, cria um cursor e executa uma consulta SQL que seleciona a função do 
# utilizador com o ID especificado. A função retorna o resultado da consulta como uma string.
def get_user_function(id):
    con = connectionDB()
    cur = con.cursor()
    select = f""" select funcao from utilizador_role where id_utilizador = {id} """
    cur.execute(select)
    resultado = cur.fetchone()[0]
    con.close()
    return resultado


# função  "criar_utilizador" e é usada para criar um novo utilizador na base de dados. A função recebe um dicionário 
# com os detalhes do utilizador e estabelece uma conexão com o base de dados, cria um cursor e executa uma consulta 
# SQL para inserir os detalhes do utilizador na tabela de utilizadores. Se a consulta for bem-sucedida, a função retorna 
# True e exibe uma mensagem de sucesso. Se houver um erro ao executar a consulta, a função exibe uma mensagem de erro.
def criar_utilizador(utilizador):
    try:
        con = connectionDB()
        cur = con.cursor()
        insert = """INSERT INTO utilizador(email,nome,password,salt) 
                    VALUES (?,?,?,?);"""

        cur.execute(insert, (utilizador['email'], utilizador['nome'],utilizador['password'], 
                                utilizador['salt']))
        con.commit()
        con.close()
        flash('Utilizador criado com sucesso', 'success')
        return True
    except:
        flash('Email já existente, altere e tente novamente', 'error')


# função chamada "recebe_user_da_db" que recebe um parâmetro chamado "email_input". A função tenta estabelecer uma conexão 
# com uma base de dados, criar um cursor e executar uma consulta na tabela "utilizador" da base de dados, buscando pelo email 
# igual ao valor do parâmetro "email_input". Se a consulta for bem-sucedida, a função retorna o resultado da consulta e a 
# conexão com a base de dados. Se ocorrer algum erro durante o processo, a função retorna o valor "False" e a conexão com a base de dados.
def recebe_user_da_db(email_input):
    try:
        con = connectionDB()
        cur = con.cursor()
        select_user = f""" Select * from utilizador where email = '{email_input}';"""
        user = cur.execute(select_user) 
        return user, con
    except:
        return False, con


# função chamada "get_utilizador" que recebe um parâmetro chamado "id". A função tenta estabelecer uma conexão com uma base de dados, 
# criar um cursor e executar uma consulta na tabela "utilizador" da base de dados, buscando pelo id igual ao valor do parâmetro "id". 
# Se a consulta for bem-sucedida, a função retorna o resultado da consulta e a conexão com a base de dados. Se ocorrer algum erro 
# durante o processo, a função retorna o valor "False" e a conexão com a base de dados.
def get_utilizador(id):
    try:
        con = connectionDB()
        cur = con.cursor()
        select_user = f""" Select * from utilizador where id = {id};"""
        user = cur.execute(select_user) 
        return user, con
    except:
        return False, con


# Este código define uma função chamada "update_utilizador" que recebe dois parâmetros: "utilizador" e "id". A função tenta estabelecer 
# uma conexão com uma base de dados, criar um cursor e executar uma consulta de atualização na tabela "utilizador" da base de dados. 
# A consulta atualiza os valores das colunas "email", "nome", "cidade", "localidade", "morada", "codigoPostal", "password", "salt", 
# "contacto" e "morada2" da linha cujo id é igual ao valor do parâmetro "id", com os valores contidos no dicionário "utilizador". Se a 
# consulta for bem-sucedida, a função confirma a atualização e fecha a conexão com a base de dados. Se ocorrer algum erro durante o 
# processo, a função exibe uma mensagem de erro.
def update_utilizador(utilizador, id):
    try:
        con = connectionDB()
        cur = con.cursor()
        update_user =   """UPDATE utilizador
                           SET email = ?, nome = ?, cidade = ?,
                           localidade = ?, morada = ?, codigoPostal = ?,
                           password = ?,salt = ?,contacto = ?,
                           morada2 = ?
                           WHERE id = ?;
                        """
        update_user = cur.execute(update_user, (utilizador["email"], utilizador["nome"], utilizador["cidade"], 
                                                utilizador["cidade"], utilizador["morada"], utilizador["codigoPostal"],
                                                utilizador["password"], utilizador["salt"], utilizador["contacto"],
                                                utilizador["morada2"], id )) 
        con.commit()
        con.close()
        flash('Utilizador atualizado com sucesso', 'success')
        return True
    except:
        flash('Não foi possivel actualizar o Perfil', 'error')