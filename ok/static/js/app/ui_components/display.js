"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(display);

    function display(){

      this.update = function(ev, data) {
        this.$node.html(data.markup);
      }

      this.after("initialize", function() {
        this.on("dataUsersDisplayRendered", this.update);
      });
    }
  }
);
