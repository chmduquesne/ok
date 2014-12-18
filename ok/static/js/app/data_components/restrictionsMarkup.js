"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(restrictionsMarkup);

    function restrictionsMarkup(){

      this.renderGroupsMarkup = function(ev, data) {
        var params = {"grou": []};
        for (var group in data.response){
          params.groups.push({"groupname": group, "encodedgroupname": encodeURIComponent(group)});
        }
        var markup = Mustache.render(templates.restrictionsMarkup, params);
        this.trigger("dataGroupsMarkupRendered", {markup: markup});
      }

      this.after("initialize", function() {
        this.on(window, "dataGroupsReceived", this.renderGroupsMarkup);
      });
    }
  }
);
