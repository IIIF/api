;(function ($, window, document, undefined) {
  var pluginName = "iiifDemo",
    defaults = {
      selectOptions: {},
      roundToCutoff: 50,
      iiifImgInfo: {},
    };

  function Plugin(element, options) {
    this.$element = $(element);
    this.options = $.extend({}, defaults, options);
    this.regions = [];
    this.selectValues = {};

    this._defaults = defaults;
    this._name = pluginName;

    this.init();
  }

  Plugin.prototype = {

    init: function() {
      this.$imgContainer   = this.$element.find('.iiif-image-container'),
      this.$iiifImg        = this.$imgContainer.find('img'),
      this.$selectRegion   = this.$element.find('.iiif-select-region'),
      this.$selectSize     = this.$element.find('.iiif-select-size'),
      this.$selectRotation = this.$element.find('.iiif-select-rotation');

      this.calculateSelectValues();
      this.render();
      this.bindEvents();
    },


    render: function() {
      this.loadRegionSelectValues();
    },


    loadRegionSelectValues: function(region) {
      region = region || this.regions[0];

      this.updateOptions(this.$selectRegion, this.regions, region);
      this.loadSizeSelectValues(region);
    },


    loadSizeSelectValues: function(region, size) {
      var sizes = this.getSizesFor(region);

      size = size || sizes[0];

      this.updateOptions(this.$selectSize, sizes, size);
      this.loadRotationSelectValues(region, size);
    },


    loadRotationSelectValues: function(region, size, rotation) {
      var rotations = this.getRotationsFor(region, size);

      rotation = rotation || rotations[0];

      this.updateOptions(this.$selectRotation, rotations, rotation);
      this.renderIiifImg(region, size, rotation);
    },


    calculateSelectValues: function () {
      var w = this.$imgContainer.width(),
          h = this.$imgContainer.height(),
          regex = /([wh](\s*[-+]\s*\d+)?)/i, // matches 'w - 200,' and ',h'
          _this = this;

      $.each(this.options.selectOptions, function(region, values) {
        $.each(values, function(size, rotation) {
          // options like 'w - 200,' & ',h' are evaluated with image container dimensions
          size = size.replace(regex, function(match) {
            return _this.roundTo(parseInt(eval(match)), 10);
          });

          if (!_this.selectValues.hasOwnProperty(region)) {
            _this.selectValues[region] = {};
            _this.regions.push(region);
          }

          _this.selectValues[region][size] = rotation;
        });
      });
    },


    bindEvents: function() {
      var _this = this;

      $(window).resize(function() {
        _this.selectValues = {};
        _this.calculateSelectValues();
        _this.render();
      });

      this.$selectRegion.on('change', function() {
        _this.loadSizeSelectValues($(this).val());
      });

      this.$selectSize.on('change', function() {
        _this.loadRotationSelectValues(_this.$selectRegion.val(), $(this).val());
      });

      this.$selectRotation.on('change', function() {
        _this.renderIiifImg(_this.$selectRegion.val(), _this.$selectSize.val(), $(this).val());
      });
    },


    updateOptions: function($element, options, selected) {
      $element.html('');

      $.each(options, function(index, option) {
        $element.append('<option value="' + option + '">' + option + '</option>');
      });

      $element.val(selected).attr('selected', 'selected');
    },


    renderIiifImg: function(region, size, rotation) {
      this.$iiifImg
        .attr('src', '')
        .hide()
        .attr('src', this.getIiifUrl(region, size, rotation)).fadeIn(300);
    },


    getIiifUrl: function(region, size, rotation) {
      var info = this.options.iiifImgInfo;

      return [info.baseUrl, region, size, rotation, info.quality + '.' + info.format].join('/');
    },

    getSizesFor: function(region) {
      return $.map(this.selectValues[region], function(obj, size) { return size });
    },


    getRotationsFor: function(region, size) {
      return this.selectValues[region][size];
    },


    roundTo: function(value) {
      var cutoff = this.options.roundToCutoff || 0;
      return Math.max(value - (value % cutoff), cutoff);
    }

  };

  $.fn[pluginName] = function (options) {
    return this.each(function () {
      if (!$.data(this, "plugin_" + pluginName)) {
        $.data(this, "plugin_" + pluginName, new Plugin(this, options));
      }
    });
  };

})(jQuery, window, document);
