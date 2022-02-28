'use strict'

let hoy = new Date();
hoy.setDate(hoy.getDate());

$('#fecha_planilla').datetimepicker({
    locale: 'es',
    format: 'DD/MM/YYYY',
    userCurrent: true,
    date: ($("#fecha_planilla").attr("value"), 'DD/MM/YYYY'),
    minDate: hoy,
});
document.querySelector("#fecha_planilla").value = `${hoy.getDate()}/${hoy.getMonth()+1}/${hoy.getFullYear()}`;

$(function (){
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
})

'use strict'
$('#process_revalidar').on('submit', function (e) {
    e.preventDefault();
    if ($('#revalidar_planilla.disabled').length < 1) {
        $('#revalidar_planilla').addClass('disabled')
        $.confirm({
            title: 'Revalidar Planilla',
            content: `Desea revalidar la planilla con el Folio Nro <strong>${$('#revalidar_planilla').attr('planilla_anular')}</strong>?`,
            icon: 'fas fa-exclamation-triangle',
            type: 'orange',
            buttons: {
                procesar: {
                    btnClass: 'btn-blue',
                    action: function (){
                        let parameters = new FormData(document.getElementById('process_revalidar'));
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            $.alert({
                                title:'Planilla revalidada!',
                                content: `Nueva Fecha: ${data.planilla.fecha_planilla} con folio: ${data.planilla.folio}`,
                                onDestroy: function () {
                                    window.location.replace('/revalidarPlanilla')
                                }
                            });
                        }else{
                            message_error(data.error);
                            $('#revalidar_planilla').removeClass('disabled')
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        $.alert(textStatus + ': ' + errorThrown);
                        $('#revalidar_planilla').removeClass('disabled')
                    });
                }},
                cancelar: function () {
                    $('#revalidar_planilla').removeClass('disabled')
                }
            }
        })

    }
});