$(document).ready(function () {
  let mainText = $(".sidewise_text").text();
  let changedText = $(".sidewise_text").data("ex");
  $(".sidewise_text").hover(
    function () {
      $(this).text(changedText);
    },
    function () {
      $(this).text(mainText);
    },
  );
});
