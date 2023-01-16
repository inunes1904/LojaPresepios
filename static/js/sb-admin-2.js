// Este código é um script de JavaScript que adiciona funcionalidades ao navegador de um usuário. 
// Ele usa o framework jQuery para adicionar interações ao site como:
/*
Alternar a exibição da barra lateral do site ao clicar no botão '#sidebarToggle' ou '#sidebarToggleTop';
Fechar qualquer menu de acordion aberto quando a janela for redimensionada para abaixo de 768px;
Alternar a exibição da barra lateral quando a janela for redimensionada para abaixo de 480px;
Evitar que o conteúdo principal da página role quando a barra lateral fixa estiver sob o cursor do rato;
Exibir um botão "Voltar ao topo" quando o usuário rolar a página;
Rolar suavemente para o topo da página ao clicar no botão "Voltar ao topo".
O script começa com a instrução "use strict", que ativa o modo estrito do JavaScript e ajuda a evitar erros 
comuns de sintaxe. O script também está envolto em uma função anônima, que é chamada imediatamente após a sua 
definição e passa o objeto jQuery como argumento. Isso significa que todas as funções e variáveis ​​definidas 
no script são privadas e não afetam o escopo global do site.
*/
(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
    
    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict
