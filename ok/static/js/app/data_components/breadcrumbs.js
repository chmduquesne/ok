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

      this.renderBreadcrumbs = function(ev, data) {
        var components = data.components;
        var params = { "path" : [] };
        for (var i in components) {
          var target = "#" + components.slice(0, i+1).join("/");
          var component = components[i];
          params.path.push({"target": target, "component": decodeURIComponent(component)});
        }
        var markup = Mustache.render(templates.breadcrumbs, params);
        this.trigger("dataBreadcrumbsRendered", {markup: markup});
      }

      this.after("initialize", function() {
        this.on("dataHashComponentsReceived", this.renderBreadcrumbs);
      });
    }
  }
);
