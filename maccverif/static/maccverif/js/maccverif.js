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

  $('#maccverif_plot_type').on('change', function() {
    alert($(this).val());
  });

  $('#maccverif_plot_btn').on('click', function(e) {
    e.preventDefault();

    var pt = $('#maccverif_plot_type').val();
    console.log('Plot type: ' + pt);

    var msg = $('#maccverif_msg').text('');
    $('#maccverif_block_plot').show();

    $.ajax({
      url: 'get-plot/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({'plot_type': pt}),
      success: function(result) {
        if (result['error']) {
          msg.text(result['error']);
          return;
        }
        var chart = $('#maccverif_chart');
        var img = $('#maccverif_chart_img');
        if (img.length == 0) {
          img = $('<img>', {id: 'maccverif_chart_img'});
          img.appendTo(chart);
        }
        img.attr('src', result['result']['url']);
      },
      error: function(result) {
        msg.text(result['error']);
      }
    });
  });

});
