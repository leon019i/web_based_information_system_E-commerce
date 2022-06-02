$(document).ready(function() {
    
    $('.increment-btn').click(function(e) {
        e.preventDefault();
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var prod_quantity = $(this).closest('.product_data').find('.prod_quantity').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value < prod_quantity) {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.decrement-btn').click(function(e) {
        e.preventDefault();
        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });
    $('.add-to-cart-btn').click(function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();    
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                 csrfmiddlewaretoken: token
            },
            success: function (response) {
                var msg = alertify.success(response.status)
                msg.delay(1.3)
            }
        });
        

    });

    $('.add-to-wishlist-btn').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();  
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                var msg = alertify.success(response.status)
                msg.delay(1.3)
            }
        });
        
    });
    $(document).on('click','.changeQuantity', function(e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();    
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                 csrfmiddlewaretoken: token
            },
            success: function (response) {
                //   $('.quantitydiv').load(location.href + " .quantitydiv");
                // location.reload()
                var msg = alertify.success(response.status)
                msg.delay(1.3)
                
            }
        });
        

    });
    $(document).on('click','.delete-cart-item', function(e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();   
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id':product_id,
                 csrfmiddlewaretoken: token
            },
            success: function (response) {
                $('.cartdata').load(location.href + " .cartdata");
                
            }
        });
        

    });
    $(document).on('click','.delete-wishlist-item', function(e) {
 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();   
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id':product_id,
                 csrfmiddlewaretoken: token
            },
            success: function (response) {
                var msg = alertify.success(response.status)
                msg.delay(1.3)
                $('.wishdata').load(location.href + " .wishdata");
                
            }
        });
        
    });


});