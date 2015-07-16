$(document).ready(function() {
  
  $(window).resize(function() {
    
    var window_width = $(window).innerWidth(),
      per_line = (window_width > 1280 ? 4 : (window_width > 1024 ? 3 : (window_width > 720 ? 2 : 1)));
      width = $(window).innerWidth() / per_line,
      height = Math.floor(width * 400/720);
      
    $("article").width(width).height(height);
  });
  
});
