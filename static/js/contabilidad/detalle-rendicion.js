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

$('#form_recibir').on('submit', function (e) {
    e.preventDefault()
        if (rendiciones.length < 1) {
            return $.alert({
                title: 'Atencion!',
                type: 'red',
                content: 'No has seleccionado ningun elemento a recibir!',
            });
        }
        $("#form_recibir input").prop("disabled", true);$(".validar_recepcion").prop("disabled", true);
        $.confirm({
            title: 'Procesar Pago',
            content: `Desea realizar la recepción de los elementos marcados?`,
            type: 'blue',
            buttons: {
                procesar: {
                    btnClass: 'btn-blue',
                    action: function (){
                    let parameters = new FormData();
                    parameters.append('marcados', rendiciones);
                    parameters.append('accion', 'recibir');
                    parameters.append('observaciones', document.getElementById('observaciones').value)
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            console.log('ok')
                        }else{
                            message_error(data.error);
                            $("#recibir input").prop("disabled", false);$(".validar_recepcion").prop("disabled", false);
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        $.alert(textStatus + ': ' + errorThrown);
                        $("#recibir input").prop("disabled", false);$(".validar_recepcion").prop("disabled", false);
                    });
                }},
                cancelar: function () {
                    $("#recibir input").prop("disabled", false);$(".validar_recepcion").prop("disabled", false);
                }
            }
        })
});