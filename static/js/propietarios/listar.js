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
                    'targets': [1,2,3,4],
                    'orderable': false,
                },{
                    'targets': [-1],
                    'orderable': false,
                    render: function (data, type, row){
                        let botones = `<a href="/propietarios/actualizar/${row.id}">
                                            <button type="button" class="btn btn-primary" data-toggle="tooltip" data-placement="top" title="Editar ${row.nombre}"><i class="far fa-edit"></i>
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
                    'targets': [-2],
                    'orderable': false,
                    render: function (data, type, row){
                        icono = row.activo == true ? 'check' : 'ban'
                        let activo = `<i class="fas fa-${icono}"></i>`
                        return activo
                    }
                },{
                    className: "botones", "targets": [ -1, -2 ]
                }
                ],
                'initComplete': function () {
                    $('[data-toggle="tooltip"]').tooltip()
                }
            });
        })