"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(breadcrumbs);

    function breadcrumbs(){

      this.update = function(ev, data) {
        this.$node.html(data.markup);
      }

      this.after("initialize", function() {
        this.on(window, "dataBreadcrumbsRendered", this.update);
      });
    }
  }
);
