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
    if (!$.isNumeric($(this).val())) {
      alert('You must enter a number!');
      $(this).val('0');
      $(this).focus();
    } else {
      compute(parseFloat($(this).val()), parseFloat($('#b').val()), $('#o').val());
    }
  });

  $('#b').on('keyup', function() {
    if (!$.isNumeric($(this).val())) {
      alert('You must enter a number!');
      $(this).val('0');
      $(this).focus();
    } else {
      compute(parseFloat($('#a').val()), parseFloat($(this).val()), $('#o').val());
    }
  });

  $('#o').on('change', function() {
    compute(parseFloat($('#a').val()), parseFloat($('#b').val()), $(this).val());
  });

  function compute(a, b, o) {
    var r = $('#result');
    r.text('...');
    $.ajax({
      url: 'calc/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({'a': a, 'b': b, 'o': o}),
      success: function(result) {
        var r2 = result['result'];
        if (r2 || r2 == +0) r.text(r2);
        else if (result['error']) r.text(result['error']);
        else r.text('UNKNOWN RESULT');
      },
      error: function(result) {
        r.text(result);
      }
    });
  };

});

