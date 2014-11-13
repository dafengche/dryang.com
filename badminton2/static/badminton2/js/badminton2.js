$(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      }
    }
  });

  $('#badminton2_record').on('change', function() {
    var r = $(this).val();
    var params = {'r': r, 'y': 2014};
    $.ajax({
      url: 'get-data/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify(params),
      success: function(result) {
        if (result['error']) {
//          container.zoomableImage('update', STATIC_URL + 'common/images/failed.jpg');
          console.log('ERROR!');
          return;
        }
        console.log(result);
      },
      error: function(result) {
//        container.zoomableImage('update', STATIC_URL + 'common/images/failed.jpg');
        console.log('ERROR!');
      },
      complete: function() {
//        $('#verif_plot_btn').removeAttr('disabled');
      }
    });
  });

});
