from flask import flash
import json
from flask_paginate import Pagination, get_page_args
from flask import current_app, request, session, redirect, url_for
from markupsafe import escape
import hashlib
from functools import wraps


# função chamada "get_css_framework". Essa função tenta obter o valor da variável "bs" da URL atual. Se essa variável existir, a 
# função retorna seu valor. Caso contrário, a função retorna o valor da configuração "CSS_FRAMEWORK" na aplicação atual. Se essa 
# configuração não existir, a função retorna "bootstrap4" como valor padrão.
# A função "request" é uma variável global que representa a solicitação HTTP atual. O atributo "args" é um dicionário que contém 
# os argumentos da URL. O método "get" é usado para obter o valor de um argumento específico. Se o argumento não existir, o método retorna None.
# A função "current_app" é uma variável global que faz referência à aplicação Flask atual. Ela é usada para acessar as configurações da aplicação.
# O método "config.get" é usado para obter o valor de uma configuração específica. Se a configuração não existir, o método retorna o valor padrão especificado como segundo argumento.
def get_css_framework():
    css = request.args.get("bs")
    if css:
        return css
    return current_app.config.get("CSS_FRAMEWORK", "bootstrap4")


# função chamada "get_link_size". Essa função retorna o valor da configuração "LINK_SIZE" na aplicação atual. 
# Se essa configuração não existir, a função retorna uma string vazia.
# A função "current_app" é uma variável global que faz referência à aplicação Flask atual. Ela é usada para acessar as configurações da 
# aplicação. O método "config.get" é usado para obter o valor de uma configuração específica. Se a configuração não existir, o método retorna o 
# valor padrão especificado como segundo argumento.
def get_link_size():
    return current_app.config.get("LINK_SIZE", "")


# função chamada "get_alignment". Essa função retorna o valor da configuração "LINK_ALIGNMENT" na aplicação atual. Se essa configuração não
# existir, a função retorna uma string vazia.
# A função "current_app" é uma variável global que faz referência à aplicação Flask atual. Ela é usada para acessar as configurações da aplicação. 
# O método "config.get" é usado para obter o valor de uma configuração específica. Se a configuração não existir, o método retorna o valor padrão 
# especificado como segundo argumento.
def get_alignment():
    return current_app.config.get("LINK_ALIGNMENT", "")


# função chamada "show_single_page_or_not" que retorna o valor da configuração "SHOW_SINGLE_PAGE" da aplicação atual, ou um valor 
# padrão de "False" se essa configuração não existir. A função usa o método "get" do dicionário de configurações da aplicação atual 
# para tentar obter o valor da configuração "SHOW_SINGLE_PAGE". Se essa configuração não existir, o método "get" retorna o valor padrão 
# fornecido, que neste caso é "False".
def show_single_page_or_not():
    return current_app.config.get("SHOW_SINGLE_PAGE", False)


# função chamada "get_pagination" que cria e retorna uma instância de uma classe de paginação. A função define alguns 
# valores padrão para os argumentos de palavra-chave da classe de paginação e, em seguida, passa esses argumentos para 
# a instância da classe usando o operador "**". Os valores padrão são o nome do registro como "records" e o framework CSS 
# como o retornado pela função "get_css_framework", o tamanho do link como o retornado pela função "get_link_size", o 
# alinhamento como o retornado pela função "get_alignment" e se deve mostrar uma única página como o retornado pela função 
# "show_single_page_or_not". A função retorna a instância da classe de paginação criada.
def get_pagination(**kwargs):
    kwargs.setdefault("record_name", "records")
    return Pagination(
        css_framework=get_css_framework(),
        link_size=get_link_size(),
        alignment=get_alignment(),
        show_single_page=show_single_page_or_not(),
        **kwargs
    )

# Os wrappers são a funcionalidade disponível em Python para realizar o wrap
# uma função com outra função para estender o seu comportamento.
# nesta função em especifico criei um decorador que impossibilita o acesso o
# às rotas decoradas sem existir uma sessao ativa que e criada através do login
def login_necessario(f):
    @wraps(f)
    def funcao_decorator(*args, **kwargs):
        if not bool(session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return funcao_decorator


# função de decorador chamada "admin_necessario". A função de decorador aceita outra função como argumento e devolve uma nova 
# função que será usada para envolver a função original.
# A função "funcao_decorator" verifica se uma sessão está ativa. Se não estiver, limpa a sessão e redireciona o usuário para 
# a página de login. Se a sessão estiver ativa, verifica se o usuário tem a função de "Admin". Se não tiver, redireciona o usuário 
# para a página inicial e exibe uma mensagem de erro. Se tudo estiver correto, a função original é executada.
def admin_necessario(f):
    @wraps(f)
    def funcao_decorator(*args, **kwargs):
        if not bool(session):
            session.clear()
            flash('Efectue  o login na aplicação!', 'error') 
            return redirect(url_for('login', next=request.url))
        elif not bool(session['funcao'] == 'Admin'):
            flash('Ups.. a sua conta de utilizador não lhe permite aceder a este conteudo!', 'error')          
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return funcao_decorator

# Esta funcao cria a sessao de Utilizador como o exemplo em baixo
# <SecureCookieSession {'utilizador': 'username da bd', 'nome': 'nome da BD'}>
def criar_session(user, funcao):
    session['id'] = user[0]
    session['email'] = user[1]
    session['nome'] = user[2]
    session['funcao'] = funcao
    
    
# Obriga a sessao a tornar-se permanente podendo fechar o browser 
# e abrir novamente quando entender
def session_permanente():
    if session:
        session.permanent = True
    

# Esta funcao apaga a sessao e todos os seus cookies  
def apagar_session():
    session.clear()

# Funcao que sanitiza automaticamente o return o que significa
# que por ser tambem um decorador o fará em todas as rotas que
# possuam este decorador
def sanitizar(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return escape(f(*args, **kwargs))
    return wrapped

# Funcao que recebe a Secret key da App a password e o salt 
# e retorn a password encriptada 
# Esta geração adiciona tempo de computação que complica a quebra
# da password, em particular por brute force.
def hash_password(sec_key, password, salt):
    key_password_hash = (sec_key + password + salt).encode("utf-8").hex()
    result = hashlib.sha256(key_password_hash.encode())
    return f'pbkdf2:sha256:{result.hexdigest()}'

# Funcao que recebe a password da form introduzida pelo utilizador 
# encripta e verifica se esta igual a da base de dados e retorna
# verdadeiro ou falso mediante se estao iguais ou nao
def verificar_passord_hash(password_utilizador, password_bd, sec_key, salt):
    key_password_hash = (sec_key + password_utilizador + salt).encode("utf-8").hex()
    result = hashlib.sha256(key_password_hash.encode())
    result = f'pbkdf2:sha256:{result.hexdigest()}'
    print(result)
    print(password_bd)
    return result == password_bd


# Calcula o subtotal do Carrinho
def calcular_sub_total(preco, quantidade):
    return preco * quantidade

# Obriga a sessao a tornar-se permanente podendo fechar o browser 
# e abrir novamente quando entender
def session_permanente():
    if session:
        session.permanent = True