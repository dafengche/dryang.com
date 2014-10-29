(function($) {
  $.widget('ui.stationFinder', {
    options: {
      dataset: ''
    },

    _create: function() {
      var self = this, o = self.options;
      console.log('ui.stationFinder _create()');
      console.log('\t' + o.dataset);
    },

    _init: function() {
      var self = this, o = self.options, el = self.element;
      console.log('ui.stationFinder _init()');
      console.log('\t' + o.dataset);
      el.addClass('station-finder');
      var dlg = $('<div></div>').appendTo(el);
      $('<input type="text"/>').focus().unbind().on('keyup', function(e) {
        e.preventDefault();
        var name = $.trim($(this).val());
        if (name.length >= 3) {
          $.ajax({
            url: 'get-stations/',
            type: 'post',
            dataType: 'json',
            data: JSON.stringify({
              'dataset': self.options.dataset,
              'name'   : name
            }),
            success: function(result) {
              console.log('Success');
              if (result['error'])
                 console.log(result['error']);
              else {
                 console.log(result['number_of_results'] + ' record(s) retrieved');
                 $('.station-finder-info').remove();
                 $('<p class="station-finder-info">Found ' + result['number_of_results'] + ' station(s)</p>').appendTo(dlg);
                 $('.station-finder-list').remove();
                 if (result['number_of_results'] > 0) {
                   var sel = $('<select class="station-finder-list"></select>');
                   var optionsAsString = '';
                   $.each(result['data'], function(k, v) {
//                     console.log(v[0] + ', ' + v[1] + ', ' + v[2]);
                     optionsAsString += "<option value='" + v[0] + "'>" + v[1] + "</option>";
                   });
                   sel.append(optionsAsString).appendTo(dlg);
                 }
              }
            },
            error: function(result) {
              console.log('Error: ' + result);
            }
          });
        }
      }).appendTo(dlg);
      dlg.dialog({
        title: 'Station Finder'
      });
    },

    destroy: function() {
      var self = this, el = self.element;
      console.log('ui.stationFinder destroy');
      el.removeClass('station-finder');
      el.empty();

      $.Widget.prototype.destroy.call(this);
    }

  });

})(jQuery);
