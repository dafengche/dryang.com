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

  $(document).bind('station-finder-station-list', function(e, data) {
    console.log('Received event station-finder-station-list');
    var optionsAsString = '';
    $.each(data, function(k, v) {
//      console.log(v[0] + ', ' + v[1] + ', (' + v[2] + ', ' + v[3] + ')');
      optionsAsString += '<option value="' + v[0] + '">' + v[1] + '</option>';
    });
    $('#verif_stn').empty().append(optionsAsString);

    // Show a search icon
    if ($('img.verif-stn-search').length == 0) {
      $('<img class="verif-stn-search" src="' + STATIC_URL + 'common/images/search.png"/>').on('click', function() {
        $('#verif_stn_finder').stationFinder('open');
      }).appendTo($('#verif_plot_type_block'));
    }
  });

  $(document).bind('zoomable-image-selected-area', function(e, data) {
    console.log('Received event zoomable-image-selected-area');
    var x1 = data['x1'], y1 = data['y1'], x2 = data['x2'], y2 = data['y2'];
//    console.log('x1, y1, x2, y2: ' + x1 + ', ' + y1 + ', ' + x2 + ', ' + y2);
    var dataset = $('#verif_dataset').val();
    var pt = $('#verif_plot_type').val();
    if ('boe' === dataset)
      pt = 'time_series';
    var params = {
      'dataset'  : $('#verif_dataset').val(),
      'plot_type': pt
    };
    if (pt === 'time_series') {
      x1 = new Date(x1);
      x2 = new Date(x2);
      params['start_date'] = x1;
      params['end_date'] = x2;
//      console.log('Date range selected: ' + x1 + ', ' + x2);
    } else { // score_map
      params['sw_lon'] = x1;
      params['sw_lat'] = y1;
      params['ne_lon'] = x2;
      params['ne_lat'] = y2;
    }
//    console.log('x1, y1, x2, y2: ' + x1 + ', ' + y1 + ', ' + x2 + ', ' + y2);
    getPlot(params);
  });

  $('#verif_dataset').on('change', function() {
    var dataset = $(this).val();

    if (dataset === 'emep') {
      $('#verif_plot_type_block').show();
      // Station finder widget
      if ($('#verif_stn_finder').hasClass('station-finder'))
        $('#verif_stn_finder').stationFinder('option', 'dataset', dataset).stationFinder('open');
      else // New instance
        $('#verif_stn_finder').stationFinder({'dataset': dataset});
    } else {
      // Hide the search icon, station finder widget
      $('.verif-stn-search').remove();
      if ($('#verif_stn_finder').hasClass('station-finder'))
        $('#verif_stn_finder').stationFinder('close');

      if (dataset === 'gaw') {
        $('#verif_plot_type_block').show();
        getStations(dataset);
      } else {
        $('#verif_plot_type_block').hide();
      }
    }
  });
/*
  $('#verif_plot_type').on('change', function() {
    getPlot({
      'dataset'  : $('#verif_dataset').val(),
      'plot_type': $(this).val()
    });
  });
*/

  $('#verif_plot_btn').on('click', function(e) {
    e.preventDefault();

    var dataset = $('#verif_dataset').val();
    var pt = 'time_series';
    if ('boe' != dataset) {
      pt = $('#verif_plot_type').val();
    }
    getPlot({
      'dataset'  : dataset,
      'plot_type': pt
    });
  });

  $('#verif_container').zoomableImage();

  // params must contain dataset and plot_type
  function getPlot(params) {
//    console.log(params);
    var container = $('#verif_container');
    var pt = params['plot_type'];
    if (pt === 'time_series' || pt === 'score_map')
      container.zoomableImage('option', 'zoomable', true);
    else
      container.zoomableImage('option', 'zoomable', false);

    $('#verif_plot_btn').prop('disabled', true);
    $('#verif_container').zoomableImage('update', STATIC_URL + 'common/images/loading.gif');

    $.ajax({
      url: 'get-plot/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify(params),
      success: function(result) {
        if (result['error']) {
          container.zoomableImage('update', STATIC_URL + 'common/images/failed.jpg');
          return;
        }
        container.zoomableImage('update', result['url']);
        if (pt === 'time_series' || pt === 'score_map') {
          var md = result['metadata'];
          if ('time_series' === pt) { // YYYY-MM-DD -> milliseconds since 1970/01/01
            md['x_min'] = new Date(md['x_min']).getTime();
            md['x_max'] = new Date(md['x_max']).getTime();
          }
          container.zoomableImage('option', 'metadata', md);
        }
      },
      error: function(result) {
        container.zoomableImage('update', STATIC_URL + 'common/images/failed.jpg');
      },
      complete: function() {
        $('#verif_plot_btn').prop('disabled', false);
      }
    });
  }

  function getStations(dataset) {
    $('#verif_plot_btn').prop('disabled', true);
    var msg = $('#verif_msg').text('');
    $.ajax({
      url: 'get-stations/',
      type: 'post',
      dataType: 'json',
      data: JSON.stringify({
        'dataset': dataset,
        'name'   : name
      }),
      success: function(result) {
//        console.log('success');
        if (result['error']) {
//          console.log(result['error']);
          msg.text('Request failed!');
        } else {
//          console.log(result['number_of_results'] + ' record(s) retrieved');
          var optionsAsString = '';
          $.each(result['data'], function(k, v) {
            optionsAsString += '<option value="' + v[0] + '">' + v[1] + '</option>';
          });
          $('#verif_stn').empty().append(optionsAsString);
        }
      },
      complete: function() {
        $('#verif_plot_btn').prop('disabled', false);
      }
    });
  }

});
