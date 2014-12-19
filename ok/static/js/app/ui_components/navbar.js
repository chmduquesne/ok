"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(navbar);

    function navbar(){

      this.update = function(ev, data) {
        this.$node.html(data.markup);
      }

      this.after("initialize", function() {
        this.on(window, "dataNavbarRendered", this.update);
      });
    }
  }
);
