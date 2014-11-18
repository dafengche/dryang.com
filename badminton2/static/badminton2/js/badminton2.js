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
    getData(params);
  });

  // Init
  init();

  function init() {
    getData({'r': $('#badminton2_record').val(), 'y': new Date().getFullYear()});
  }

  function getData(params) {
    console.log(params);
    var msg = $('#badminton2_msg');
    var container = $('#badminton2_plot');
    var r = $('#badminton2_record').val();
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
        var data = [];
        if (r === 'g') { // Games
          $.each(result['data'], function(k, v) {
            data.push([new Date(v['date']).getTime(), v['players'].length]);
          });
//          console.log(data);
          $.plot(container,
            [{
              data  : data,
              color : '#0062E3',
              points: {fillColor: '#0062E3', show: true},
              lines : {show: true}
            }],
            {
              xaxis: {
                mode: 'time'
              },
              grid: {
                hoverable        : true,
                borderWidth      : 3,
                mouseActiveRadius: 50,
                backgroundColor  : {colors: ['#FFFFFF', '#EDF5FF']},
                axisMargin       : 20
              }
            }
          );
        } else if (r === 'p') { // Players
        } else if (r === 'c') { // Costs
        } else if (r === 'ctb') { // Contributions
        } else if (r === 'b') { // My balance
        }
      },
      error: function(result) {
//        container.zoomableImage('update', STATIC_URL + 'common/images/failed.jpg');
        console.log('ERROR!');
      },
      complete: function() {
//        $('#verif_plot_btn').removeAttr('disabled');
      }
    });
  }

});
