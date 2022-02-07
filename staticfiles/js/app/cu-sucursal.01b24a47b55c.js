        $('#crear_servicio_form').on('submit', function (e) {
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
                    location.href = '/sucursales/';
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            });
        });
