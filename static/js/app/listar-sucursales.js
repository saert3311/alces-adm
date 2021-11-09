        $(function () {
            $('#listado-sucursales').DataTable({
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
                    {'data': 'nombre'},
                    {'data': 'direccion'},
                    {'data': 'lat_lon'},
                    {'data': 'activo'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [1, 2],
                    'orderable': false,
                },{
                    'targets': [-2],
                    'orderable': false,
                    render: function (data, type, row){
                        icono = row.activo == true ? 'check' : 'ban'
                        let activo = `<i class="fas fa-${icono}"></i>`
                        return activo
                    },
                    'width': '10%'
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/sucursales/actualizar/${row.id}">
                                            <button type="button" class="btn btn-primary btn-sm"><i class="far fa-edit"></i>
                                            </button>
                                        </a>`
                        return botones
                    },
                    'width': '10%'
                },{
                    className: "botones", "targets": [ -1, -2 ]
                }
                ]
            });
        })