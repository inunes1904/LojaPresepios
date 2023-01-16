/*
função JavaScript que faz o processamento de uma encomenda feita por um utilizador em uma loja online. 
A função é ativada quando o utilizador submete o formulário de checkout (finalização de compra).
Primeiro, a função verifica se todos os campos do formulário foram preenchidos. Se algum campo não 
foi preenchido, ela exibe uma mensagem de erro na página. Se todos os campos foram preenchidos, a 
função esconde o botão de "continuar" e exibe o botão de "pagamento".
Em seguida, a função envia os dados do formulário e da encomenda para o backend da loja através da 
fetch API. Quando a transação é concluída com sucesso, a função exibe uma mensagem de alerta e redireciona 
o utilizador para a página inicial da loja. Além disso, ela também limpa o cookie de carrinho de compras do utilizador.
Ao final da função, há uma implementação da API do Paypal, que permite ao utilizador realizar o pagamento da encomenda 
através desta plataforma.
*/

var form = document.getElementById('myFormCheckout')

console.log(total)
// Quando submete previne o comportamento default e verifica se esta tudo ok
form.addEventListener('submit', function (e){
    $("#divdasdivs").empty()
    e.preventDefault()
    if (form.nome.value!="", form.email.value!="", form.morada.value!="", 
        form.contato.value!=""){
    // esconde o botao e mostra o botao efetuar pagamento
    document.getElementById('continuar').classList.add('hidden')
    document.getElementById('pagamento-info').classList.remove('hidden')
    }else{
        // se o formulario contêm algum campo não preenchido
        // Escreve nas divs os Erros 
        $("#divdasdivs").append('<p style="color:red;"><b>Erro no Formulário</b></p>')        
        $("#divdasdivs").append('<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;Todos os campos têm de ser preenchidos.</b></small></p>')
    }

    // Utiliza a fetch API para enviar os dados do envio para o Backend
    // E posteriormente limpa o cookie do carrinho
    function submitFormData(){
        
        console.log('Form submited')
        var envioInfoData = {
                            'Nome':null,
                            'Email':null,
                            'Contato':null,
                            'Morada':null,
                            'Morada2':null,
                            'Cidade':null,
                            'Localidade':null,
                            'CodigoPostal':null,
                            'total':null
                            }
        envioInfoData.Nome = form.nome.value
        envioInfoData.Email = form.email.value
        envioInfoData.Contato = form.contato.value
        envioInfoData.Morada = form.morada.value
        envioInfoData.Morada2 = form.morada2.value
        envioInfoData.Cidade = form.cidade.value
        envioInfoData.Localidade = form.localidade.value
        envioInfoData.CodigoPostal = form.codpostal.value
        envioInfoData.total = form.total.value

    var url = '/processar-encomenda/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',     
        }, 
        body:JSON.stringify({ 'data': envioInfoData })
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('Sucesso:', data)
        alert('Transação Concluida')

        carrinho = {}
        document.cookie = 'carrinho=' + JSON.stringify(carrinho) + ";domain=;path=/"
        window.location.href = "/"
    })

    }


// API do paypal apenas criamos duas contas sandbox para testes. 
// Render the PayPal button into #paypal-button-container
 paypal.Buttons({

    style: {
      color: 'silver',
      label: 'pay',
      size: 'responsive',
      height: 40
    },


    // Set up the transaction
    createOrder: function (data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: parseFloat(total).toFixed(2)
          }
        }]
      });
    },

    // Finalize the transaction
    onApprove: function (data, actions) {
      return actions.order.capture().then(function (orderData) {
        // Successful capture! For demo purposes:
        console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
        var transaction = orderData.purchase_units[0].payments.captures[0];
        
            submitFormData()
        // Replace the above to show a success message within this page, e.g.
        // const element = document.getElementById('paypal-button-container');
        // element.innerHTML = '';
        // element.innerHTML = '<h3>Thank you for your payment!</h3>';
        // Or go to another URL:  actions.redirect('thank_you.html');
      });
    }


  }).render('#paypal-button-container');

})

 