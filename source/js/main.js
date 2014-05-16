// on document ready
$(function() {
  interactiveImg.render();
});


var interactiveImg = (function() {
  var frameHeight,
      frameWidth,
      ddOptions = {},
      elIiifContainer = $('.main-interactive-image .container-image'),
      elIiifImg = $('.main-interactive-image .container-image img'),
      elTryItRegion = $('.try-it-region'),
      elTryItSize = $('.try-it-size'),
      elTryItRotation = $('.try-it-rotation');

  // BL's image (5213 x 5706) accessioned at Stanford
  var iiifImg = {
        baseUrl: 'http://stacks.stanford.edu/image/iiif/ff139pd0160%252FK90113-43',
        region: 'full',
        size: 'full',
        rotation: 0,
        quality: 'native',
        format: 'jpg'
      };


  function init() {
    calculateSelectOptions();
    loadImage();
    attachEvents();
  }


  function loadImage() {
    loadRegionOptions();
  }


  function attachEvents() {
    $(window).resize(function() {
      calculateSelectOptions();
      loadImage();
    });

    elTryItRegion.on('change', function() {
      loadSizeOptions($(this).val());
    });

    elTryItSize.on('change', function() {
      var region = elTryItRegion.val();

      loadRotationOptions(region, $(this).val());
    });

    elTryItRotation.on('change', function() {
      var region = elTryItRegion.val(),
          size = elTryItSize.val();

      renderIiifImg(region, size, $(this).val());
    });
  }


  function loadRegionOptions(region, size, rotation) {
    var regions = getRegions();

    if (typeof region === 'undefined') {
      region = regions[0];
    }

    elTryItRegion.html('');

    $.each(regions, function(index, option) {
      elTryItRegion.append('<option value="' + option + '">' + option + '</option>');
    });

    elTryItRegion.val(region).attr('selected', 'selected');

    loadSizeOptions(region, size, rotation);
  }


  function loadSizeOptions(region, size, rotation) {
    var sizes = getSizesFor(region);

    if (typeof size === 'undefined') {
      size = sizes[0];
    }

    elTryItSize.html('');

    $.each(sizes, function(index, option) {
      elTryItSize.append('<option value="' + option + '">' + option + '</option>');
    });

    elTryItSize.val(size).attr('selected', 'selected');

    loadRotationOptions(region, size, rotation);
  }


  function loadRotationOptions(region, size, rotation) {
    var rotations = getRotationsFor(region, size);

    if (typeof rotation === 'undefined') {
      rotation = rotations[0];
    }

    elTryItRotation.html('');

    $.each(rotations, function(index, option) {
      elTryItRotation.append('<option value="' + option + '">' + option + '</option>');
    });

    elTryItRotation.val(rotation).attr('selected', 'selected');

    renderIiifImg(region, size, rotation);
  }


  function getRegions() {
    var regions = [];

    $.each(ddOptions, function(region, obj) {
      regions.push(region);
    });

    return regions;
  }


  function getSizesFor(region) {
    var sizes = [];

    $.each(ddOptions[region], function(size, obj) {
      sizes.push(size);
    });

    return sizes;
  }


  function getRotationsFor(region, size) {
    return ddOptions[region][size];
  }


  function renderIiifImg(region, size, rotation) {
    elIiifImg.hide();
    elIiifImg.attr('src', getIiifUrl(region, size, rotation)).fadeIn(300);
  }


  function getIiifUrl(region, size, rotation) {
    return [iiifImg.baseUrl, region, size, rotation, iiifImg.quality + '.' + iiifImg.format].join('/');
  }


  function calculateFrameDimensions() {
    frameHeight = elIiifContainer.height();
    frameWidth  = elIiifContainer.width();
  }


  function calculateSelectOptions() {
    calculateFrameDimensions();

    ddOptions = {
      '0,1200,5213,2242'    : {},
      '1400,1200,2500,1075' : {},
      'full'                : {},
      '2325,1300,800,800'   : {},
      '3050,3000,1200,1600' : {},
      '2150,4500,1500,645'  : {},
      '2125,4375,4500,1935' : {}
    }

    ddOptions['0,1200,5213,2242'][frameWidth + ','] = [0];
    ddOptions['0,1200,5213,2242'][roundTo(frameWidth - 200) + ','] = [0];
    ddOptions['0,1200,5213,2242'][roundTo(frameWidth - 400) + ','] = [0];

    ddOptions['1400,1200,2500,1075'][frameWidth + ','] = [0];
    ddOptions['1400,1200,2500,1075'][roundTo(frameWidth - 200) + ','] = [0];
    ddOptions['1400,1200,2500,1075'][roundTo(frameWidth - 400) + ','] = [0];

    ddOptions['full'][',' + frameHeight] = [0,90,180,270];
    ddOptions['full'][',' + roundTo(frameHeight - 200)] = [0,90,180,270];

    ddOptions['2325,1300,800,800']['400,400'] = [0,90,180,270];
    ddOptions['2325,1300,800,800']['200,200'] = [0,90,180,270];
    ddOptions['2325,1300,800,800']['100,100'] = [0,90,180,270];

    ddOptions['3050,3000,1200,1600']['300,400'] = [0,90,180,270];
    ddOptions['3050,3000,1200,1600']['225,300'] = [0,90,180,270];
    ddOptions['3050,3000,1200,1600']['150,200'] = [0,90,180,270];

    ddOptions['2150,4500,1500,645'][frameWidth + ','] = [0];
    ddOptions['2150,4500,1500,645'][roundTo(frameWidth - 200) + ','] = [0];
    ddOptions['2150,4500,1500,645'][roundTo(frameWidth - 400) + ','] = [0];

    ddOptions['2125,4375,4500,1935'][frameWidth + ','] = [0];
    ddOptions['2125,4375,4500,1935'][roundTo(frameWidth - 200) + ','] = [0];
    ddOptions['2125,4375,4500,1935'][roundTo(frameWidth - 400) + ','] = [0];
  }


  function roundTo(value) {
    var cutoff = 50;

    value = value - (value % cutoff);

    return (value < cutoff) ? cutoff : value;
  }

  return {
    render: function() {
      init();
    }
  };

})();
