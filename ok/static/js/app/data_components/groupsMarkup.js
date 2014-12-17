"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(groupsMarkup);

    function groupsMarkup(){

      this.renderGroupsMarkup = function(ev, data) {
        var params = {"groups": []};
        for (var group in data.response){
          params.groups.push({"groupname": group, "encodedgroupname": encodeURIComponent(group)});
        }
        var markup = Mustache.render(templates.groupsMarkup, params);
        this.trigger("dataGroupsMarkupRendered", {markup: markup});
      }

      this.after("initialize", function() {
        this.on(window, "dataGroupsReceived", this.renderGroupsMarkup);
      });
    }
  }
);
