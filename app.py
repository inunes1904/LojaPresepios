# Este código é uma aplicação web feita com o Flask, um framework de aplicações web para Python.
# A variável app é uma instância da classe Flask, que é usada para gerenciar a aplicação. A pasta
# UPLOAD_FOLDER é onde imagens serão salvas e ALLOWED_EXTENSIONS é um conjunto de strings com os 
# tipos de arquivo que são permitidos para upload.

from flask import Flask
from presepioapp import views
from database_creation.criar_db import verificar_db


app = Flask(__name__) # webserver gateway interphase (WSGI)

UPLOAD_FOLDER = 'static/images/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Em seguida, o código define várias rotas para diferentes URLs da aplicação. Por exemplo, a rota '/loja/'
# é mapeada para a função views.store quando um pedido é feito com o método HTTP 'GET' ou 'POST'. As rotas
# também podem ter parâmetros, como a rota '/artigo/detalhe/int:id/', que espera um parâmetro inteiro chamado 'id'.
# Rotas Ecommerce
app.add_url_rule(rule='/',endpoint='index', view_func=views.index, methods=['GET', 'POST'])
app.add_url_rule(rule='/loja/',endpoint='store' ,view_func=views.store, methods=['GET', 'POST'])
app.add_url_rule(rule='/artigo/detalhe/<int:id>/', endpoint='detail', view_func=views.detail, methods=['GET', 'POST'])
app.add_url_rule(rule='/iniciarsessao/', endpoint='login', view_func=views.login, methods=['GET', 'POST'])
app.add_url_rule(rule='/registarutilizador/', endpoint='register', view_func=views.register, methods=['GET', 'POST'])
app.add_url_rule(rule='/sair/', endpoint='logout', view_func=views.logout, methods=['GET', 'POST'])
app.add_url_rule(rule='/editarperfil/<int:id>/', endpoint='profile', view_func=views.profile, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/carrinho/', endpoint='cart', view_func=views.cart, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/carrinho/finalizar-compra/', endpoint='checkout', view_func=views.checkout, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/atualizar-item/', endpoint='update_item', view_func=views.update_item, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/processar-encomenda/', endpoint='process_order', view_func=views.process_order, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/quem-somos/', endpoint='who', view_func=views.who, methods=['GET'])
app.add_url_rule(rule='/perguntas-frequentes/', endpoint='faq', view_func=views.faq, methods=['GET'])

# O código também define rotas para tratar erros, como a rota '/nao-encontrado/' para a página 'page not found'. 
# Além disso, há rotas para o administrador da aplicação gerenciar produtos e vendas.
# Rotas Erros
app.add_url_rule(rule='/nao-encontrado/', endpoint='page_not_found', view_func=views.page_not_found, methods=['GET'])
app.register_error_handler(404, views.page_not_found)

# Rotas Administrador
app.add_url_rule(rule='/gestao-admin/',endpoint='admin',view_func=views.admin, methods=['GET', 'POST'])
app.add_url_rule(rule='/gestao-admin/produto/add',endpoint='add_produto',view_func=views.add_produto, methods=['GET', 'POST'])
app.add_url_rule(rule='/gestao-admin/produto/edit/<int:id>/',endpoint='edit_produto',view_func=views.edit_produto, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/gestao-admin/produto/delete/<int:id>/',endpoint='delete_produto',view_func=views.delete_produto, methods=['GET', 'POST', 'PUT'])
app.add_url_rule(rule='/gestao-vendas/',endpoint='adminsales',view_func=views.adminsales, methods=['GET', 'POST'])
app.add_url_rule(rule='/gestao-clientes/',endpoint='adminclients',view_func=views.adminclients, methods=['GET', 'POST'])

# Definicao de um Segredo da Aplicacao e uma pagina para UPLOAD
app.config['SECRET_KEY'] = 'JustAfuckingTestMotherFucker'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  


# Inicia a aplicação sem ser necessario utilizar o terminal para o efeito
# SSL_CONTEXT envia os certificados para poder utilizar HTTPS
if __name__ == "__main__":
    # Verifica se existe Base de dados
    verificar_db(app)
    app.run(debug=True, port=5002)
    
