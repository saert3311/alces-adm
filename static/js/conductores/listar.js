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
                    {'data': 'nombre_completo'},
                    {'data': 'direccion'},
                    {'data': 'la_comuna'},
                    {'data': 'telefono'},
                    {'data': 'licencia'},
                    {'data': 'venc_licencia'},
                    {'data': 'la_foto'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [2, 4],
                    'orderable': false,
                },{
                    'targets': [-2],
                    'orderable': false,
                    render: function (data, type, row){
                        let link_foto = `<i class="far fa-eye foto_conductor" load_img="${row.la_foto}" load_name="${row.nombre_completo}"></i>`
                        return link_foto
                    }
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/conductores/actualizar/${row.id}">
                                            <button type="button" class="btn btn-primary"><i class="far fa-edit"></i>
                                            </button>
                                        </a>
                                        <a href="tel:${row.telefono}">
                                            <button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="top" title="Llamar ${row.nombre}"><i class="fas fa-phone-alt"></i>
                                            </button>
                                        </a>
                                        <a href="mailto:${row.email}">
                                            <button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="top" title="Email a ${row.nombre}"><i class="far fa-envelope"></i>
                                            </button>
                                        </a>`
                        return botones
                    }
                },{
                    className: "botones", "targets": [ -1, -2 ]
                }
                ],
                'initComplete': function () {
                            $('.foto_conductor').on('click', function () {
            let loc_img = $(this).attr("load_img");
            let nombre_c = $(this).attr("load_name");
            $.confirm({
                title: nombre_c,
                content: `<img class="foto_conductor" src="${loc_img}" alt="${loc_img}">`,
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
                                $('[data-toggle="tooltip"]').tooltip()
                }
            });
        })