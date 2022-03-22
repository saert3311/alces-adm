'use strict'

let rendiciones = []

$('.validar_recepcion').on('click', function () {
    let id = $(this).prop('name')
    if ($( this ).is( ":checked" )) {
        if (!(rendiciones.includes(id))) {
            rendiciones.push(id)
            console.log(rendiciones)
        }
    }else{
        rendiciones.splice(rendiciones.indexOf(id), 1)
        console.log(rendiciones)
    }
})

$('#recibir').on('submit', function (e) {
    e.preventDefault()
        if ($('#pago_footer button.disabled').length < 1) {
        $('#btn-pago').addClass('disabled')
        $.confirm({
            title: 'Procesar Pago',
            content: `Desea realizar la recepción de los elementos marcados?`,
            type: 'blue',
            buttons: {
                procesar: {
                    btnClass: 'btn-blue',
                    action: function (){
                    let parameters = new FormData(document.getElementById('recibir'));
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
})