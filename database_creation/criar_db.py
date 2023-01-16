import random
import sqlite3
import string
from presepioapp.utilitarios import hash_password
from markupsafe import escape
from flask import current_app

# função chamada "connectionDB" que estabelece uma conexão com uma base de dados SQLite específica. A função usa o 
# módulo sqlite3 para se conectar à base de dados "app.db" na pasta "db". A conexão é então retornada pelo função e 
# pode ser usada em outras partes do código para realizar operações na base de dados.
def connectionDB():
    return sqlite3.connect('db/app.db')

#  função chamada "criar_base_de_dados" que cria várias tabelas em uma base de dados. A função estabelece uma conexão 
# com a base de dados, cria um cursor para realizar operações SQL e, em seguida, executa vários comandos SQL para criar 
# as tabelas "utilizador", "encomenda", "produto", "encomenda_produto", "envio_info", "utilizador_role", "review" e 
# "detalhes_pagamento". Algumas dessas tabelas possuem relações de chave estrangeira com outras tabelas, que são especificadas 
# nas declarações de tabela. Por fim, a função realiza o commit das alterações na base de dados e fecha a conexão com a base de dados.
def criar_base_de_dados():
    con = connectionDB()
    # Criar cursor para realizar operações SQL
    cur = con.cursor()
    # Comando SQL para criar a tabela de linguagens de programação.
    sql_script = '''

    CREATE TABLE "utilizador" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(255) NOT NULL UNIQUE,
	"nome"	VARCHAR(255) NOT NULL,
	"cidade"	VARCHAR(255),
	"localidade"	VARCHAR(255),
	"morada"	VARCHAR(255),
	"codigoPostal"	VARCHAR(255),
	"password"	VARCHAR(255) NOT NULL,
	"salt"	VARCHAR(255) NOT NULL,
	"contacto"	VARCHAR(13),
	"morada2"	VARCHAR(50),
	PRIMARY KEY("id")
    );
        
    CREATE TABLE "encomenda" (
	"id"	INTEGER NOT NULL,
	"terminada"	TINYINT(1) NOT NULL,
	"data_encomenda"	DATETIME NOT NULL,
	"transacao_id"	VARCHAR(255) NOT NULL,
	"id_utilizador"	BIGINT,
	FOREIGN KEY("id_utilizador") REFERENCES "utilizador"("id"),
	PRIMARY KEY("id")
    );
   
   CREATE TABLE `produto`(
        `id` INTEGER PRIMARY KEY,
        `nome` VARCHAR(255) Unique NOT NULL,
        `descricao` VARCHAR(255) NOT NULL,
        `unidades` INT NOT NULL,
        `preco` DECIMAL(8, 2) NOT NULL,
        `imagem` VARCHAR(255) NOT NULL
    );

    CREATE TABLE `encomenda_produto`(
        `id` INTEGER PRIMARY KEY NOT NULL,
        `quantidade` INT NOT NULL,
        `data_adicionado` DATETIME NOT NULL,
        `id_encomenda` BIGINT NOT NULL,
        `id_produto` BIGINT NOT NULL,
		FOREIGN KEY(id_encomenda) REFERENCES encomenda(id),
		FOREIGN KEY(id_produto) REFERENCES produto(id)
    );

    CREATE TABLE "envio_info" (
	"id"	INTEGER NOT NULL,
	"morada"	VARCHAR(255) NOT NULL,
	"cidade"	VARCHAR(255) NOT NULL,
	"localidade"	VARCHAR(255) NOT NULL,
	"codigoPostal"	VARCHAR(255) NOT NULL,
	"data_adicionado"	DATETIME NOT NULL,
	"id_utilizador"	BIGINT,
	"id_encomenda"	BIGINT NOT NULL,
	"nome"	VARCHAR(255),
	"email"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("id_encomenda") REFERENCES "encomenda"("id"),
	FOREIGN KEY("id_utilizador") REFERENCES "utilizador"("id")
    );

    CREATE TABLE `utilizador_role`(
        `id_utilizador` INTEGER UNIQUE  NOT NULL,
        `funcao` VARCHAR(10) NOT NULL,
		FOREIGN KEY(id_utilizador) REFERENCES utilizador(id)
    );

    CREATE TABLE `review`(
        `id` INTEGER PRIMARY KEY NOT NULL,
        `comentario` VARCHAR(255) NOT NULL,
        `rating` DECIMAL(1,1) NOT NULL,
        `data_adicionado` DATETIME NOT NULL,
		`id_utilizador` BIGINT NOT NULL,
        `id_produto` BIGINT NOT NULL,
		FOREIGN KEY(id_utilizador) REFERENCES utilizador(id),
		FOREIGN KEY(id_produto) REFERENCES produto(id)
    );

    '''
    # Executa o script de criacao de tabelas
    cur.executescript(sql_script)
    # Efetua o (commit) das mudanças
    con.commit()
    # Ao final, fechar a conexão com a base de dados.
    con.close()



# função chamada "criar_super_user" que insere um utilizador super utilizador na tabela de utilizadors de uma base de dados. A função recebe um 
# argumento "secret_key" que é usado para criptografar a senha do utilizador super utilizador. A função estabelece uma conexão com a base de 
# dados, cria um cursor para realizar operações SQL e, em seguida, gera uma "salt" aleatória usando o módulo "random" e o "string". A "salt" 
# é então usada em conjunto com a chave secreta e a senha para criptografar a senha do utilizador super utilizador. Em seguida, um novo registro 
# é inserido na tabela "utilizador" com as informações do utilizador super utilizador, incluindo a senha criptografada. Por fim, a função realiza o 
# commit das alterações na base de dados, fecha a conexão com a base de dados e retorna o ID do utilizador super utilizador.
def criar_super_user(app):
    con = connectionDB()
    # Criar cursor para realizar operações SQL
    cur = con.cursor()
    # Comando SQL para criar a tabela de linguagens de programação.
    salt = ''.join(random.choices(string.ascii_letters+string.punctuation, k=16))
    passW = hash_password(app.config['SECRET_KEY'], escape('Admin!12345'), salt)
    insert_user = f''' insert into utilizador (email, nome, password, salt) 
                       values ('admin@admin.pt', 'Administrador', '{passW}', '{salt}'); '''
    cur.execute(insert_user)
    con.commit()
    id_utilizador = cur.lastrowid
    con.close()
    return id_utilizador


#  função chamada "criar_role_super_user" que insere um registro de função de super utilizador para um utilizador específico em uma 
# tabela de uma base de dados. A função recebe um argumento "id_utilizador" que é o ID do utilizador para o qual a função de super 
# utilizador deve ser atribuída. A função estabelece uma conexão com a base de dados, cria um cursor para realizar 
# operações SQL e, em seguida, insere um novo registro na tabela "utilizador_role" 
# com o ID do utilizador e a função "Admin". Por fim, a função realiza o commit das alterações 
# na base de dados e fecha a conexão com a base de dados.
def criar_role_super_user(id_utilizador):
    con = connectionDB()
    # Criar cursor para realizar operações SQL
    cur = con.cursor()
    insert_role = f''' insert into utilizador_role (id_utilizador, funcao) 
                      values ({id_utilizador}, 'Admin'); '''
    cur.execute(insert_role)
    con.commit()
    id_utilizador = cur.lastrowid
    con.close()



# função chamada "criar_produtos" que insere informações de produtos em uma tabela de uma base de dados. A função estabelece uma 
# conexão com a base de dados, cria um cursor para realizar operações SQL, e então executa um script que insere os dados dos produtos 
# na tabela "produto". Por fim, a função realiza o commit das alterações na base de dados e fecha a conexão com a base de dados.
def criar_produtos():
    con = connectionDB()
    # Criar cursor para realizar operações SQL
    cur = con.cursor()
    script_produtos = """INSERT INTO "main"."produto" ("id", "nome", "descricao", "unidades", "preco", "imagem") 
       VALUES ('1', 'Presépio Mini Tronco ', 'Presépio realizado num tronco de madeira', '68', '15', 'images/uploads/cat-img-4.jpg');
       INSERT INTO "main"."produto" ("id", "nome", "descricao", "unidades", "preco", "imagem") 
       VALUES ('2', 'Presépio Tronco', 'Presépio realizado num tronco de madeira', '26', '20', 'images/uploads/cat-img-1.jpg');
       INSERT INTO "main"."produto" ("id", "nome", "descricao", "unidades", "preco", "imagem") 
       VALUES ('3', 'Presépio Relógio', 'Presépio realizado em um relógio', '54', '20', 'images/uploads/cat-img-2.jpg');
       INSERT INTO "main"."produto" ("id", "nome", "descricao", "unidades", "preco", "imagem") 
       VALUES ('4', 'Presépio Carro', 'Presépio construído num carro mágico', '32', '45', 'images/uploads/presepio_carro.jpg');
    """
    # Executa o script de criacao de tabelas
    cur.executescript(script_produtos)
    # Efetua o (commit) das mudanças
    con.commit()
    # Ao final, fechar a conexão com a base de dados.
    con.close()




# função em Python que tem como objetivo verificar se é possível aceder a uma base de dados. Se a base de dados não existir, 
# a função tenta criar uma nova base de dados, criar um superutilizador (com o nome de utilizador "admin@admin.pt" e a palavra-passe
# "Admin!12345") e inserir produtos na base de dados. Caso algum desses passos falhe, a função imprime uma mensagem de erro.
def verificar_db(app):  
    # Verificar se conseguimos aceder á base de dados caso contrário cria uma nova e um superuser:
    # user -> admin@admin.pt 
    # password -> Admin!12345 
    try:
        with open('db/app.db', mode="r") as db:
            print('-----------------\n\nBase de Dados OK!\n\n-----------------')
    except FileNotFoundError:
        print('-----------------\n\nA criar nova base de dados...\n\n-----------------')
        with open('db/app.db', mode="w") as db:
            print('-----------------\n\nFicheiro Criado...\n\n-----------------')
        try:
            criar_base_de_dados()
            print('-----------------\n\nTabelas criadas...\n\n-----------------')
        except:
            print('-----------------\n\nNão foi possível criar as tabelas...\n\n-----------------')
        try:
            id_utilizador = criar_super_user(app)
            criar_role_super_user(id_utilizador)
            print('-----------------\n\nUtilizador e Role criados...\n\n-----------------')
        except:
            print('-----------------\n\nNão foi possível inserir o superuser...\n\n-----------------')
        try:
            criar_produtos()
            print('-----------------\n\nProdutos criados...\n\n-----------------')
        except:
             print('-----------------\n\nNão foi possível inserir produtos...\n\n-----------------')
        
            
        