"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(navbar);

    function navbar(){

      this.renderNavbar = function(ev, data) {
        var params = { };
        params[data.components[0]] = true;
        var markup = Mustache.render(templates.navbar, params);
        this.trigger("#navbar", "dataNavbarRendered", {markup: markup});
      }

      this.after("initialize", function() {
        this.on("dataHashComponentsReceived", this.renderNavbar);
      });
    }
  }
);
