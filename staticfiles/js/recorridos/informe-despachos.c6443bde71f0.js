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
    maxDate: tomorrow
});
document.querySelector("#id_fecha_despacho").value = `${hoy.getDate()}/${hoy.getMonth()+1}/${hoy.getFullYear()}`;

$(function (){
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
})


let cargar_despachos = (accion = 'listar_despachos', fecha = moment().format('L'), bus='', servicio='', inspector = '') => {
    $('#listado_despachos').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'accion': accion,
                        'fecha_despacho' : fecha,
                        'id_vehiculo' : bus,
                        'id_recorrido' : servicio,
                        'id_usuario' : inspector
                    },
                   dataSrc: '',
                },
                columns: [
                    {'data': 'id'},
                    {'data': 'nro_vehiculo'},
                    {'data': 'detalle'},
                    {'data': 'hora_salida_ss'},
                    {'data': 'vuelta'},
                    {'data': 'nombre_conductor'},
                    {'data': 'nombre_inspector'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    className: "text-center", "targets": ['_all']
                }
                ],
            });
}
cargar_despachos();
$('#busqueda_despachos').on('submit', function (e) {
    e.preventDefault();
    let [fecha, bus, servicio, inspector] = $('#busqueda_despachos').serializeArray()
    cargar_despachos('buscar', fecha.value, bus.value, servicio.value, inspector.value)
});