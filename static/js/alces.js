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