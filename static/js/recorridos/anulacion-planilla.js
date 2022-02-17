'use strict'
$('#process_anulacion').on('submit', function (e) {
    e.preventDefault();
    let planilla= $('#anular_planilla').attr("planilla_anular");
    if ($('#anular_planilla.disabled').length < 1) {
        $('#anular_planilla').addClass('disabled')
        $.confirm({
            title: 'Anular Planilla',
            content: `Desea anular la planilla con el Folio Nro <strong>${planilla}</strong>?`,
            icon: 'fas fa-exclamation-triangle',
            type: 'orange',
            buttons: {
                procesar: {
                    btnClass: 'btn-blue',
                    action: function (){
                    $.ajax({
                        url: window.location.pathname,
                        type: 'POST',
                        data: {'planilla' : planilla},
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            window.location.href = '/anularPlanilla';
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
                    $('#anular_planilla').removeClass('disabled')
                }
            }
        })

    }
});