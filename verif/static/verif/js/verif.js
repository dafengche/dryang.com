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

  getPlot({
    'dataset'  : $('#verif_dataset').val(),
    'plot_type': $('#verif_plot_type').val()
  });

  $('#verif_dataset').on('change', function() {
    getPlot({
      'dataset'  : $(this).val(),
      'plot_type': $('#verif_plot_type').val()
    });
  });

  $('#verif_plot_type').on('change', function() {
    getPlot({
      'dataset'  : $('#verif_dataset').val(),
      'plot_type': $(this).val()
      
    });
  });

  function getPlot(params) {
//    console.log(params);

    var msg = $('#verif_msg').text('');
    var img = $('#verif_img').attr('src', STATIC_URL + 'verif/images/loading.gif');
    var container = $('#verif_container').unbind();
    setContainerDimension(container, img);

//    var pt = $('#verif_plot_type').val();
    var pt = params['plot_type']

    $.ajax({
      url: 'get-plot/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify(params),
      success: function(result) {
        if (result['error']) {
//          msg.text(result['error']);
          img.attr('src', STATIC_URL + 'verif/images/failed.jpg');
          setContainerDimension(container, img);
          return;
        }
        img.attr('src', result['result']['url']);
        setContainerDimension(container, img);

        if ('time_series' != pt && 'score_map' != pt) {
          return;
        }

        // Zoom
        var md = result['result']['metadata'];
        if ('time_series' == pt) { // YYYY-MM-DD -> milliseconds since 1970/01/01
          md['x_min'] = new Date(md['x_min']).getTime();
          md['x_max'] = new Date(md['x_max']).getTime();
        }

        var rect = $('<div>', {id: 'verif_rect'});
        var drag = false;
        var startX, startY;
        var x1, x2, y1, y2;

        container.on('mouseenter', function(e) {
          e.preventDefault();
          container.css('cursor', 'crosshair');
        }).on('mouseleave', function(e) {
          e.preventDefault();
          container.css('cursor', 'default');
        }).on('mousedown', function(e) {
          e.preventDefault();
          drag = true;
          startX = e.pageX, startY = e.pageY;
//          console.log('Mouse down at (' + startX + ', ' + startY + ')');
          rect.css({
            'top'   : startY + 'px',
            'left'  : startX + 'px',
            'width' : '0px',
            'height': '0px'
          });
          rect.appendTo(container);

          var offset = $(this).offset();
          var xy = getXY(startX - offset.left, startY - offset.top, md);
          x1 = xy[0], y1 = xy[1];
//          console.log('-> (' + x1 + ', ' + y1 + ')');
        }).on('mousemove', function(e) {
          e.preventDefault();
          if (drag) { // Draw a rectangle
            var endX = e.pageX, endY = e.pageY;
//            console.log('Mouse move at (' + endX + ', ' + endY + ')');
            var width = Math.abs(endX - startX);
            var height = Math.abs(endY - startY);
            var newX = (endX < startX) ? (startX - width) : startX;
            var newY = (endY < startY) ? (startY - height) : startY;
            rect.css({
              'width'           : width + 'px',
              'height'          : height + 'px',
              'top'             : newY + 'px',
              'left'            : newX + 'px',
              'background-color': '#C0C0C0',
              'zoom'            : 1,
              'filter'          : 'alpha(opacity = 50)',
              'opacity'         : 0.5
            });
          }
        }).on('mouseup', function(e) {
          e.preventDefault();
          drag = false;
          var endX = e.pageX, endY = e.pageY;
//          console.log('Mouse up at (' + endX + ', ' + endY + ')');
          rect.remove();

          var offset = $(this).offset();
          var xy = getXY(endX - offset.left, endY - offset.top, md);
          x2 = xy[0], y2 = xy[1];
//          console.log('-> (' + x2 + ', ' + y2 + ')');

          if (x1 > x2) [x1, x2] = [x2, x1];
          if (y1 > y2) [y1, y2] = [y2, y1];
          x1 = x1 < md['x_min'] ? md['x_min'] : x1;
          y1 = y1 < md['y_min'] ? md['y_min'] : y1;
          x2 = x2 > md['x_max'] ? md['x_max'] : x2;
          y2 = y2 > md['y_max'] ? md['y_max'] : y2;

          if ('time_series' == pt) {
            x1 = new Date(x1);
            x2 = new Date(x2);
            params['start_date'] = x1;
            params['end_date'] = x2;
//            console.log('Date range selected: ' + x1 + ', ' + x2);
          } else { // score_map
            params['sw_lon'] = x1;
            params['sw_lat'] = y1;
            params['ne_lon'] = x2;
            params['ne_lat'] = y2;
            console.log('Area selected: sw(' + x1 + ', ' + y1 + '), ne('
              + x2 + ', ' + y2 + ')');
          }

          // Request a updated plot
          getPlot(params);
        });
      },
      error: function(result) {
//        msg.text(result['error']);
        img.attr('src', '{{ STATIC_URL }}verif/images/failed.jpg');
        setContainerDimension(container, img);
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

  function setContainerDimension(container, img) {
    container.css({
      'width' : img.width(),
      'height': img.height()
    });
  }

});
