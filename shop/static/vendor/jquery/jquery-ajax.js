//$(document).on('click', '.add-to-cart', function (e) {
//
//e.preventDefault();
//
//var goodsInCartCount = $('.cart-quantity');
//var cartCount = parseInt(goodsInCartCount.text() || 0);
//
//var product_id = $(this).data('product-id');
//
//var add_to_cart_url = $(this).attr('href');
//
//$.ajax({
//    type: 'POST',
//    url: add_to_cart_url,
//    data: {
//        product_id: product_id,
//        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
//    },
//    success: function (data) {
//        cartCount ++;
//        goodsInCartCount.text(cartCount);
//
//        var cartItemsContainer = $("#cart-items-container");
//        cartItemsContainer.html(data.cart_items_html);
//    }
//
//    error: function (data) {
//        console.log('Ошибка при отправке товара в корзину');
//    }
//
//})
//
//})
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
////    $(document).on("click", ".add-to-cart", function (e) {
////        // Блокируем его базовое действие
////        e.preventDefault();
////
////        // Берем элемент счетчика в значке корзины и берем оттуда значение
////        var goodsInCartCount = $("#goods-in-cart-count");
////        var cartCount = parseInt(goodsInCartCount.text() || 0);
////
////        // Получаем id товара из атрибута data-product-id
////        var product_id = $(this).data("product-id");
////
////        // Из атрибута href берем ссылку на контроллер django
////        var add_to_cart_url = $(this).attr("href");
////
////        // делаем post запрос через ajax не перезагружая страницу
////        $.ajax({
////            type: "POST",
////            url: add_to_cart_url,
////            data: {
////                product_id: product_id,
////                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
////            },
////            success: function (data) {
////                // Сообщение
////                successMessage.html(data.message);
////                successMessage.fadeIn(400);
////                // Через 7сек убираем сообщение
////                setTimeout(function () {
////                    successMessage.fadeOut(400);
////                }, 7000);
////
////                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
////                cartCount++;
////                goodsInCartCount.text(cartCount);
////
////                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
////                var cartItemsContainer = $("#cart-items-container");
////                cartItemsContainer.html(data.cart_items_html);
////
////            },
////
////            error: function (data) {
////                console.log("Ошибка при добавлении товара в корзину");
////            },
////        });
////    });