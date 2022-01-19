'use strict'
var TOTAL_MOSTRAR = 0

function ArqueoDinero (num, bill) {
    let billetes = {
        'veintemil': 20000,
        'diezmil': 10000,
        'cincomil': 5000,
        'dosmil': 2000,
        'mil': 1000,
        'quinientos': 500,
        'cien': 100,
        'cincuenta': 50,
        'diez': 10
    }
    if (isNaN(num)) {
        return 0
    }
    return num*billetes[bill]
}

$(document).ready(function () {
    $("tr.item").each(function() {
      let raw = $(this).find('td.montos').html()
        TOTAL_MOSTRAR += parseInt(raw)
        $(this).find('td.montos').html(displayCLP(raw))
    });
    $('#total-ingresos').html(displayCLP(TOTAL_MOSTRAR))

})

$('#arqueo :input').change(function(e){
    let TOTAL = 0
    $('#arqueo :input').each(function () {
        if (Math.sign($(this).val()) == 1 || Math.sign($(this).val()) == 0 ) {
            if ($(this).hasClass('is-invalid')){
                $(this).removeClass('is-invalid')
            }
            TOTAL += ArqueoDinero($(this).val(), $(this).attr('id'))
        }else{
                $(this).addClass('is-invalid')
        }
    })
    $('#total_arqueo').text(displayCLP(TOTAL))
});