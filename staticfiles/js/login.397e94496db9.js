function logear() {
    $.ajax({
        url: '/login/', type: 'POST',
        data: $('#loginform').serialize(),
        cache: false,
        success: function(data) {
            if (data['msg'] == 'success') {
                location.href = "/";
            } else {
                $('#cuerpo-login').attr('style','min-height:100vh');
                Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: 'Usuario o Contraseña errada'
                })
            }
        }
    });
}