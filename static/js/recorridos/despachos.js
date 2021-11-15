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