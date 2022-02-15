let mix = require("laravel-mix");

mix
  .sass("src/scss/style.scss", "static/css/style.css")
  .js("src/js/index.js", "static/js/main.js");
