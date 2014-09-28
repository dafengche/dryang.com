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

  $('#a').on('keyup', function() {
    var a = parseFloat($(this).val());
    var b = parseFloat($('#b').val());
    doCalc(a, b);
  });

  $('#b').on('keyup', function() {
    var a = parseFloat($('#a').val());
    var b = parseFloat($(this).val());
    doCalc(a, b);
  });

  function doCalc(a, b) {
    var r = $('#result');
    r.text();
    $.ajax({
      url: 'calc/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({'a': a, 'b': b}),
      success: function(result) {
        r.text(result['result']);
      },
      error: function(result) {
        r.text(result);
      }
    });
  };

});

