        $(function () {
            $('#planillas_pagar').DataTable({
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
                    {'data': 'fecha_simple'},
                    {'data': 'inspector'},
                    {'data': 'entregado'},
                    {'data': 'pendiente'},
                    {'data': 'id'}
                ],
                language: {
                    url: '/static/plugins/datatables/es.json'
                },
                'columnDefs': [{
                    'targets': [-2, -3],
                    'orderable': false,
                    render: function (data, type, row){
                        return displayCLP(row.valor)
                    }
                },{
                    'targets': [0],
                    render: function (data, type, row){
                        fecha = new Date(row.fecha_planilla)
                        return fecha.toLocaleDateString('es-cl')
                    }
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/pagoPlanilla/pagar/${row.id}">
                                            <button type="button" class="btn btn-info btn-sm"><i class="fas fa-money-bill-wave"></i>
                                            </button>
                                        </a>`
                        return botones
                    },
                    'width': '10%'
                },{
                    className: "botones", "targets": [0,1,2,3,4,5]
                }
                ]
            });
        })