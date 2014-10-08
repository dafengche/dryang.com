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
    var pt = $('#verif_plot_type').val();
    $('#verif_block_plot').show();

    $.ajax({
      url: 'get-plot/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({'plot_type': pt}),
      success: function(result) {
        if (result['error']) {
//          msg.text(result['error']);
          img.attr('src', STATIC_URL + 'verif/images/failed.jpg');
          return;
        }
        img.attr('src', result['result']['url']);

        // Zoom
        var md = result['result']['metadata'];
        if ('time_series' == pt) { // YYYY-MM-DD -> milliseconds since 1970/01/01
          md['x_min'] = new Date(md['x_min']).getTime();
          md['x_max'] = new Date(md['x_max']).getTime();
        }

        var drag = false;
        var startX, startY;
        var x1, x2, y1, y2; // To be sent to the backend
        img.unbind().on('mouseenter', function(e) {
          e.preventDefault();
          img.css('cursor', 'crosshair');
        }).on('mouseleave', function(e) {
          e.preventDefault();
          img.css('cursor', 'default');
          msg.text('');
        }).on('mousemove', function(e) {
          e.preventDefault();
          // Get X and Y
          var offset = $(this).offset();
          var xy = getXY(x = e.pageX - offset.left, e.pageY - offset.top, md);
          var x = xy[0];
          var y = xy[1];
          if (x >= md['x_min'] && x <= md['x_max']
            && y >= md['y_min'] && y <= md['y_max']) {
            if ('time_series' == pt) {
              x = new Date(x);
              // jQuery dateFormat plugin or datepicker.formatDate() from the jQuery UI plugin could be used to format date
              x = x.getUTCFullYear().toString() + '-' +
                (x.getUTCMonth() + 1).toString() + '-' +
                x.getUTCDate() + ' ' +
                x.getUTCHours() + ':' +
                x.getUTCMinutes() + ':' +
                x.getUTCSeconds();
            }
            msg.text('(' + x + ', ' + y + ')');
          }
        }).on('mousedown', function(e) {
          e.preventDefault();
        }).on('mouseup', function(e) {
          e.preventDefault();
        });
      },
      error: function(result) {
//        msg.text(result['error']);
        img.attr('src', '{{ STATIC_URL }}verif/images/failed.jpg');
      }
    });
  }

  function getXY(x, y, metadata) {
    var height = metadata['height']
    var width = metadata['width']
    var xmin = metadata['x_min'];
    var xmax = metadata['x_max'];
    var ymin = metadata['y_min'];
    var ymax = metadata['y_max'];
    var subplotLeft = metadata['subplot_left'];
    var subplotRight = metadata['subplot_right'];
    var subplotBottom = metadata['subplot_bottom'];
    var subplotTop = metadata['subplot_top'];
//    console.log('height: ' + height + ', width: ' + width);
//    console.log('xmin: ' + xmin + ', xmax: ' + xmax);
//    console.log('ymin: ' + ymin + ', ymax: ' + ymax);
//    console.log('subplot: left = ' + subplotLeft + ', right = ' + subplotRight + ', bottom = ' + subplotBottom + ', top = ' + subplotTop);

//    console.log('(' + x + ', ' + y + ')');
    x = xmin + (x - width * subplotLeft) * (xmax - xmin) / (width * (subplotRight - subplotLeft));
    y = ymin + (height * (subplotTop - subplotBottom) - (y - height * (1. - subplotTop))) * (ymax - ymin) / (height * (subplotTop - subplotBottom));
//    console.log('-> (' + x + ', ' + y + ')');

    return [x, y];
  }

});
