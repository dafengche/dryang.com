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
    var title = $('#badminton2_title').html('<h3>' + params['y'] + '</h3>');
    var msg = $('#badminton2_msg').html('');
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
        container.unbind();
        if (r === 'g') { // Games
          var data = [];
          var totalPlayerCount = 0;
          $.each(result['data'], function(k, v) {
            data.push([new Date(v['date']).getTime(), v['players'].length]);
            totalPlayerCount += v['players'].length;
          });
//          console.log(data);
          msg.html('Game(s) played: ' + data.length
            + ', Player count: ' + totalPlayerCount
            + ', ' + (totalPlayerCount / data.length).toFixed(2)
            + ' players/game');

          var dataset = [{
            data  : data,
            color : '#0062E3',
            points: {fillColor: '#0062E3', show: true},
            lines : {show: true}
          }];
          var options = {
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
          };
          $.plot(container, dataset, options);
          container.useTooltip(r);
        } else if (r === 'p') { // Players
          var data = [], ticks = [];
          var idx = 0;
          $.each(result['data']['player_records'], function(k, v) {
            data.push([idx, v['game_dates'].length]);
            ticks.push([idx, v['first_name']]);
            idx++;
          });
          // TODO: Sort by first_name
//          console.log(data);
//          console.log(ticks);
          var dataset = [{data: data}];
          var options = {
            series: {
              bars: {
                show: true
              }
            },
            bars: {
              align: "center",
              barWidth: 0.5
            },
            xaxis: {
              ticks: ticks
            },
            grid: {
              hoverable: true,
              borderWidth: 2
            }
          };
          $.plot(container, dataset, options);
          container.useTooltip(r);
        } else if (r === 'c' || r === 'ctb') { // Costs or contributions
          var data = {}
          $.each(result['data'], function(k, v) {
            var costs = data[v['type']['name']];
            if (costs === undefined)
              data[v['type']['name']] = v['amount'];
            else
              data[v['type']['name']] += v['amount'];
          });
//          console.log(data);
          var dataset = [];
          $.each(data, function(k, v) {
            dataset.push({
              label: k,
              data : v
            });
          });
//          console.log(dataset);
          var options = {
            series: {
              pie: {
                show: true,
                label: {
                  show: true,
                  radius: 0.8,
                  formatter: pieLabelFormatter,
                  background: {
                    opacity: 0.8,
                    color  : '#000'
                  }
                }
              }
            },
            grid: {
              hoverable: true,
              clickable: true,
              borderWidth: 2
            },
            legend: {
              show: false
            }
          };
          $.plot(container, dataset, options);
//          container.useDlg(r);
        } else if (r === 'b') { // My balance
          var data = [];
          $.each(result['data']['game_dates'], function(k, v) {
            data.push([new Date(v).getTime(), 1]);
          });
//          console.log(data);
          var costPerPlay = result['data']['cost_per_play'];
          var contrib = result['data']['contrib'];
          var bal = contrib - costPerPlay * data.length;
          msg.html('Game(s) I played: ' + data.length
            + ', cost per play: £' + costPerPlay.toFixed(2)
            + '<br/>My contribution: £' + contrib.toFixed(2)
            + ', my balance: '
            + (bal < 0.
              ? '<font color="red">£' + bal.toFixed(2) + '</font>'
              : '£' + bal.toFixed(2)));

          var dataset = [{
            data  : data,
            color : '#0062E3',
            points: {fillColor: '#0062E3', show: true},
            lines : {show: false}
          }];
          var options = {
//            bars: {
//              show: true
//            },
            xaxis: {
              mode: 'time',
              tickLength: 0
            },
            yaxis: {
              min: 0,
              max: 1.5,
              tickLength: 0,
              ticks: false
            },
            grid: {
              hoverable        : true,
              borderWidth      : 3,
              mouseActiveRadius: 50,
              backgroundColor  : {colors: ['#FFFFFF', '#EDF5FF']},
              axisMargin       : 20
            }
          };
          $.plot(container, dataset, options);
          container.useTooltip(r);
        }
      },
      error: function(result) {
//        container.zoomableImage('update', STATIC_URL + 'common/images/failed.jpg');
        console.log('ERROR!');
      }
    });
  }

  function pieLabelFormatter(label, series) {
//    console.log(series);
    return '<div class="badminton2_pie_label">'
      + label + ': ' + series.percent.toFixed(2) + '%, £'
      + series.data[0][1].toFixed(2) + '</div>';
//      + label + ': ' + series.percent.toFixed(2) + '%'
  }

  var previousPoint = null, previousLabel = null;
  var month = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec');

  $.fn.useTooltip = function(r) {
    $(this).bind('plothover', function(event, pos, item) {
      if (item) {
        if (r === 'g' || r === 'p' || r === 'b') {
          if (previousLabel != item.series.label || previousPoint != item.dataIndex) {
            previousPoint = item.dataIndex;
            previousLabel = item.series.label;
            $('#badminton2_tooltip').remove();

            var x = item.datapoint[0];
            var y = item.datapoint[1];
            var color = item.series.color;

            if (r === 'g') {
              var dt = new Date(x);
              showTooltip(item.pageX, item.pageY - 30, color,
                '<strong>' + dt.getDate() + ' ' + month[dt.getMonth()] + ' '
                + dt.getFullYear() + ': ' + y + ' players</strong>');
            } else if (r === 'p') { // Bar chart
              showTooltip(item.pageX, item.pageY - 30, color,
                '<strong>' + item.series.xaxis.ticks[x].label
                + ': played ' + y + ' game(s)</strong>');
            } else { // r = 'b'
              var dt = new Date(x);
              showTooltip(item.pageX, item.pageY - 30, color,
                '<strong>' + dt.getDate() + ' ' + month[dt.getMonth()] + ' '
                + dt.getFullYear() + '</strong>');
            }
          }
        }
      } else {
        $('#badminton2_tooltip').remove();
        previousPoint = null;
      }
    });
  }

  function showTooltip(x, y, color, contents) {
    $('<div id="badminton2_tooltip">' + contents + '</div>').css({
      'top': y,
      'left': x,
      'border': '2px solid ' + color
    }).appendTo('body').fadeIn(200);
  }

  $.fn.useDlg = function(r) {
    $(this).bind('plotclick', function(event, pos, item) {
      if (item) {
        if (r === 'c' || r === 'ctb') { // Pie chart
          var msg = item.series.label + ': £' + item.series.data[0][1].toFixed(2);
          alert(msg);
        }
      }
    });
  }

});
