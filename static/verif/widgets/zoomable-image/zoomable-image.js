(function($) {
  var img;

  $.widget('ui.zoomableImage', {
    options: {
      zoomable: true,
      metadata: {}
    },

    _init: function() {
      var self = this, o = self.options, el = self.element;
//      console.log('_init');
      el.addClass('zoomable-image').addClass('zoomable-image-container');
      img = $('<img/>').addClass('zoomable-image-img').load(function() {
//        console.log('Image loaded, width = ' + this.width + ', height = ' + this.height);
        el.css({
          'width' : this.width,
          'height': this.height
        });
      }).appendTo(el);
    },

    destroy: function() {
      var self = this, el = self.element;
      el.removeClass('zoomable-image');
      el.empty();

      $.Widget.prototype.destroy.call(this);
    },

    _setOption: function(k, v) {
      var self = this, o = self.options, el = self.element;
      if (k === 'zoomable') {
        if (v) { // Zoomable
 //         console.log('Zoomable');

          var rect = $('<div>').addClass('zoomable-image-rect');
          var drag = false;
          var startX, startY;
          var x1, x2, y1, y2;

          // Notice the off() methods to avoid event been triggered multiple
          // times. Without off(), each time a new handler is attached
          el.off('mouseenter').on('mouseenter', function(e) {
            e.preventDefault();
            el.css('cursor', 'crosshair');
          }).off('mouseleave').on('mouseleave', function(e) {
            e.preventDefault();
            el.css('cursor', 'default');
          }).off('mousedown').on('mousedown', function(e) {
            e.preventDefault();
            drag = true;
            startX = e.pageX, startY = e.pageY;
//            console.log('Mouse down at (' + startX + ', ' + startY + ')');
            rect.css({
              'top'   : startY + 'px',
              'left'  : startX + 'px',
              'width' : '0',
              'height': '0'
            });
            rect.appendTo(el);

            var offset = $(this).offset();
//            console.log('offset.left: ' + offset.left + ', offset.top: ' + offset.top);
            var xy = getXY(startX - offset.left, startY - offset.top, o.metadata);
            x1 = xy[0], y1 = xy[1];
//            console.log('-> (' + x1 + ', ' + y1 + ')');
          }).off('mousemove').on('mousemove', function(e) {
            e.preventDefault();
            if (drag) { // Draw a rectangle
              var endX = e.pageX, endY = e.pageY;
//              console.log('Mouse move at (' + endX + ', ' + endY + ')');
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
          }).off('mouseup').on('mouseup', function(e) {
            e.preventDefault();
            drag = false;
            var endX = e.pageX, endY = e.pageY;
//            console.log('Mouse up at (' + endX + ', ' + endY + ')');
            rect.remove();

            var offset = $(this).offset();
//            console.log('offset.left: ' + offset.left + ', offset.top: ' + offset.top);
            var xy = getXY(endX - offset.left, endY - offset.top, o.metadata);
            x2 = xy[0], y2 = xy[1];
//            console.log('-> (' + x2 + ', ' + y2 + ')');

            if (x1 > x2) [x1, x2] = [x2, x1];
            if (y1 > y2) [y1, y2] = [y2, y1];
            x1 = x1 < o.metadata['x_min'] ? o.metadata['x_min'] : x1;
            y1 = y1 < o.metadata['y_min'] ? o.metadata['y_min'] : y1;
            x2 = x2 > o.metadata['x_max'] ? o.metadata['x_max'] : x2;
            y2 = y2 > o.metadata['y_max'] ? o.metadata['y_max'] : y2;
//            console.log('x1, y1, x2, y2: ' + x1 + ', ' + y1 + ', ' + x2 + ', ' + y2);
            console.log('Sending event zoomable-image-selected-area...');
            $(document).trigger('zoomable-image-selected-area', [{
              'x1': x1,
              'y1': y1,
              'x2': x2,
              'y2': y2
            }]);
          });
        } else {
          el.unbind();
        }
      }
      this._super(k, v);
    },

    update: function(imgSrc) {
//      console.log('Update img src to ' + imgSrc);
      img.attr('src', imgSrc);
    }
  });

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
})(jQuery);
