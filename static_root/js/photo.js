
jQuery(function () {
  var $ = jQuery,
  container = $(window),
  containerW,
  containerH,
  slides = [],
  i = 0,
  imgs = $('.post-body img');

  (function init() {

    measure();

    // Build array of slides for gallery
    imgs.each(function (index, value) {

      value = $(value);
      var src = value.attr('src'),
      width = value.attr('width'),
      height = value.attr('height');

      if (src && width && height) {

        var dimensions = getImageDimensions(parseInt(width), parseInt(height));
        var o = {
          el: value,
          src: src,
          origW: width,
          origH: height,
          w: dimensions.width,
          h: dimensions.height };


        // Caption
        var figure = value.parent(),
        caption = figure.find('figcaption').text();
        if (caption) {
          o.title = caption;
        }

        slides.push(o);

        // Add event listener and CSS class to each image
        $(value).
        attr('data-index', i).
        on('click', function () {
          var index = parseInt($(this).attr('data-index'));
          openPhotoSwipe(index);
        });
        figure.addClass('is-photoswipeable');
        i++;
      }
    });

    $(window).on('resize', function () {
      debouncedMeasure();
    });

  })();

  // Measure the PhotoSwipe container
  function measure(callback) {
    containerW = container.width();
    containerH = container.height();
    if (callback) {
      callback.call();
    }
  }

  var debouncedMeasure = _.debounce(function () {
    measure(resetImageDimensions);
  }, 250);

  // If image is landscape or square, set width to gallery width and height to width * ratio
  // If image is portrait, set height to gallery height and width to height / ratio
  function getImageDimensions(w, h) {
    var ratio = h / w;
    if (w >= h) {
      return {
        width: containerW,
        height: Math.round(containerW * ratio) };

    } else {
      return {
        width: Math.round(containerH / ratio),
        height: containerH };

    }
  }

  // Parse picture and gallery id from URL (#&pid=1&gid=2)
  function photoswipeParseHash() {
    var hash = window.location.hash.substring(1),
    params = {};

    if (hash.length < 5) {
      return params;
    }

    var vars = hash.split('&');
    for (var i = 0; i < vars.length; i++) {if (window.CP.shouldStopExecution(0)) break;
      if (!vars[i]) {
        continue;
      }
      var pair = vars[i].split('=');
      if (pair.length < 2) {
        continue;
      }
      params[pair[0]] = pair[1];
    }window.CP.exitedLoop(0);

    if (params.gid) {
      params.gid = parseInt(params.gid, 10);
    }

    if (!params.hasOwnProperty('pid')) {
      return params;
    }
    params.pid = parseInt(params.pid, 10);
    return params;
  }

  function openPhotoSwipe(index) {

    var gallery,
    options;

    options = {
      index: index,
      galleryUID: 1,
      shareEl: false,
      allowPanToNext: true };


    // Pass data to PhotoSwipe and initialize it
    gallery = new PhotoSwipe(document.getElementById('photoswipe'), PhotoSwipeUI_Default, slides, options);

    gallery.init();
  }

  // If window has resized, reset the dimensions of the images in the slides array
  function resetImageDimensions() {
    slides.forEach(function (element) {
      var d = getImageDimensions(parseInt(element.origW), parseInt(element.origH));
      element.w = d.width;
      element.h = d.height;
    });
  }

  // Parse URL and open gallery if it contains #&pid=3&gid=1
  var hashData = photoswipeParseHash();
  if (hashData.pid > 0 && hashData.gid > 0) {
    openPhotoSwipe(hashData.pid - 1);
  }

});
