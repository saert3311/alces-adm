'use strict'

let tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);

let hoy = new Date();
hoy.setDate(hoy.getDate());

$('#fecha_planilla').datetimepicker({
    locale: 'es',
    format: 'DD/MM/YYYY',
    userCurrent: true,
    date: ($("#fecha_planilla").attr("value"), 'DD/MM/YYYY')
});
document.querySelector("#id_fecha_planilla").value = `${hoy.getDate()}/${hoy.getMonth()+1}/${hoy.getFullYear()}`;

$(function (){
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
})


let cargar = (accion = 'listar', fecha = moment().format('L'), bus='', servicio='', inspector = '') => {
    $('#listado').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'accion': accion,
                        'fecha_planilla' : fecha,
                        'id_vehiculo' : bus,
                        'id_recorrido' : servicio,
                        'id_usuario' : inspector
                    },
                   dataSrc: '',
                },
                columns: [
                    {'data': 'nro_control'},
                    {'data': 'nro_vehiculo'},
                    {'data': 'servicio_desc'},
                    {'data': 'nro_despachos'},
                    {'data': 'nombre_conductor'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    className: "text-center", "targets": ['_all']
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="${window.location.pathname}${row.id}">
                                            <button type="button" class="btn btn-info btn-sm"><i class="far fa-calendar-times"></i>
                                            </button>
                                        </a>`
                        return botones
                    },
                    'width': '10%'
                }
                ],
            });
}
cargar();
$('#busqueda').on('submit', function (e) {
    e.preventDefault();
    let [fecha, bus, servicio, inspector] = $('#busqueda').serializeArray()
    cargar('buscar', fecha.value, bus.value, servicio.value, inspector.value)
});