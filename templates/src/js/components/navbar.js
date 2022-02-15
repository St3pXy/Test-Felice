jQuery(document).ready(function ($) {
  $(".navbar-toggler").hover(
    function () {
      // over
      $(".bar_cover .bar:nth-last-child(1)").addClass("active");
    },
    function () {
      // out
      $(".bar_cover .bar:nth-last-child(1)").removeClass("active");
    },
  );
});
