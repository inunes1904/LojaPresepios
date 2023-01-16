/*
 código responsável de parte da função de carrinho de compras. Ele adiciona ou remove itens de um 
 carrinho de compras quando o utilizador clica em um botão com a class "atualizar carrinho". Se o utilizador não estiver autenticado, 
 os itens são armazenados em um cookie chamado "carrinho". Caso contrário, a função "atualizarEncomenda" é chamada
  para enviar uma solicitação HTTP POST para atualizar o carrinho de compras do utilizador. Depois de processar a 
  resposta, a página é recarregada para atualizar a exibição do carrinho.
*/

var atualizarBotoes = document.getElementsByClassName('atualizar-carrinho')

for (i=0; i<atualizarBotoes.length; i++){
    atualizarBotoes[i].addEventListener('click', function(){
        var produtoId = this.dataset.produto
        var acao = this.dataset.acao
        if (utilizador === ""){
            adicionarCookieItem(produtoId, acao)
        }else{
            atualizarEncomenda(produtoId, acao)
        }
    })
}

function adicionarCookieItem(produtoId, acao){
    console.log('Utilizador não autenticado')
    if(acao == 'adicionar'){
        if (carrinho[produtoId] == undefined){
            carrinho[produtoId] = {'quantidade':1}
        }else{
            carrinho[produtoId]['quantidade'] += 1
        }    
    }
    if (acao == 'remover'){
            
        carrinho[produtoId]['quantidade'] -= 1
        if (carrinho[produtoId]['quantidade'] <= 0 ){
            delete carrinho[produtoId]
        }
    }
    console.log(acao)
    if (acao == 'apagar'){
        delete carrinho[produtoId]
    }
    document.cookie = 'carrinho=' + JSON.stringify(carrinho) + ";domain=;path=/"
    console.log(carrinho)
    location.reload()
}

function atualizarEncomenda(produtoId, acao) {
    var url = '/atualizar-item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',     
        }, 
        body:JSON.stringify({ 'produtoId': produtoId, 'acao':acao })
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        location.reload()
       
    })
    


}
