$(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
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

  getPlot();

  $('#verif_plot_type').on('change', function() {
    getPlot();
  });

  function getPlot() {
    var msg = $('#verif_msg').text('');
    var img = $('#verif_img').attr('src', STATIC_URL + 'verif/images/loading.gif');
    $('#verif_block_plot').show();

    $.ajax({
      url: 'get-plot/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({'plot_type': $('#verif_plot_type').val()}),
      success: function(result) {
        if (result['error']) {
//          msg.text(result['error']);
          img.attr('src', STATIC_URL + 'verif/images/failed.jpg');
          return;
        }
        img.attr('src', result['result']['url']);
      },
      error: function(result) {
//        msg.text(result['error']);
        img.attr('src', '{{ STATIC_URL }}verif/images/failed.jpg');
      }
    });
  }

});
