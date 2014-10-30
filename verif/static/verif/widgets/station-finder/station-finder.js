(function($) {
  var dlg;

  $.widget('ui.stationFinder', {
    options: {
      dataset: ''
    },
/*
    _create: function() {
      var self = this, o = self.options;
      console.log('ui.stationFinder _create()');
      console.log('\t' + o.dataset);
    },
*/
    _init: function() {
      var self = this, o = self.options, el = self.element;
//      console.log('ui.stationFinder _init()');
//      console.log('\t' + o.dataset);
      el.addClass('station-finder');
      dlg = $('<div></div>').appendTo(el);
      var ajaxCounter = 0, ajaxCompletedCounter = 0;
      var timer = null;
      $('<input type="text"/>').focus().unbind().on('keyup', function(e) {
        e.preventDefault();

        var name = $.trim($(this).val());
        if (name.length >= 3) {
          if (timer != null)
            window.clearTimeout(timer);
          timer = window.setTimeout(function() {
            timer = null;
          ajaxCounter += 1;
          $('.station-finder-info').remove();
          $('.station-finder-loading').remove();
//          $('.station-finder-list').remove();
          $('<img class="station-finder-loading" src="' + STATIC_URL + 'common/images/loading.gif"/>').appendTo(dlg);
          $.ajax({
            url: 'get-stations/',
            type: 'post',
            dataType: 'json',
            data: JSON.stringify({
              'dataset': self.options.dataset,
              'name'   : name
            }),
            success: function(result) {
//              console.log('success');
              if (ajaxCompletedCounter + 1 === ajaxCounter) { // Last result
                $('.station-finder-loading').remove();
                if (result['error']) {
//                  console.log(result['error']);
                  $('<p class="station-finder-info">Request failed!</p>').appendTo(dlg);
                } else {
//                  console.log(result['number_of_results'] + ' record(s) retrieved');
                  $('<p class="station-finder-info">Found ' + result['number_of_results'] + ' station(s)</p>').appendTo(dlg);
                  console.log('Sending event station-finder-station-list...');
                  $(document).trigger('station-finder-station-list', [result['data']]);
//                  setTimeout(function() {dlg.dialog('close')}, 2000);
                }
              } else {
//                console.log('Result discarded');
              }
            },
            error: function(result) {
//              console.log('error');
              if (ajaxCompletedCounter + 1 === ajaxCounter) { // Last result
                $('.station-finder-loading').remove();
//                console.log('Error: ' + result);
                $('<p class="station-finder-info">Request failed!</p>').appendTo(dlg);
              } else {
//                console.log('Result discarded');
              }
            },
            complete: function() {
//              console.log('complete');
              ajaxCompletedCounter += 1;
            }
          });
          }, 800);
        }
      }).appendTo(dlg);
      dlg.dialog({
        title: 'Station Finder'
      });
    },

    destroy: function() {
      var self = this, el = self.element;
//      console.log('ui.stationFinder destroy');
      el.removeClass('station-finder');
      el.empty();

      $.Widget.prototype.destroy.call(this);
    },

    open: function() {
      console.log('ui.stationFinder open');
      dlg.dialog('open');
    },

    close: function() {
      console.log('ui.stationFinder close');
      dlg.dialog('close');
    }
  });

})(jQuery);
