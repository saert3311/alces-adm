let costo_bruto = $('#costo_planilla').text()
$('#costo_planilla').text(displayCLP(costo_bruto))

div_resultado = (obj) => {
    let html = '<div id="imprimir_vale_pago"><img src="/static/img/logo_alces_grises.png" class=" mx-auto d-block" style="max-height: 80px;width: auto">'
    if (typeof (obj) === 'object') {
        html+= `<div class="row mb-1 pb-1 border-bottom border-dark"><div class="col"><h4 class="text-center mb-0">VALE CONTROL</h4><p class="mb-0 text-center"><strong>Inspector:</strong> ${obj['inspector']}</p><p class="text-center mb-0">${moment().format('L')} ${moment().format('LT')}</p></div></div>`
        html+= `<div class="row"><div class="col-sm-6"><h5 class="mb-1">FOLIO</h5><p class="mb-0">${obj['nro_pago']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">PLANILLA</h5><p class="mb-0">${obj['nro_planilla']}</p></div></div>`
        html+= `<div class="row mb-0"><div class="col-sm-6"><h5 class="mb-1">BUS:</h5><p class="mb-0">${obj['bus']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">FORMA PAGO:</h5><p class="mb-0">${obj['forma_pago']}</p></div></div>`
        html+= `<div class="row mb-0 text-center"><div class="col"><h5 class="mb-1">Ruta:</h5><p class="mb-0">${obj['ruta']} - ${obj['variante']}</p></div></div>`
        html+= `<div class="row mb-4 border-bottom border-dark"><div class="col-sm-4 text-center"><h5 class="mb-1">Fecha:</h5><p class="mb-0">${obj['fecha']}</p></div>`
        html+= `<div class="col-sm-4 text-center"><h5 class="mb-1 text-center">Vuelta:</h5><p>${obj['vuelta']}</p></div>`
        html+= `<div class="col-sm-4 text-center"><h5 class="mb-1 text-center">Salida:</h5><p>${obj['hora_salida']}</p></div></div>`
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
    document.getElementById('recibo_despacho').innerHTML = html;
    printJS({
        printable: 'recibo_despacho',
        type: 'html',
        targetStyles: ['*']
    })
}

$('#generar_pago').on('submit', function (e) {
    e.preventDefault();
    if ($('#pago_footer button.disabled').length < 1) {
            $('#btn-pago').addClass('disabled')
            let parameters = new FormData(this);
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
                    resultado_pago(data.despacho)
                    $('#loader_vale_cobro').addClass('d-none')
                    $('#card_vale_pago').removeClass('d-none')
                }else{
                    message_error(data.error);
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                $.alert(textStatus + ': ' + errorThrown);
            });
         }
    });
