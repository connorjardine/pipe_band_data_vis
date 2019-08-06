var coc_state = true;
var gswb_state = true;

$('#coc').on('click', function() {
    coc_state = !coc_state;
    if(!coc_state){
        $("#coc-data").hide();
    }
    else{
        $("#coc-data").show()
    }

});

$('#gswb').on('click', function() {
    gswb_state = !gswb_state;
    if(!gswb_state){
        $("#gswb-data").hide();
    }
    else{
        $("#gswb-data").show()
    }

});