var coc_state = true;
var gswb_state = true;
var pswb_state = true;
var pswb1_state = true;
var pswb2_state = true;

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

$('#pswb').on('click', function() {
    console.log("click");
    pswb_state = !pswb_state;
    if(!pswb_state){
        $("#ps1-data").hide();
    }
    else{
        $("#ps1-data").show()
    }
});

$('#pswb1').on('click', function() {
    console.log("click");
    pswb1_state = !pswb1_state;
    if(!pswb1_state){
        $("#pswb1-data").hide();
    }
    else{
        $("#pswb1-data").show()
    }
});

$('#pswb2').on('click', function() {
    console.log("click");
    pswb2_state = !pswb2_state;
    if(!pswb2_state){
        $("#pswb2-data").hide();
    }
    else{
        $("#pswb2-data").show()
    }
});