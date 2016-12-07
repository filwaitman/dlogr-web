jQuery(document).ready(function($) {
    // $("#registration_submit").attr({"disabled": "disabled"});
    // $("#accept_terms").click(function(){
    //     if ($(this).is(':checked')){
    //         $("#registration_submit").removeAttr("disabled");
    //     } else {
    //         $("#registration_submit").attr({"disabled": "disabled"});
    //     }
    // });

    $("#showhidepassword").click(function(){
        var field = $(".showhidepassword_field");

        if (field.attr("type") == "text"){
            field.attr({type: "password"});
        } else {
            field.attr({type: "text"});
        }

        return false;
    });
});


