$('#crear_usuario_form').on('submit', function (e) {
    e.preventDefault();
    var parameters = $(this).serializeArray();
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json'
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            location.href = '/usuarios/';
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
});
$('#id_username').rut({formatOn: 'keyup', validateOn: 'change keyup'});