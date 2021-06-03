// add anchor images and links when hovering over anchors
window.onload = function() {
  anchors.options.placement = 'left';
  anchors.add();
};

// update the hash fragment as we scroll
$(document).bind('scroll', function(e) {
  $('h2,h3,h4').each(function() {
    if ($(this).offset().top < window.pageYOffset + 5 && $(this).offset().top + $(this).height() > window.pageYOffset + 5) {
      var urlId = '#' + $(this).attr('id');
      window.history.replaceState(null, null, urlId);
    }
  });
});
