$(document).ready(function(){
var $passform = $("#passwordForm");

if($passform.length){
    $passform.validate({
        onkeyup: false,
        onclick: false,
        onfocusout: false, 
        rules:{
            passfield1:{
                required : true,
                minlength: 8,
            },
            passfield2:{
                required : true,
                equalTo : '#passwordField'
            }
        },
        messages:{
            passfield1:{
                required :'Field is mandatory!',
                minlength: 'password has to be 8 characters or more'
            },
            passfield2:{
                required :'Field is mandatory!',
                equalTo: "fields values doesn't match"
            }
        },
        submitHandler: function(form) {  
            var password = $("#passwordField").val();
            var tok = $(".token").val();
            var uidb64 = $(".uidb64").val();
            var token = $('input[name=csrfmiddlewaretoken]').val();
        
            $.ajax({
                method: "POST",
                url: "/submit-password-form",
                data: {
                    'password':password,
                    'uidb64':uidb64,
                    'tok':tok,
                    csrfmiddlewaretoken:token
                },
                success: function (response) {
                    console.log(response);
                    var msg = alertify.success(response.status);
                    msg.delay(1.3);
                    document.location.href = '/login'          
                }
            });

            
        
        
    }
    })
        

}

});