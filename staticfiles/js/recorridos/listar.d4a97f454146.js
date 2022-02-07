        $(function () {
            $('#listado-servicios').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'accion': 'listar'
                    },
                   dataSrc: '',
                },
                columns: [
                    {'data': 'nombre'},
                    {'data': 'valor_planilla'},
                    {'data': 'distancia_kms'},
                    {'data': 'es_vigente'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [-2],
                    'orderable': false,
                    render: function (data, type, row){
                        icono = row.es_vigente == true ? 'check' : 'ban'
                        let activo = `<i class="fas fa-${icono}"></i>`
                        return activo
                    }
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/administrarServicios/actualizar/${row.id}">
                                            <button type="button" class="btn btn-primary"><i class="far fa-edit"></i>
                                            </button>
                                        </a>`
                        return botones
                    }
                },{
                    className: "botones", "targets": [ -1, -2 ]
                },{
                    'targets': [1],
                    'orderable': false,
                    render: function (data, type, row){
                        return displayCLP(row.valor_planilla)
                        }
                    }
                ],
            });
        })