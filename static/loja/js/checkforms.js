function validateform(){
    
	 // Receber o valor das variaveis
	 var password = $("#password")[0].value
	 var password2 = $("#password2")[0].value
	 var email = $("#email")[0].value
	 // Verifica se as passwords sao iguais
	 if (password === password2){
			 // Verifica Se a password esta valida
			 if(password.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})")) 
			 { 
				 // Verifica Se o email esta valido
				 if (email.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/)){
					 $("#divdasdivs").empty()
					 return true
				 }else{         
					 // Escreve nas divs os Erros        
					 $("#divdasdivs").empty()
					 $("#divdasdivs").append('<p class="warningIcon"><b>Email Errado!</b></p>'
					 +'<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;O email tem de ser válido</b></small></p>')
					 return false
				 }       
			 }
			 else
			 {                 
				 $("#divdasdivs").empty()
				 $("#divdasdivs").append('<p style="color:red;"><b>Password Errada!</b></p>')
				 // Verifica se a password contem 1 caracter alfabetico minusculo
				 if (!password.match('(?=.*[a-z])')){
					 // Escreve nas divs os Erros   
					 $("#divdasdivs").append('<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;Pelo menos 1 caracter alfabético minúsculo</b></small></p>')
					 
				 }
				 // Verifica se a password contem 1 caracter alfabetico maiusculo
				 if (!password.match('(?=.*[A-Z])')){
					 // Escreve nas divs os Erros   
					 $("#divdasdivs").append('<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;Pelo menos 1 caracter alfabético maiúsculo</b></small></p>')   
					 
				 }
				 // Verifica se a password contem 1 caracter numerico
				 if (!password.match('(?=.*?[0-9])')){
					 // Escreve nas divs os Erros   
					 $("#divdasdivs").append('<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;Pelo menos 1 caracter numérico</b></small></p>')
				  
				 }
				 // Verifica se a password contem 1 caracter alfabetico especial
				 if (!password.match('(?=.*[$*&@#!])')){
					 // Escreve nas divs os Erros   
					 $("#divdasdivs").append('<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;Pelo menos 1 caracter especial</b></small></p>')
					 
				 }
				 
				 // Verifica se a password contem 8 caracteres no minimo
				 if (!password.match('(.{8,})')){
					 // Escreve nas divs os Erros   
					 $("#divdasdivs").append('<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;Pelo menos 8 caracters</b></small></p>')
					 
				 }
				 
				 return false
			 }
	 }else{     
		 // Escreve nas divs os Erros 
		 $("#divdasdivs").empty()
		 $("#divdasdivs").append('<p style="color:red;"><b>Password Errada!</b></p>'
		 +'<p><small><b><i class="fa-solid fa-triangle-exclamation fa-lg warningIcon"></i>&emsp;As Passwords são diferentes</b></small></p>')
		return false
	
	 }
    
  };
