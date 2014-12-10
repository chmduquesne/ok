"use strict";

requirejs.config({
  baseUrl: '',
});

require(
  [
    "bower_components/flight/lib/debug"
  ],
  function(debug) {
    debug.enable(true);
    require(
      [ "js/app/boot/page" ],
      function(initialize) {
        initialize();
      }
    );
  }
);
