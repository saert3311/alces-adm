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
ultimos_despachos = () => {
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
                    {'data': 'nombre'},
                    {'data': 'valor_planilla'},
                    {'data': 'distancia_kms'},
                    {'data': 'es_vigente'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [-2],
                    'orderable': false,
                    render: function (data, type, row){
                        icono = row.es_vigente == true ? 'check' : 'ban'
                        let activo = `<i class="fas fa-${icono}"></i>`
                        return activo
                    }
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/administrarServicios/actualizar/${row.id}">
                                            <button type="button" class="btn btn-primary"><i class="far fa-edit"></i>
                                            </button>
                                        </a>`
                        return botones
                    }
                },{
                    className: "botones", "targets": [ -1, -2 ]
                },{
                    'targets': [1],
                    'orderable': false,
                    render: function (data, type, row){
                        return displayCLP(row.valor_planilla)
                        }
                    }
                ],
            });
}
ultimos_despachos();
function resultado_despacho(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul>';
        $.each(obj, function (key, value) {
            html += '<li>' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    $.confirm({
        title: 'Despacho generado',
        icon: 'fas fa-road',
        content: html,
        type: 'blue',
        typeAnimated: true,
        autoClose: 'close|5000',
         buttons: {
             close: {
                 text: 'Ok',
                 action: function () {
                 }
             },
         }
    });
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
            resultado_despacho(data.msg)
        }else{
            message_error(data.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        $.alert(textStatus + ': ' + errorThrown);
    });
});
