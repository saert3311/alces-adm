        $(function () {
            $('#listado-vehiculos').DataTable({
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
                    {'data': 'nro'},
                    {'data': 'patente'},
                    {'data': 'veh_completo'},
                    {'data': 'ano'},
                    {'data': 'ven_revision'},
                    {'data': 't_salida'},
                    {'data': 'la_foto'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [2, 5, 7],
                    'orderable': false,
                },{
                    'targets': [-2],
                    'orderable': false,
                    render: function (data, type, row){
                        let link_foto = `<i class="far fa-eye foto_vehiculo" load_img="${row.la_foto}" load_name="${row.veh_completo}"></i>`
                        return link_foto
                    }
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/buses/actualizar/${row.id}">
                                            <button type="button" class="btn btn-secondary"><i class="far fa-edit"></i>
                                            </button>
                                        </a>`
                        return botones
                    }
                },{
                    className: "botones", "targets": [ -1, -2 ]
                }
                ],

                'initComplete': function () {
                            $('.foto_vehiculo').on('click', function () {
            let loc_img = $(this).attr("load_img");
            let nombre_v = $(this).attr("load_name");
            $.confirm({
                title: nombre_v,
                content: `<img class="foto_conductor" src="${loc_img}" alt="${nombre_v}">`,
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
                }
            });
        });