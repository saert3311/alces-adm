        $('#crear_propietario_form').on('submit', function (e) {
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
                    location.href = '/propietarios/';
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            });
        });
        $('#id_rut').rut({formatOn: 'keyup', validateOn: 'change keyup'});
        $("#id_region").on('change', function () {
            let url = $("#crear_propietario_form").attr("data-comunas-url");
            let id_region = $(this).val();
            let select_comunas = $("#id_comuna")
            let opciones = '<option value="">---------------</option>'
            $.ajax({
                url: url,
                data: {
                    'region': id_region
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')){
                    $.each(data, function(key, value){
                        opciones += `<option value="${value.id}">${value.comuna}</option>`;
                    });
                    return false
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
                select_comunas.html(opciones);
            });
        });