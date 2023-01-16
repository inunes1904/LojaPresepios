import random, sqlite3, string, os, json
from statistics import mean
from flask import redirect, render_template, request, url_for, current_app, jsonify
from crud.clientes_charts import *
from crud.encomenda_crud import *
from crud.envio_crud import *
from crud.produtos_crud import *
from crud.reviews_crud import *
from crud.sales_charts import *
from crud.utilizador_crud import *
from flask_paginate import Pagination, get_page_args
from presepioapp.utilitarios import (criar_session, get_pagination, hash_password,
                                     verificar_passord_hash, apagar_session, login_necessario,
                                     calcular_sub_total, admin_necessario, session_permanente)
from markupsafe import escape
from datetime import date, datetime


UPLOADFOLDER = 'static/images/uploads/'
UPLOADFOLDER_DB = 'images/uploads/'

#  função chamada "logout". Essa função apaga a sessão atual e redireciona o utilizador para a página inicial.
# A função "apagar_session" é outra função que deve ser definida em algum lugar do código. Ela é responsável por apagar 
# os dados da sessão atual. A função "redirect" é usada para redirecionar o utilizador para outra página da aplicação. O argumento 
# "url_for('index')" gera a URL da página inicial da aplicação.
def logout():
    apagar_session()
    return redirect(url_for('index'))


# Esta função process_order() é chamada quando um utilizador finaliza uma compra na loja online. 
# O código carrega os dados da compra enviados pelo front-end da aplicação em formato JSON e verifica 
# se o utilizador está logado ou não. Se o utilizador estiver logado, a função recupera a informação sobre a 
# encomenda atual do utilizador na base de dados e finaliza a encomenda, adicionando uma transação e criando 
# um registo de envio para a encomenda. Se o utilizador não estiver logado, a função cria uma encomenda sem 
# informação do utilizador e adiciona os produtos a ela, e também cria um registo de envio para a encomenda. 
#  Por fim, a função retorna uma mensagem de sucesso no pagamento para o front-end da aplicação.
def process_order():
    data = json.loads(request.data)
    if session:
        enc, con = get_or_create_encomenda((int(session['id'])))
        id_encomenda = enc[0][0]
        total_JS = int(data['data']['total'])
        produtos_bd, con2 = get_prods_cart(int(session['id']))    
        total = 0
        id_transacao = datetime.now().timestamp()
        for prod in produtos_bd:
            total += calcular_sub_total(prod[3], prod[1])
        if total_JS == total:
            print('Encomenda finalizada')
            finalizar_encomenda(id_encomenda,id_transacao, con2)
            criar_envio(data, int(session['id']), id_encomenda, con)

    else:
        carrinho = json.loads(request.cookies.get('carrinho'))
        data = json.loads(request.data)
        # gravar encomenda na Base de dados sem id de utilizador para
        idenc = create_encomenda_nouser()
        # gerar para cada produto no carrinho uma linha 
        for i in carrinho:
            create_enc_prod_nouser(idenc, int(i), carrinho[i]['quantidade'])
        # inserir dados no envio na bd
        criar_envio_nouser(data, idenc)
        
    return jsonify(
        pagamento='Pagamento Efetuado'
    ) 


# Esta função checkout() é chamada quando um utilizador acede a página de checkout da loja online. O código 
# verifica se o utilizador está logado ou não. Se o utilizador estiver logado, a função recupera a informação sobre 
# os produtos no carrinho de compras do utilizador na base de dados e adiciona-os em uma lista de produtos. A 
# função também recupera a informação do utilizador na base de dados. Se o utilizador não estiver logado, a função 
# recupera os produtos no carrinho de compras a partir de um cookie armazenado no navegador do utilizador e os 
# adiciona na lista de produtos. Por fim, a função renderiza a página de checkout, passando para ela a lista 
# de produtos, o total da compra, o número de itens no carrinho e informações sobre o utilizador (se estiver logado).
def checkout():
    itemsCarrinho = 0
    produtos = []
    total = 0
    utilizador = ""
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))    
        for prod in produtos_bd:
            novo_produto = {'id_produto':prod[0],
                            'quantidade':prod[1],
                            'nome':prod[2],
                            'preco':prod[3],
                            'imagem':prod[4],
                            'id_utilizador':prod[5],
                            'terminada':prod[6],
                            'id_enc':prod[7],
                            'subtotal':calcular_sub_total(prod[3], prod[1])}
            produtos.append(novo_produto)
            total += novo_produto['subtotal']
            itemsCarrinho += novo_produto['quantidade']
        
        user_query, con_2 = get_utilizador(int(session['id']))
        
        for user in user_query:
            utilizador = user
        
        con.close()
        con_2.close()

    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            itemsCarrinho += carrinho[i]['quantidade']
            prod, con = get_produto(i)
            prod = prod.fetchone()
            
            novo_produto = {
                            'id_produto':prod[0],
                            'quantidade':carrinho[i]['quantidade'],
                            'nome':prod[1],
                            'preco':prod[4],
                            'imagem':prod[5],
                            'id_enc': None,
                            'subtotal':calcular_sub_total(prod[4], carrinho[i]['quantidade'])
            }
            total += calcular_sub_total(prod[4], carrinho[i]['quantidade'])
            produtos.append(novo_produto) 
            con.close()
    return render_template('checkout.html', produtos=produtos, total=total, items=itemsCarrinho, utilizador=utilizador )


# Esta função cart() é chamada quando um utilizador acessa a página de carrinho de compras da loja online. O código 
# verifica se o utilizador está logado ou não. Se o utilizador estiver logado, a função recupera a informação sobre os produtos 
# no carrinho de compras do utilizador na base de dados e os adiciona em uma lista de produtos. Se o utilizador não estiver logado, 
# a função recupera os produtos no carrinho de compras a partir de um cookie armazenado no navegador do utilizador e os adiciona 
# na lista de produtos. Por fim, a função renderiza a página de carrinho de compras, passando para ela a lista de produtos e o total da compra.
def cart():

    produtos=[]
    total = 0
    itemsCarrinho = 0

    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))    
        
        for prod in produtos_bd:
            novo_produto = {'id_produto':prod[0],
                            'quantidade':prod[1],
                            'nome':prod[2],
                            'preco':prod[3],
                            'imagem':prod[4],
                            'id_utilizador':prod[5],
                            'terminada':prod[6],
                            'id_enc':prod[7],
                            'subtotal':calcular_sub_total(prod[3], prod[1])}
            produtos.append(novo_produto)
            total += novo_produto['subtotal']
            itemsCarrinho += novo_produto['quantidade']
        con.close()
    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            try:
                itemsCarrinho += carrinho[i]['quantidade']
                prod, con = get_produto(i)
                prod = prod.fetchone()
                
                novo_produto = {
                                'id_produto':prod[0],
                                'quantidade':carrinho[i]['quantidade'],
                                'nome':prod[1],
                                'preco':prod[4],
                                'imagem':prod[5],
                                'id_enc': None,
                                'subtotal':calcular_sub_total(prod[4], carrinho[i]['quantidade'])
                }
                total += calcular_sub_total(prod[4], carrinho[i]['quantidade'])
                produtos.append(novo_produto) 
                con.close()
            except:
                print('Algum produto Removidoda Base de dados')

    return render_template('cart.html', produtos=produtos, total=total, items=itemsCarrinho)



# Esta função update_item() é chamada quando um utilizador faz uma atualização no carrinho de compras de uma loja online, 
# como adicionar ou remover um produto. O código recupera os dados enviados pelo utilizador através da requisição HTTP, 
# que incluem o ID do produto e a ação a ser realizada (adicionar ou remover). Em seguida, a função tenta recuperar a 
# informação sobre a encomenda atual do utilizador na base de dados, criando uma nova encomenda se ela não existir. Depois, 
# a função tenta recuperar a informação sobre o produto na encomenda, criando uma nova linha para o produto na encomenda 
# se ela não existir. Em seguida, a função verifica qual ação o utilizador deseja realizar e atualiza a quantidade do produto 
# na encomenda de acordo. Se a quantidade for menor ou igual a zero ou se a ação for "apagar", o produto é removido da 
# encomenda. Por fim, a função envia uma resposta ao utilizador indicando que o item foi adicionado.
def update_item():
    data = json.loads(request.data)
    produtoId = data['produtoId']
    acao = data['acao']
    print('Id do Produto: ', produtoId + ' || Ação a realizar: ', acao)

    try:
        enc, con = get_or_create_encomenda(session['id'])
    except:
        enc, con = get_or_create_encomenda(session['id'])
   
    
    id_enc = enc[0][0]
    
    try:
        enc_prod, con_2 = get_or_create_enc_prod(id_enc=id_enc, id_prod=produtoId)
    except:
        enc_prod, con_2 = get_or_create_enc_prod(id_enc=id_enc, id_prod=produtoId)
        
    quantidade = int(enc_prod[0][1])
    id_enc_prod = int(enc_prod[0][0])
    
    if acao == 'adicionar':
        # aumentar a quantidade do produto
        quantidade = add_rem_quant_enc_prod(id_enc=id_enc, quantidade=quantidade+1, produto_id=int(produtoId))
    elif acao == 'remover':
        # aumentar a quantidade do produto
        quantidade = add_rem_quant_enc_prod(id_enc=id_enc, quantidade=quantidade-1, produto_id=int(produtoId))

    if quantidade <= 0 or acao == 'apagar':
        # Apagar o produto da encomenda
        delete_enc_prod(id_enc_prod)

    con.close()
    con_2.close()
    return jsonify(
        adicionado='Item adicionado'
    )

# Este código é uma função de login. Quando o método de request é POST, o código recebe os dados de email e password do 
# formulário de login. Em seguida, o código acede a base de dados para procurar um utilizador com o email inserido. Se 
# o utilizador não for encontrado, é exibida uma mensagem de erro. Se o utilizador for encontrado, é verificada a password. 
# Se a password estiver incorreta, é exibida uma mensagem de erro. Se a password estiver correta, é criada uma sessão para o 
# utilizador e é exibida uma mensagem de sucesso. Finalmente, o utilizador é redirecionado para a página principal.
def login():
    if request.method == 'POST':
        email_input = escape(request.form.get('email'))
        password_input = escape(request.form.get('password'))
        
        user_query, con = recebe_user_da_db(email_input)

        user = ""
        for us in user_query:
           user = us
      
        if not user:
            flash('Email nao existe na base de dados', 'error')
        elif not verificar_passord_hash(password_input, user[7], current_app.config['SECRET_KEY'], user[8]):
            flash('A password está incorreta tente novamente', 'error')
        else:
            try:
                funcao = get_user_function(user[0])
            except:
                funcao = 'Utilizador'

            criar_session(user, funcao)
            # Criar sessao permanente
            if bool(request.form.get('checkbox')):
                session_permanente()

            flash(f'Bem-Vindo {user[2].title()}, o seu login foi efetuado com sucesso', 'success')
            con.close()
            return redirect(url_for('index'))

        con.close()
    return render_template('login.html')



# Este código é uma função que processa o formulário de registo de um novo utilizador. Quando o utilizador 
# submete o formulário, os dados são lidos e validados. Em seguida, um novo utilizador é criado na base de 
# dados com o nome, o email e a password fornecidos pelo utilizador. Antes de ser adicionada à base de dados, 
# a password é criptografada usando uma chave secreta e um salt aleatório. O salt é um valor único gerado para 
# cada utilizador e é adicionado à password antes de ser criptografada. Isso ajuda a tornar a criptografia da 
# password mais segura e a proteger a password do utilizador caso a base de dados seja comprometida. Quando o 
# novo utilizador é criado com sucesso na base de dados, o utilizador é redirecionado para a página de login. 
# Se houver algum problema ao criar o novo utilizador, o utilizador permanecerá na página de registo.
def register():
    if request.method == 'POST':
        salt = ''.join(random.choices(string.ascii_letters+string.punctuation, k=16))
        novo_utilizador = {
            'nome': escape(request.form.get('nome')),
            'email': escape(request.form.get('email')),
            'password': hash_password(current_app.config['SECRET_KEY'], escape(request.form.get('password')), salt),
            'salt':salt
        }
       
        done = criar_utilizador(novo_utilizador)
        if done:
            return redirect(url_for('login'))
        
    return render_template('register.html')



# Este código define uma função 'profile' que é usada para apresentar o perfil de um utilizador. 
# A função é protegida por uma verificação de login usando o decorador '@login_necessario', o 
# que significa que só é possível aceder à página do perfil se o utilizador estiver autenticado.
# Quando a página do perfil é acessada, a função recupera os dados do utilizador a partir da base 
# de dados usando a função 'get_utilizador' e armazena-os na variável 'utilizador'. Se o método de 
# solicitação for um POST, isto significa que o utilizador está a tentar atualizar os seus dados de 
# perfil. Neste caso, a função atualiza os dados do utilizador na base de dados usando a função 
# 'update_utilizador' e redireciona o utilizador de volta para a página do perfil.
# Finalmente, a função renderiza o template 'profile.html' e passa os dados do utilizador 
# e o número de itens no carrinho de compras como argumentos para o template.
@login_necessario
def profile(id):
    
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))
        itemsCarrinho = 0
        for prod in produtos_bd:
            itemsCarrinho += prod[1]
        con.close()
    else:
        itemsCarrinho=0

    user_query, con = get_utilizador(id)
    utilizador=""
    for user in user_query:
        utilizador = user
    if request.method == 'POST':
        password = escape(request.form.get('password')) 
        if not password.startswith('pbkdf2:sha256:'):
            password = hash_password(current_app.config['SECRET_KEY'], password, utilizador[8])
        utilizador_update={
                'email':request.form.get('email'),
                'nome':request.form.get('nome'),
                'cidade':request.form.get('cidade'),
                'localidade':request.form.get('localidade'),
                'morada':request.form.get('morada'),
                'codigoPostal':request.form.get('cod-postal'),
                'password':password,
                'salt':utilizador[8],
                'contacto':request.form.get('contacto'),
                'morada2':request.form.get('morada2')}

        done = update_utilizador(utilizador_update, id)
        if done:
            return redirect(url_for('profile', id=id))

    con.close()
    return render_template('profile.html', utilizador=utilizador, items=itemsCarrinho)


# Este código é uma função que retorna a página principal do site. Primeiramente, a função verifica se o 
# utilizador está autenticado e, se estiver, conta a quantidade de itens no carrinho de compras do utilizador.
# Se o utilizador não estiver autenticado, a função tenta obter o carrinho de compras do utilizador armazenado 
# em um cookie e, em seguida, conta a quantidade de itens no carrinho. Em seguida, a função obtém os quatro 
# produtos mais populares do base de dados e os armazena em uma lista de dicionários. Por fim, a função retorna 
# o modelo de página "index.html" e passa a lista de produtos populares e a quantidade de itens no carrinho de 
# compras para o modelo como parâmetros.
def index():
    produtos_top4 = []
    itemsCarrinho = 0
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))
        itemsCarrinho = 0
        for prod in produtos_bd:
            itemsCarrinho += prod[1]
        con.close()
    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            itemsCarrinho += carrinho[i]['quantidade']

    top4_produtos, con = select_top_four()
    
    for produto in top4_produtos:
        novo_produto = {'id': produto[0],
                        'nome':produto[1],
                        'descricao':produto[2],
                        'unidades':produto[3],
                        'preco':produto[4],
                        'imagem':produto[5] }
        produtos_top4.append(novo_produto)
    con.close()
    return render_template('index.html', produtos_top4=produtos_top4,  items=itemsCarrinho)


# Este código é uma função que renderiza uma página com os produtos da loja. A página possui uma opção de paginação e filtragem de produtos.
# Primeiro, é verificado se o utilizador está logado e, se sim, a quantidade de itens no carrinho de compras é calculada. Em seguida, é criada 
# uma conexão com o base de dados e é selecionado o total de produtos existentes.
# O utilizador pode selecionar a ordenação dos produtos por preço (de maior para menor ou de menor para maior) ou por nome. A query SQL é gerada 
# de acordo com a opção selecionada pelo utilizador e é executada. Os produtos são retornados e os parâmetros de paginação são gerados. Por fim, 
# a página é renderizada com os produtos e os parâmetros de paginação.
def store():
    itemsCarrinho = 0
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))
        for prod in produtos_bd:
            itemsCarrinho += prod[1]
        con.close()
    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            itemsCarrinho += carrinho[i]['quantidade']

    con = sqlite3.connect('db/app.db')
    cur = con.cursor()
    cur.execute("select count(*) from produto")
    total = cur.fetchone()[0]

    select = request.args.get('dselect')
    page, per_page, offset = get_page_args( page_parameter="p", per_page_parameter="pp", pp=3 )

    if select == 'high-low':
        if per_page:
            sql = "select id,nome,descricao,unidades,preco,imagem from produto order by preco DESC limit {}, {}".format(
                offset, per_page
            )
        else:
            sql = "select nome,descricao,unidades,preco,imagem from produto order by preco DESC"
    elif select == 'low-high':
        if per_page:
            sql = "select id,nome,descricao,unidades,preco,imagem from produto order by preco ASC limit {}, {}".format(
                offset, per_page
            )
        else:
            sql = "select id,nome,descricao,unidades,preco,imagem from produto order by preco ASC"
    else: 
        if per_page:
            sql = "select id,nome,descricao,unidades,preco,imagem from produto order by nome limit {}, {}".format(
                offset, per_page
            )
        else:
            sql = "select id,nome,descricao,unidades,preco,imagem from produto order by nome"
    
    cur.execute(sql)
    produtos = cur.fetchall()
    pagination = get_pagination(
        p=page,
        pp=per_page,
        total=total,
        record_name="produtos",
        format_total=True,
        format_number=True,
        page_parameter="p",
        per_page_parameter="pp",
    )
    
    return render_template("store.html", produtos=produtos, pagination=pagination, items=itemsCarrinho)



# Página de detalhes de um produto da loja virtual. A função recebe o ID de um produto e faz o seguinte:
# Inicializa as variáveis itemsCarrinho, post_permitido, total_rating_stars e total_rating_half_stars com valores iniciais.
# Obtém todos os comentários (reviews) do base de dados para o produto com o ID fornecido e armazena esses comentários em 
# uma lista de dicionários chamada 'reviews'. Além disso, a função calcula a média de classificações para o produto e armazena 
# essa média nas variáveis total_rating_stars e total_rating_half_stars.
# Verifica se o utilizador está logado e, se estiver, obtém os produtos no carrinho de compras do utilizador e armazena o número de 
# itens no carrinho em itemsCarrinho. Além disso, verifica se o utilizador já deixou um comentário para o produto e, se já o fez, 
# desabilita a possibilidade de o utilizador deixar outro comentário para o mesmo produto (post_permitido é definido como False).
# Se o utilizador não estiver logado, tenta obter o carrinho de compras do utilizador a partir de um cookie e armazena o número de 
# itens no carrinho em itemsCarrinho.
def detail(id):

    itemsCarrinho = 0
    reviews_db = get_all_reviews(id)
    post_permitido = True
    total_rating_stars = 0
    total_rating_half_stars = 0

    reviews = []
    total = 0
    for review in reviews_db:
        stars = int(str(review[2]).split('.')[0])
        try:
            if int(str(review[2]).split('.')[1]) >= 5:
                half_stars = 1
        except:
            half_stars = 0
        rev = {
                'id':review[0],
                'comentario':review[1],
                'stars':stars,
                'half_stars':half_stars,
                'data': review[3],
                'nome': review[6],
                'id_utilizador':review[4]
        }
        reviews.append(rev)
        total += review[2]
    try:
        total_rating = round(total / len(reviews), 1)
        total_rating_stars = int(str(total_rating).split('.')[0])
        
        try:
            if int(str(total_rating).split('.')[1]) >= 5:
                total_rating_half_stars = 1
        except:
            total_rating_half_stars = 0
    except:
        print('Sem reviews')
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))
        itemsCarrinho = 0
        for prod in produtos_bd:
            itemsCarrinho += prod[1]
        con.close()
        for rev in reviews:
            if int(session['id']) == rev['id_utilizador']:
                post_permitido = False
    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            itemsCarrinho += carrinho[i]['quantidade']
    
    query_prod, query_top4, con = select_by_id_and_top_four(id)
    
    for prod in query_prod:
        produto = {'id': prod[0],
                   'nome':prod[1],
                   'descricao':prod[2],
                   'unidades':prod[3],
                   'preco':prod[4],
                   'imagem':prod[5] }
    lista_produtos = []
    for prod in query_top4:
        novo_produto = {'id': prod[0],
                        'nome':prod[1],
                        'descricao':prod[2],
                        'unidades':prod[3],
                        'preco':prod[4],
                        'imagem':prod[5] }
        lista_produtos.append(novo_produto)
    con.close()

    if request.method == 'POST':
        rating = round(float(request.form.get('halfstarsInput')),1)
        comentario = request.form.get('comentario')
        id_utilizador = int(session['id'])
        id_produto = int(id)
        gerar_review(rating, comentario, id_utilizador, id_produto)

        return redirect(url_for('detail', id=id_produto))
    return render_template("detail.html", post=post_permitido, reviews=reviews ,
                            produto=produto, produtos_top4=lista_produtos, 
                            items = itemsCarrinho, total_rating_stars=total_rating_stars, 
                            total_rating_half_stars=total_rating_half_stars )

# função chamada "who". Essa função é responsável por renderizar a página "who.html" e passar a quantidade de itens no carrinho 
# de compras para a página.
# A função verifica primeiro se uma sessão está ativa. Se estiver, a função obtém os produtos no carrinho de compras do utilizador 
# logado a partir do base de dados. Depois, conta a quantidade total de itens no carrinho de compras e fecha a conexão com o 
# base de dados. Se a sessão não estiver ativa, a função tenta obter os dados do carrinho de compras armazenados em um cookie. 
# Se o cookie existir, a função conta a quantidade total de itens no carrinho de compras. Finalmente, a função renderiza a página
# "who.html" e passa a quantidade de itens no carrinho de compras para a página.
def who():
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))
        itemsCarrinho = 0
        for prod in produtos_bd:
            itemsCarrinho += prod[1]
        con.close()
        
    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            itemsCarrinho += carrinho[i]['quantidade']
    return render_template("who.html", items = itemsCarrinho)


# função chamada "faq". Essa função é responsável por renderizar a página "faq.html" e passar a quantidade 
# de itens no carrinho de compras para a página.
# A função verifica primeiro se uma sessão está ativa. Se estiver, a função obtém os produtos no carrinho de 
# compras do utilizador logado a partir do base de dados. Depois, conta a quantidade total de itens no carrinho de 
# compras e fecha a conexão com o base de dados. Se a sessão não estiver ativa, a função tenta obter os dados do 
# carrinho de compras armazenados em um cookie. Se o cookie existir, a função conta a quantidade total de itens no 
# carrinho de compras. Finalmente, a função renderiza a página "faq.html" e passa a quantidade de itens no carrinho 
# de compras para a página.
def faq():
    if session:
        produtos_bd, con = get_prods_cart(int(session['id']))
        itemsCarrinho = 0
        for prod in produtos_bd:
            itemsCarrinho += prod[1]
        con.close()
        
    else:
        try:
            carrinho = json.loads(request.cookies.get('carrinho'))
        except:
            carrinho = {} 
        for i in carrinho:
            itemsCarrinho += carrinho[i]['quantidade']
    return render_template("faq.html", items = itemsCarrinho)


# função chamada "admin" que é usada para exibir a página "products.html". A função é decorada com duas 
# outras funções: "admin_necessario" e "login_necessario". Isso significa que essas funções serão 
# executadas antes da função "admin".
# A função chama a função "dicionario_produtos" que deve ser definida em algum lugar do código e deve 
# retornar uma lista de dicionários com os detalhes de todos os produtos. Depois, a função "admin" renderiza 
# a página "products.html" e passa a lista de produtos para a página.
@admin_necessario
@login_necessario
def admin():
    produtos = dicionario_produtos()
    return render_template('products.html', produtos=produtos)


# função chamada "add_produto" que é usada para adicionar um produto à base de dados. A função é decorada 
# com duas outras funções: "admin_necessario" e "login_necessario". Isso significa que essas funções serão 
# executadas antes da função "add_produto".
# A função verifica se o formulário de adição de produto foi enviado usando o método POST. Se sim, a função 
# obtém os dados do formulário e os armazena em um dicionário. Depois, a função chama a função "criar_produto" 
# passando o dicionário como argumento. Essa função deve ser definida em algum lugar do código e é responsável 
# por adicionar o produto à base de dados. Depois, a função "add_produto" redireciona o utilizador para a página 
# "admin". Se não, a função renderiza a página "add_produto.html".
@admin_necessario
@login_necessario
def add_produto():
    if request.method == 'POST':
        f = request.files['file']
        f.save(UPLOADFOLDER+f.filename)
        nome = request.form.get('nome_produto')
        descricao = request.form.get('descricao_produto')
        unidades = request.form.get('unidades_produto')
        preco = request.form.get('preco_produto')
        produto = {'nome': nome, 'descricao': descricao, 
                   'unidades': unidades, 'preco': preco,
                   'imagem': str(UPLOADFOLDER_DB+f.filename), }
        criar_produto(produto)
        return redirect(url_for('admin'))
    return render_template('add_produto.html')


# função chamada "edit_produto" que é usada para editar um produto na base de dados. A função é decorada 
# com duas outras funções: "admin_necessario" e "login_necessario". Isso significa que essas funções serão 
# executadas antes da função "edit_produto".
# A função recebe um argumento "id" que é o ID do produto a ser editado. Ela obtém os detalhes do produto 
# a partir da base de dados e os armazena em um dicionário. Depois, a função verifica se o formulário de 
# edição do produto foi enviado usando o método POST. Se sim, a função atualiza os dados do produto na base 
# de dados e redireciona o utilizador para a página "admin". Se não, a função renderiza a página "edit_produto.html" 
# e passa os detalhes do produto para a página.
@admin_necessario
@login_necessario
def edit_produto(id):
    query_produto, con = get_produto(id)
    produto = {}
    for prod in query_produto:
        produto = {'id': prod[0],
                   'nome':prod[1],
                   'descricao':prod[2],
                   'unidades':prod[3],
                   'preco':prod[4],
                   'imagem':prod[5] }
    con.close()
    if request.method == 'POST':
        try:
            f = request.files['file']
            f.save(UPLOADFOLDER+f.filename)
            imagem = UPLOADFOLDER+f.filename
        except:
            imagem = produto['imagem']
        nome = request.form.get('nome_produto')
        descricao = request.form.get('descricao_produto')
        unidades = request.form.get('unidades_produto')
        preco = request.form.get('preco_produto')
        produto_com_update = {'nome': nome, 'descricao': descricao, 
                   'unidades': unidades, 'preco': preco,
                   'imagem': imagem, }
        update_produto(id, produto_com_update)
        return redirect(url_for('admin'))

    return render_template('edit_produto.html', produto=produto)


# função chamada "adminsales" que é usada para exibir estatísticas sobre as vendas da aplicação. A função é decorada com 
# duas outras funções: "admin_necessario" e "login_necessario". Isso significa que essas funções serão executadas antes 
# da função "adminsales".
# A função obtém algumas estatísticas sobre as vendas a partir de uma base de dados, incluindo as vendas por mês, a média 
# de vendas por mês, o mês com mais vendas e os produtos mais vendidos. Depois, a função processa esses dados e os converte 
# em formato JSON. Por fim, a função renderiza a página "sales.html" e passa as estatísticas para a página.
@admin_necessario
@login_necessario
def adminsales():
   
    hoje = datetime.now().strftime('%d/%m/%Y')
    
    if request.method == 'GET' and request.args.get('anoAtual'):
        ano_atual = request.args.get('anoAtual')
    else: 
        ano_atual = str(hoje).split('/')[2]
           
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 
             'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    vendas_hoje = get_vendas_hoje(hoje)
    vendas_line = vendas_line_chart(ano_atual)
    media_mes = round(mean(vendas_line),2)
    total_vendas = sum(vendas_line)
    top = vendas_line.index(max(vendas_line))
    encomendas = encomendas_bar_chart(ano_atual)
    top_3_list = vendas_line.copy()
    top3 = []
    top3_nomes = []
    for i in range(3):
        maximo = max(top_3_list) 
        top3.append(maximo)
        best = vendas_line.index(maximo)
        top3_nomes.append(meses[best])
        top_3_list.remove(maximo)
    nomes = " ".join([nome for nome in top3_nomes])

    mais_vendidos = get_mais_vendidos()

    return render_template('sales.html', vendas_line=vendas_line,
                             media=media_mes, total=total_vendas, hoje=vendas_hoje,
                             top3=top3,top3_nomes=nomes, top_mes = meses[top], 
                             enc=encomendas, mais_vendidos=mais_vendidos)


# função chamada "adminclients" que é usada para exibir estatísticas sobre os clientes da aplicação. 
# A função é decorada com duas outras funções: "admin_necessario" e "login_necessario". Isso significa que essas 
# funções serão executadas antes da função "adminclients".
# A função obtém algumas estatísticas sobre os clientes a partir de uma base de dados, incluindo o top 3 de clientes 
# com mais gastos, as vendas por mês e a porcentagem de utilizadores e não-utilizadores. Depois, a função processa esses dados
# e os converte em formato JSON. Por fim, a função renderiza a página "clients.html" e passa as estatísticas para a página.
@admin_necessario
@login_necessario
def adminclients():
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 
             'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    top1 = get_top_clientes(1)
    top3 = get_top_clientes(3)
    top3_nomes = "/".join([ item[0] for item in top3])
    top3_gasto = [ item[4] for item in top3]
    try:
        top1 = top1[0][0]
    except:
        top1 = None
    vendas_meses, clientes = get_vendas_clientes_mes()
    

    for i in range(len(vendas_meses)):
        vendas_meses[i] = meses[vendas_meses[i]] 
    vendas_meses = "/".join([ite for ite in vendas_meses])
    
    for cliente in clientes:
        venda = [0]*12
        for i in range(len(clientes[cliente]['vendas'])):
            venda[clientes[cliente]['mes'][i]-1] = clientes[cliente]['vendas'][i]
        clientes[cliente]['vendas'] = venda
    clientes = json.dumps(clientes, indent = 4)
    perc_users, perc_naousers = users_naousers()

    return render_template('clients.html', top1 = top1, top3_gasto=top3_gasto, 
                            top3_nomes=top3_nomes, meses=vendas_meses, 
                            clientes=clientes, perc_users=perc_users, perc_naousers=perc_naousers)


# função chamada "delete_produto" que é usada para excluir um produto do base de dados. A função é decorada com duas outras 
# funções: "admin_necessario" e "login_necessario". Isso significa que essas funções serão executadas antes da função "delete_produto".
# A função "delete_produto" recebe um argumento "id" que é o ID do produto a ser excluído. Ela chama a função "del_produto" passando o 
# ID do produto como argumento. Essa função deve ser definida em algum lugar do código e é responsável por excluir o produto do base 
# de dados. Depois, a função "delete_produto" redireciona o utilizador para a página "admin".
@admin_necessario
@login_necessario
def delete_produto(id):
    del_produto(id)
    return redirect(url_for('admin'))


# função chamada "page_not_found" que é um manipulador de exceção. Essa função é 
# chamada quando uma página não é encontrada (erro 404). A função recebe um argumento "e" que é uma exceção.
# A função imprime a exceção e, em seguida, renderiza a página de erro "error_404.html". Ela também retorna o 
# código de status HTTP 404 para o navegador. O código de status 404 indica que a página solicitada não foi encontrada.
def page_not_found(e):
    print(e)
    return render_template('error_404.html'), 404