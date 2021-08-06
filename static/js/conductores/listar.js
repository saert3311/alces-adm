        $(function () {
            $('#listado-conductores').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'accion': 'buscardata'
                    },
                   dataSrc: '',
                },
                columns: [
                    {'data': 'rut'},
                    {'data': 'nombreCompleto'},
                    {'data': 'direccion'},
                    {'data': 'comuna_text'},
                    {'data': 'telefono'},
                    {'data': 'licencia'},
                    {'data': 'venc_licencia'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [2, 4, 7, 8],
                    'orderable': false,
                }]
            });
        })
        $('.foto_conductor').on('click', function () {
            var loc_img = $(this).attr("load_img");
            $.confirm({
                title: 'Fotografia',
                content: '<img class="foto_conductor" src="' + loc_img + '" alt="">',
                animation: 'top',
                animationClose: 'top',
                buttons: {
                    okay: {
                        text: 'Ok',
                        btnClass: 'btn-blue'
                    }
                }
            });
        });