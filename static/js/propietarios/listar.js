        $(function () {
            $('#listado-propietarios').DataTable({
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
                    {'data': 'activo'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [2, 4],
                    'orderable': false,
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/propietarios/actualizar/${row.id}">
                                            <button type="button" class="btn btn-secondary"><i class="far fa-edit"></i>
                                            </button>
                                        </a>`
                        return botones
                    }
                },{
                    className: "botones", "targets": [ -1, -2 ]
                }
                ],
            });
        })