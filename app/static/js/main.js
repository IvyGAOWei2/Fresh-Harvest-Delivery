!function(n){"function"==typeof define&&define.amd?define(["jquery"],function(e){return n(e)}):"object"==typeof module&&"object"==typeof module.exports?exports=n(require("jquery")):n(jQuery)}(function(n){function e(n){var e=7.5625,t=2.75;return n<1/t?e*n*n:n<2/t?e*(n-=1.5/t)*n+.75:n<2.5/t?e*(n-=2.25/t)*n+.9375:e*(n-=2.625/t)*n+.984375}void 0!==n.easing&&(n.easing.jswing=n.easing.swing);var t=Math.pow,u=Math.sqrt,r=Math.sin,i=Math.cos,a=Math.PI,c=1.70158,o=1.525*c,s=2*a/3,f=2*a/4.5;n.extend(n.easing,{def:"easeOutQuad",swing:function(e){return n.easing[n.easing.def](e)},easeInQuad:function(n){return n*n},easeOutQuad:function(n){return 1-(1-n)*(1-n)},easeInOutQuad:function(n){return n<.5?2*n*n:1-t(-2*n+2,2)/2},easeInCubic:function(n){return n*n*n},easeOutCubic:function(n){return 1-t(1-n,3)},easeInOutCubic:function(n){return n<.5?4*n*n*n:1-t(-2*n+2,3)/2},easeInQuart:function(n){return n*n*n*n},easeOutQuart:function(n){return 1-t(1-n,4)},easeInOutQuart:function(n){return n<.5?8*n*n*n*n:1-t(-2*n+2,4)/2},easeInQuint:function(n){return n*n*n*n*n},easeOutQuint:function(n){return 1-t(1-n,5)},easeInOutQuint:function(n){return n<.5?16*n*n*n*n*n:1-t(-2*n+2,5)/2},easeInSine:function(n){return 1-i(n*a/2)},easeOutSine:function(n){return r(n*a/2)},easeInOutSine:function(n){return-(i(a*n)-1)/2},easeInExpo:function(n){return 0===n?0:t(2,10*n-10)},easeOutExpo:function(n){return 1===n?1:1-t(2,-10*n)},easeInOutExpo:function(n){return 0===n?0:1===n?1:n<.5?t(2,20*n-10)/2:(2-t(2,-20*n+10))/2},easeInCirc:function(n){return 1-u(1-t(n,2))},easeOutCirc:function(n){return u(1-t(n-1,2))},easeInOutCirc:function(n){return n<.5?(1-u(1-t(2*n,2)))/2:(u(1-t(-2*n+2,2))+1)/2},easeInElastic:function(n){return 0===n?0:1===n?1:-t(2,10*n-10)*r((10*n-10.75)*s)},easeOutElastic:function(n){return 0===n?0:1===n?1:t(2,-10*n)*r((10*n-.75)*s)+1},easeInOutElastic:function(n){return 0===n?0:1===n?1:n<.5?-(t(2,20*n-10)*r((20*n-11.125)*f))/2:t(2,-20*n+10)*r((20*n-11.125)*f)/2+1},easeInBack:function(n){return(c+1)*n*n*n-c*n*n},easeOutBack:function(n){return 1+(c+1)*t(n-1,3)+c*t(n-1,2)},easeInOutBack:function(n){return n<.5?t(2*n,2)*(7.189819*n-o)/2:(t(2*n-2,2)*((o+1)*(2*n-2)+o)+2)/2},easeInBounce:function(n){return 1-e(1-n)},easeOutBounce:e,easeInOutBounce:function(n){return n<.5?(1-e(1-2*n))/2:(1+e(2*n-1))/2}})});


(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        } 
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 2000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="fas fa-arrow-left"></i>',
            '<i class="fas fa-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:1
            },
            992:{
                items:2
            },
            1200:{
                items:2
            }
        }
    });


    // vegetable carousel
    $(".vegetable-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="fas fa-arrow-left"></i>',
            '<i class="fas fa-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            },
            1200:{
                items:4
            }
        }
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });



    // Product Quantity
    $('.quantity button').on('click', function() {
        var button = $(this);
        var oldValue = button.closest('.quantity').find('input').val();
        var unit = button.data('unit');
        var increment;
    
        // 根据单位确定增量
        if (unit === 'Weight_kg') {
            increment = 0.25;
        } else if (unit === 'Weight_g') {
            increment = 0.1;
        } else {
            increment = 1;
        }
    
        var newValue;
        if (button.hasClass('btn-plus')) {
            newValue = parseFloat(oldValue) + increment;
        } else {
            newValue = Math.max(increment, parseFloat(oldValue) - increment);
        }
    
        // 格式化新值
        var formattedValue = (newValue % 1 === 0) ? newValue.toFixed(0) : newValue.toFixed(2);
    
        button.closest('.quantity').find('input').val(formattedValue);
        return false;
    });

})(jQuery);


document.addEventListener('DOMContentLoaded', () => {
    // 初始化购物车计数
    updateCartCount();

    document.querySelectorAll('.btn-add-to-cart').forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // 停止事件冒泡
            event.preventDefault();  // 阻止链接的默认行为
            const productCard = button.closest('.product-detail');
            const quantity = parseFloat(productCard.querySelector('.quantity-input').value);
            // console.log(button, quantity)
            addToCart(button, quantity);
        });
    });

    function addToCart(button, quantity) {
        const id = button.dataset.id;
        const name = button.dataset.name;
        const price = parseFloat(button.dataset.price);
        const imgSrc = button.dataset.img;
        let unit = button.dataset.unit;

        let cart = JSON.parse(localStorage.getItem('cart')) || [];


        unit = (unit === 'Weight_kg') ? 'kg' : (unit === 'Weight_g') ? 'g' : unit;

        // 计算qty
        if (unit === 'kg' || unit === 'Weight_kg') {
            qty = quantity / 0.25;
        } else if (unit === 'g'|| unit === 'Weight_g') {
            qty = quantity / 10;
        } else {
            qty = quantity;
        }
        
        const existingItemIndex = cart.findIndex(item => item.id === id && item.unit === unit);
        if(existingItemIndex !== -1) {
            cart[existingItemIndex] = { ...cart[existingItemIndex], quantity, qty };
        } else {
            cart.push({ id, name, price, imgSrc, quantity, unit, qty});
        }

        localStorage.setItem('cart', JSON.stringify(cart));
        cartAnime('cartIcon');
        fetch('/cart/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cart)
        })
    }

    function cartAnime(className){
        const cartIcon = document.getElementById(className);
        const scale = 1.4;
    
        setTimeout(() => {
          cartIcon.style.transform = `scale(${scale})`;
    
          setTimeout(() => {
            cartIcon.style.transform = `scale(1)`;
            updateCartCount();
          }, 500);
        }, 500);
    }

    function updateCartCount() {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        document.getElementById('cart-count').textContent = cart.length; // 使用购物车列表长度来计数
    }

    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('cart');
    });
});


