//Archivo de js comun en toda la aplicacion

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function displayCLP(num){
    if(isNaN(num)){
        return Intl.NumberFormat('es-CL', {currency: 'CLP', style: 'currency'}).format(parseInt(num))
    }else {
        return Intl.NumberFormat('es-CL', {currency: 'CLP', style: 'currency'}).format(num)
    }
}
function displayFecha(fecha){
    fecha_obj = new Date(fecha)
    return `${fecha_obj.getDate()}/${fecha_obj.getMonth()}/${fecha_obj.getFullYear()}`
}
function message_error(obj, reload=false) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul>';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    if (reload == false) {
        $.confirm({
            title: 'Error',
            icon: 'fas fa-exclamation-triangle',
            content: html,
            type: 'red',
            typeAnimated: true,
            buttons: {
                tryAgain: {
                    text: 'Ok',
                    btnClass: 'btn-red',
                    action: function () {
                    }
                },
            }
        });
    }else{
        $.confirm({
            title: 'Error',
            icon: 'fas fa-exclamation-triangle',
            content: html,
            type: 'red',
            typeAnimated: true,
            buttons: {
                tryAgain: {
                    text: 'Ok',
                    btnClass: 'btn-red',
                    action: function () {
                    }
                },
            },
            onDestroy: function () {
                location.reload()
            }
        });
    }
}

function waitForElement(querySelector, timeout){
  return new Promise((resolve, reject)=>{
    var timer = false;
    if(document.querySelectorAll(querySelector).length) return resolve();
    const observer = new MutationObserver(()=>{
      if(document.querySelectorAll(querySelector).length){
        observer.disconnect();
        if(timer !== false) clearTimeout(timer);
        return resolve();
      }
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
    if(timeout) timer = setTimeout(()=>{
      observer.disconnect();
      reject();
    }, timeout);
  });
}

function sortObj(obj) {
  return Object.keys(obj).sort().reduce(function (result, key) {
    result[key] = obj[key];
    return result;
  }, {});
}

function reverseObj(obj) {
  return Object.keys(obj).reverse().reduce(function (result, key) {
    result[key] = obj[key];
    return result;
  }, {});
}