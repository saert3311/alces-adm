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

let div_rendicion = (obj) => {
        let html = `<div class="row mb-2 pb-2 border-bottom border-dark"><div class="col"><h4 class="text-center mb-0">RENDICION CUENTAS</h4><p class="mb-0 text-center"><strong>Inspector:</strong> ${obj['inspector']}</p><p class="text-center mb-0">${moment().format('L')} ${moment().format('LT')}</p></div></div>`
        html += `<div class="row mx-1 text-center"><div class="col-sm-6"><h5 class="mb-1">Fecha</h5><p class="mb-0">${obj['fecha']}</p></div>`
        html += `<div class="col-sm-6"><h5 class="mb-1">Folio</h5><p class="mb-0">${obj['folio']}</p></div></div>`
        html += `<div class="row mb-0 text-center"><div class="col"><h5 class="mb-1">Dinero recibido</h5><h4 class="mb-0">${displayCLP(obj['total'])}</h4></div></div>`
        html += `<div class="row mb-0 text-center"><div class="col"><h5 class="mb-1">Dinero Pendiente</h5><h4 class="mb-0">${displayCLP(obj['pendiente'])}</h4></div></div>`
        html += `<div class="row mb-0 text-center"><div class="col"><h5 class="mb-1">Arqueo Dinero</h5></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">20.000</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['20000']*20000))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">10.000</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['10000']*10000))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">5.000</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['5000']*5000))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">2.000</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['2000']*2000))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">1.000</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['1000']*1000))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">500</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['500']*500))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">100</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['100']*100))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">50</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['50']*50))}</p></div></div>`
        html += `<div class="row mx-3 text-center border"><div class="col-sm-6"><h5 class="mb-1">10</h5></div>`
        html += `<div class="col-sm-6"><p class="mb-0">${displayCLP((obj['arqueo']['10']*10))}</p></div></div>`
        html += `<div class="row mx-3 mb-0 pb-5 border-bottom border-dark"><div class="col"><h5 class="mb-1">${obj['inspector']}<br>Firma:</h5></div></div>`
        html += '</div>'
    return html
}

function resultado_rendicion(obj) {
    let html = '';
    if (typeof (obj) === 'object' && obj.hasOwnProperty('rendicion')) {
        html = div_rendicion(obj['rendicion']);
    } else {
        html = '<p>' + obj + '</p>';
    }
    $('#imprimir').append(html)
            printJS({
            printable: 'imprimir',
            type: 'html',
            targetStyles: ['*']
        })
}



$('#realizar_consignacion').on('click', function (e) {
    if (!$(this).hasClass('disabled')){
        $(this).addClass('disabled')
        $('#arqueo input').attr('readonly', 'readonly')
        $('#existe_diferencia').attr('disabled', 'disabled')
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
                            resultado_rendicion(data)
                        }else{
                            message_error(data.error, data.recargar);
                            $('#realizar_consignacion').removeClass('disabled')
                            $('#existe_diferencia').removeAttr('disabled')
                            $('#arqueo input[type=number]').removeAttr('readonly')
                            $('#arqueo input[type=checkbox]').removeAttr('readonly')
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        $.alert(textStatus + ': ' + errorThrown);
                        $('#realizar_consignacion').removeClass('disabled')
                        $('#existe_diferencia').removeAttr('disabled')
                        $('#arqueo input[type=number]').removeAttr('readonly')
                        $('#arqueo input[type=checkbox]').removeAttr('readonly')
                    });
                }},
                cancelar: function () {
                    $('#realizar_consignacion').removeClass('disabled')
                    $('#existe_diferencia').removeAttr('disabled')
                    $('#arqueo input[type=number]').removeAttr('readonly')
                    $('#arqueo input[type=checkbox]').removeAttr('readonly')
                }
            }
        })

    }
})

$('#reimprimir_rendicion').on('click', function (e) {
    printJS({
            printable: 'imprimir',
            type: 'html',
            targetStyles: ['*']
    })
})