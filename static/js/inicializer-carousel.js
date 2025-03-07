$(document).ready(function(){
    $('.carousel').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        dots: true,
        arrows: true,
    });

    setTimeout(function(){
        console.log("Forçando atualização do Slick...");
        $('.carousel').slick('refresh');
    }, 1000); // Espera 1 segundo e força o Slick a reconhecer todas as imagens
});