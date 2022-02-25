'use strict'

let tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);

let hoy = new Date();
hoy.setDate(hoy.getDate());

$('#fecha_despacho').datetimepicker({
    locale: 'es',
    format: 'DD/MM/YYYY',
    userCurrent: true,
    date: ($("#fecha_despacho").attr("value"), 'DD/MM/YYYY'),
    minDate: hoy,
    maxDate: tomorrow
});
document.querySelector("#id_fecha_despacho").value = `${hoy.getDate()}/${hoy.getMonth()+1}/${hoy.getFullYear()}`;
$('#hora_salida').datetimepicker({
    locale: 'es',
    format: 'LT'
});
$(function (){
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
})

let div_despacho = (obj) => {
    let html = '<div id="imprimir_despacho"><img src="/static/img/logo_alces_grises.png" class=" mx-auto d-block" style="max-height: 80px;width: auto">'
    if (typeof (obj) === 'object') {
        html+= `<div class="row mb-1 pb-1 border-bottom border-dark"><div class="col"><h4 class="text-center mb-0">PLANILLA DE RUTA</h4><p class="mb-0 text-center"><strong>Inspector:</strong> ${obj['inspector']}</p><p class="text-center mb-0">${moment().format('L')} ${moment().format('LT')}</p></div></div>`
        html+= `<div class="row"><div class="col-sm-6"><h5 class="mb-1">Despacho</h5><p class="mb-0">${obj['id']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">Planilla</h5><p class="mb-0">${obj['planilla']}</p></div></div>`
        html+= `<div class="row mb-0"><div class="col-sm-6"><h5 class="mb-1">Bus:</h5><p class="mb-0">${obj['bus']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">Patente:</h5><p class="mb-0">${obj['patente']}</p></div></div>`
        html+= `<div class="row mb-0"><div class="col-sm-6"><h5 class="mb-1">Conductor:</h5><p class="mb-0">${obj['conductor']}</p></div>`
        html+= `<div class="col-sm-6"><h5 class="mb-1">RUT:</h5><p class="mb-0">${obj['rut_conductor']}</p></div></div>`
        if (obj['rut_auxiliar'] != undefined) {
            html += `<div class="row mb-0"><div class="col-sm-6"><h5 class="mb-1" >Auxiliar:</h5><p class="mb-0">${obj['auxiliar']}</p></div>`
            html += `<div class="col-sm-6"><h5 class="mb-1">RUT:</h5><p class="mb-0">${obj['rut_auxiliar']}</p></div></div>`
        }
        html+= `<div class="row mb-0 text-center"><div class="col"><h5 class="mb-1">Ruta:</h5><p class="mb-0">${obj['ruta']} - ${obj['variante']}</p></div></div>`
        html+= `<div class="row mb-4 border-bottom border-dark"><div class="col-sm-5 text-center"><h5 class="mb-1">Fecha:</h5><p class="mb-0">${moment(obj['fecha']).format('L')}</p></div>`
        html+= `<div class="col-sm-3 text-center"><h5 class="mb-1 text-center">Vuelta:</h5><p>${obj['vuelta']}</p></div>`
        html+= `<div class="col-sm-4 text-center"><h5 class="mb-1 text-center">Salida:</h5><p>${obj['hora_salida']}</p></div></div>`
    }
    html += '</div>'
    return html

}
let ultimos_despachos = () => {
     $('#ultimos_despachos').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                "ordering": false,
                "info":     false,
                "paging":   false,
                "searching": false,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'accion': 'ultimos_despachos'
                    },
                   dataSrc: '',
                },
                columns: [
                    {'data': 'hora_salida_ss'},
                    {'data': 'nro_vehiculo'},
                    {'data': 'recorrido_despacho'},
                    {'data': 'la_planilla'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `${row.la_planilla}<span class="float-right badge bg-info item_planilla" planilla="${row.id}" accion="buscar_despacho"><i class="fas fa-print"></i></span>
                                                        <span class="float-right badge bg-danger item_planilla mr-2" planilla="${row.id}" accion="anular_despacho"><i class="far fa-trash-alt"></i></span>`
                        return botones
                    }
                },{
                    className: "text-center", "targets": [ 0, 1, 2, 3]
                }
                ],
                'initComplete': function () {
                    $('.item_planilla').on('click', function () {
                    let pla_buscar = $(this).attr("planilla");
                    let accion = $(this).attr("accion");
                        $.ajax({
                            url: window.location.pathname,
                            type: 'POST',
                            data: {
                                accion : accion,
                                despacho : pla_buscar
                            },
                        }).done(function (data) {
                            if (!data.hasOwnProperty('error')) {
                                resultado_despacho(data)
                            }else{
                                message_error(data.error);
                            }
                        }).fail(function (jqXHR, textStatus, errorThrown) {
                            $.alert(textStatus + ': ' + errorThrown);
                        }).always(function (){
                            ultimos_despachos();
                        });
                    });
                }
            });
}
ultimos_despachos();
function resultado_despacho(obj) {
    let html = '';
    if (typeof (obj) === 'object' && obj.hasOwnProperty('despacho')) {
        html = div_despacho(obj['despacho']);
    } else {
        html = '<p>' + obj + '</p>';
    }
    document.getElementById('recibo_despacho').innerHTML = html;
    $('#modal_resultado').modal('show')
    printJS({
        printable: 'recibo_despacho',
        type: 'html',
        targetStyles: ['*']
    })
}
$('#generar_despacho').on('submit', function (e) {
    e.preventDefault();
    let parameters = new FormData(this);
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            resultado_despacho(data)
            $('#generar_despacho .select2bs4').val(null).trigger('change')
        }else{
            message_error(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        $.alert(textStatus + ': ' + errorThrown);
    }).always(function (){
        ultimos_despachos();
    });
});

$('#modal_resultado').on('hidden.bs.modal', function (event) {
    document.getElementById('recibo_despacho').innerHTML = "";
})
