'use strict'
var TOTAL_MOSTRAR = 0
var TOTAL_ARQUEO = 0
var EXISTE_DIFERENCIA = false


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
    $('#monto_diferencia').val(displayCLP(TOTAL_MOSTRAR))

})

$('#arqueo :input[type=number]').change(function(e){
    TOTAL_ARQUEO = 0
    $('#arqueo :input[type=number]').each(function () {
        if (Math.sign($(this).val()) == 1 || Math.sign($(this).val()) == 0 ) {
            if ($(this).hasClass('is-invalid')){
                $(this).removeClass('is-invalid')
            }
            TOTAL_ARQUEO += ArqueoDinero($(this).val(), $(this).attr('id'))
        }else{
                $(this).addClass('is-invalid')
        }
    })
    $('#total_arqueo').html(displayCLP(TOTAL_ARQUEO))
    $('#monto_diferencia_show').val(displayCLP(TOTAL_MOSTRAR-TOTAL_ARQUEO))
    $('#monto_diferencia').val((TOTAL_MOSTRAR-TOTAL_ARQUEO))
    if (TOTAL_ARQUEO === TOTAL_MOSTRAR && EXISTE_DIFERENCIA == false)  {
        if ($('#realizar_consignacion').hasClass('disabled')) {
            $('#realizar_consignacion').removeClass('disabled')
        }
    }else {
        if (!$('#realizar_consignacion').hasClass('disabled')) {
            $('#realizar_consignacion').addClass('disabled')
        }
    }
});

$('#arqueo #existe_diferencia').change(function (e){
    if ($(this).is(':checked')) {
       EXISTE_DIFERENCIA = true
        $('#realizar_consignacion').removeClass('disabled btn-success').addClass('btn-warning')
    }else {
        EXISTE_DIFERENCIA = false
        $('#realizar_consignacion').removeClass('btn-warning').addClass('btn-success')
        if (TOTAL_ARQUEO !== TOTAL_MOSTRAR) {
            $('#realizar_consignacion').addClass('disabled')
        }
    }
})

$('#realizar_consignacion').on('click', function (e) {
    if (!$(this).hasClass('disabled')){
        $(this).addClass('disabled')
        $('#arqueo input').attr('readonly', 'readonly')
        $.confirm({
            title: 'Procesar',
            content: `Monto: ${$('#total_arqueo').text()}, Diferencia: ${$('#monto_diferencia_show').val()}`,
            type: 'blue',
            buttons: {
                procesar: {
                    btnClass: 'btn-blue',
                    action: function (){
                    let parameters = new FormData(document.getElementById('arqueo'));
                    parameters.set('accion', 'procesar'); parameters.set('total_arqueo', TOTAL_ARQUEO)
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            console.log(data)
                        }else{
                            message_error(data.error, data.recargar);
                            $('#realizar_consignacion').removeClass('disabled')
                            $('#arqueo input[type=number]').removeAttr('readonly')
                            $('#arqueo input[type=checkbox]').removeAttr('readonly')
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        $.alert(textStatus + ': ' + errorThrown);
                        $('#realizar_consignacion').removeClass('disabled')
                        $('#arqueo input[type=number]').removeAttr('readonly')
                        $('#arqueo input[type=checkbox]').removeAttr('readonly')
                    });
                }},
                cancelar: function () {
                    $('#realizar_consignacion').removeClass('disabled')
                    $('#arqueo input[type=number]').removeAttr('readonly')
                    $('#arqueo input[type=checkbox]').removeAttr('readonly')
                }
            }
        })

    }
})