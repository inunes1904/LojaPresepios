/*
Este código é um script JavaScript que adiciona algumas funcionalidades a uma página HTML.
Ele começa por definir um modo de "strict mode" com a declaração 'use strict';.
Em seguida, ele adiciona um event listener ao evento "DOMContentLoaded", que é disparado quando o 
DOM é carregado e totalmente construído.
Dentro da função de callback deste evento, são definidas algumas funções e iniciadas algumas 
instâncias de objetos.
A primeira função é "injectClassess", que recebe um elemento HTML como parâmetro e adiciona classes 
CSS ao elemento pai deste elemento, baseado em um atributo "data-customclass" do elemento original.
Depois disso, é selecionado um conjunto de elementos com a classe "selectpicker" e, para cada um deles, 
é criada uma nova instância do objeto Choices, que é uma biblioteca externa para criar menus dropdown 
customizáveis. A função "injectClassess" é passada como callback para o evento "callbackOnInit" desta instância.
Em seguida, é criada uma instância da biblioteca GLightbox, que é usada para criar modais lightbox na página.
Depois disso, são criadas duas instâncias da biblioteca Swiper, que é usada para criar sliders de imagens. A 
primeira instância é para um slider de thumbs (miniaturas) e a segunda instância é para um slider principal, 
que utiliza os thumbs da primeira instância como thumbs.
O código também adiciona um event listener a todos os links que possuem um href "#" e previnem que esses 
links sejam clicados, evitando assim que a página seja recarregada.
Por fim, são adicionados event listeners a botões com as classes "dec-btn" e "inc-btn", que aumentam ou 
diminuem, respectivamente, o valor de um campo de input de quantidade de produto quando são clicados.
*/


'use strict';

document.addEventListener('DOMContentLoaded', function () {
	/* ===============================================================
		CUSTOM SELECT [CHOICES.JS]
	=============================================================== */
	function injectClassess(x) {
		let pickerCustomClass = x.dataset.customclass;
		let pickerSevClasses = pickerCustomClass.split(' ');
		x.parentElement.classList.add.apply(x.parentElement.classList, pickerSevClasses);
	}

	const selectPicker = document.querySelectorAll('.selectpicker');
	if (selectPicker.length) {
		selectPicker.forEach((el) => {
			const customSelect = new Choices(el, {
				placeholder: true,
				searchEnabled: false,
				itemSelectText: '',
				callbackOnInit: () => injectClassess(el),
			});
		});
	}

	

	/* ===============================================================
		GLIGHTBOX
	=============================================================== */
	const lightbox = GLightbox({
		touchNavigation: true,
	});

	/* ===============================================================
		PRODUCT DETAIL SLIDER
	=============================================================== */
	var productSliderThumbs = new Swiper('.product-slider-thumbs', {
		direction: 'horizontal',
		slidesPerView: 5,
		spaceBetween: 10,
		breakpoints: {
			560: {
				direction: 'vertical',
				slidesPerView: 1,
				spaceBetween: 0,
			},
		},
	});

	var productsSlider = new Swiper('.product-slider', {
		slidesPerView: 1,
		spaceBetween: 0,
		thumbs: {
			swiper: productSliderThumbs,
		},
	});

	/* ===============================================================
		DISABLE UNWORKED ANCHORS
	=============================================================== */
	document.querySelectorAll('a[href="#').forEach((el) => {
		el.addEventListener('click', function (e) {
			e.preventDefault();
		});
	});

	/* ===============================================================
         PRODUCT QUNATITY
      =============================================================== */
	document.querySelectorAll('.dec-btn').forEach((el) => {
		el.addEventListener('click', () => {
			var siblings = el.parentElement.querySelector('input');
			if (parseInt(siblings.value, 10) >= 1) {
				siblings.value = parseInt(siblings.value, 10) - 1;
			}
		});
	});
	document.querySelectorAll('.inc-btn').forEach((el) => {
		el.addEventListener('click', () => {
			var siblings = el.parentElement.querySelector('input');
			siblings.value = parseInt(siblings.value, 10) + 1;
		});
	});
});



