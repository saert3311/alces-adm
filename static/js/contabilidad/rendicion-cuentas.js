'use strict'
var TOTAL = 0
$(document).ready(function () {
    $("tr.item").each(function() {
      let raw = $(this).find('td.montos').html()
        TOTAL += parseInt(raw)
        $(this).find('td.montos').html(displayCLP(raw))
    });
    $('#total-ingresos').html(displayCLP(TOTAL))

    $('#arqueo :input').change(function(e){

   $('#log').prepend('<p>Form changed ' + $(e.target).attr('id') + '</p>')
});
})