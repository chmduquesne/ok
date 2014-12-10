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

      this.serveBreadcrumbs = function() {
        var components = window.location.hash.substring(1).split("/");
        var params = { "path" : [] };
        for (var i in components) {
          var target = "#" + components.slice(0, i+1).join("/");
          var component = components[i];
          params.path.push({"target": target, "component": component});
        }
        console.log(params)
        var markup = Mustache.render(templates.breadcrumbs, params);
        this.trigger("breadcrumbsServed", {markup: markup});
      }

      this.after("initialize", function() {
        this.serveBreadcrumbs();
        this.on("hashchange", this.serveBreadcrumbs);
      });
    }
  }
);
