//Archivo de js comun en toda la aplicacion

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function displayCLP(num){
    return Intl.NumberFormat('es-CL', {currency: 'CLP', style: 'currency'}).format(num)
}
function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul>';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    $.confirm({
        title: 'Error',
        icon: 'fas fa-exclamation-triangle',
        content: html,
        type: 'red',
        typeAnimated: true,
         buttons: {
             tryAgain: {
                 text: 'Ok',
                 btnClass: 'btn-red',
                 action: function () {
                 }
             },
         }
    });
}