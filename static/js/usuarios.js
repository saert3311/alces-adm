$(function (){
    $('#listado-usuarios').DataTable({
        language : {
            url : '/static/plugins/datatables/es.json'
        },
     'columnDefs': [ {
        'targets': [5,6],
        'orderable': false,
     }]
    });
})
