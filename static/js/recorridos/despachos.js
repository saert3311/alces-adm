let tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);

let hoy = new Date();
hoy.setDate(hoy.getDate());

$('#fecha_despacho').datetimepicker({
    locale: 'es',
    format: 'DD/MM/YYYY',
    userCurrent: false,
    date: ($("#fecha_despacho").attr("value"), 'DD/MM/YYYY'),
    minDate: hoy,
    maxDate: tomorrow
});
$('#hora_salida').datetimepicker({
    locale: 'es',
    format: 'LT'
});
$(function (){
    $('.select2bs4').select2({
        theme: 'bootstrap4'
    })
})