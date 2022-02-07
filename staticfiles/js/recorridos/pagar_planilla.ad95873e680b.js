let costo_bruto = $('#precio_planilla_bruto').text()
$('.costo_planilla').text(displayCLP(costo_bruto))

div_resultado = (obj) => {
    let html = '<div id="imprimir_vale_pago"><img src="/static/img/logo_alces_grises.png" class=" mx-auto d-block" style="max-height: 80px;width: auto">'
    if (typeof (obj) === 'object') {
        html+= `<div class="row mb-1 pb-1 border-bottom border-dark"><div class="col"><h4 class="text-center mb-0">VALE CONTROL</h4><p class="mb-0 text-center"><strong>Inspector:</strong> ${obj['inspector']}</p><p class="text-center mb-0">${moment().format('L')} ${moment().format('LT')}</p></div></div>`
        html+= `<div class="row"><div class="col-sm-6"><h5 class="mb-1">FOLIO</h5><p class="mb-0">${obj['folio']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">PLANILLA</h5><p class="mb-0">${obj['nro_planilla']}</p></div></div>`
        html+= `<div class="row mb-0"><div class="col-sm-6"><h5 class="mb-1">BUS:</h5><p class="mb-0">${obj['bus']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">FORMA PAGO:</h5><p class="mb-0">${obj['forma_pago']}</p></div></div>`
        html+= `<div class="row mb-0 text-center"><div class="col"><h5 class="mb-1">Detalle:</h5></div></div>`
        html+= `<div class="row mb-4 border-bottom border-dark"><div class="col-sm-6 text-center"><h5 class="mb-1">Fecha:</h5><p class="mb-0">${moment(obj['fecha']).format('L')}</p></div>`
        html+= `<div class="col-sm-6 text-center"><h5 class="mb-1 text-center">Monto:</h5><p>${displayCLP(obj['monto'])}</p></div></div>`
    }
    html += '</div>'
    return html

}
function resultado_pago(obj) {
    let html = '';
    if (typeof (obj) === 'object' && obj.hasOwnProperty('pago_planilla')) {
        html = div_resultado(obj['pago_planilla']);
    } else {
        html = '<p>' + obj + '</p>';
    }
    document.getElementById('vale_cobro').innerHTML = html;
    sessionStorage.setItem('resultado', 'Pago Procesado');
    $('#loader_vale_cobro').addClass('d-none')
    $('#card_vale_pago').removeClass('d-none')
    printJS({
        printable: 'vale_cobro',
        type: 'html',
        targetStyles: ['*']
    })
}

$('#generar_pago').on('submit', function (e) {
    e.preventDefault();
    if ($('#pago_footer button.disabled').length < 1) {
        $('#btn-pago').addClass('disabled')
        $.confirm({
            title: 'Procesar Pago',
            content: `Desea procesar planilla Nro ${$('#nro_pla').text()}, por un monto de ${$('.costo_planilla').text()}, en ${$('.pla_modo_pago option:selected').text()}?`,
            type: 'blue',
            buttons: {
                procesar: {
                    btnClass: 'btn-blue',
                    action: function (){
                    let parameters = new FormData(document.getElementById('generar_pago'));
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                        beforeSend : function () {
                            $('#loader_vale_cobro').removeClass('d-none')
                        }
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            resultado_pago(data)
                        }else{
                            message_error(data.error);
                            $('#btn-pago').removeClass('disabled')
                            $('#loader_vale_cobro').addClass('d-none')
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        $.alert(textStatus + ': ' + errorThrown);
                        $('#btn-pago').removeClass('disabled')
                        $('#loader_vale_cobro').addClass('d-none')
                    });
                }},
                cancelar: function () {
                    $('#btn-pago').removeClass('disabled')
                    $('#loader_vale_cobro').addClass('d-none')
                }
            }
        })

    }
});

$('#imprimir_vale_boton').on('click', function (e) {
    $('#momento_impresion').html(`${moment().format('L')} ${moment().format('LT')}`)
    printJS({printable: 'vale_cobro', type: 'html', targetStyles: ['*']})
    $('#momento_impresion').empty()
})

window.onafterprint = (event) => {
    if (sessionStorage.getItem("resultado")){
        toastr.success(sessionStorage.getItem("resultado"))
        sessionStorage.removeItem('resultado')
    }
}