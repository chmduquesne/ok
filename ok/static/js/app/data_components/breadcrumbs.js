"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(breadcrumbs);

    function breadcrumbs(){

      // Build the html for the breadcrumbs from the current url hash
      this.serveBreadcrumbs = function() {
        var components = window.location.hash.substring(1).split("/");
        var params = { "path" : [] };
        for (var i in components) {
          var target = "#" + components.slice(0, i+1).join("/");
          var component = components[i];
          params.path.push({"target": target, "component": component});
        }
        var markup = Mustache.render(templates.breadcrumbs, params);
        this.trigger("breadcrumbsServed", {markup: markup});
      }

      this.after("initialize", function() {
        // serve once before attaching
        this.serveBreadcrumbs();
        this.on("hashchange", this.serveBreadcrumbs);
      });
    }
  }
);
