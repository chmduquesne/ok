"use strict";

define(
  [
    "bower_components/flight/lib/component"
  ],

  function(defineComponent){
    return defineComponent(urlhash);

    function urlhash(){

      this.onHashchange = function() {
        var components = window.location.hash.substring(1).split("/");
        if (components.length == 0 || components.length > 2){
          location.assign("#users");
          return;
        }
        if (components.length == 1) {
          if (components[0] == "users") {
            this.trigger("uiShouldShowMultipleUsersView");
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
          if (components[0] == "groups") {
            this.trigger("uiShouldShowMultipleGroupsView");
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
        }
        if (components.length == 2) {
          if (components[0] == "users") {
            this.trigger("uiShouldShowSingleUserView", {username: components[1]});
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
          if (components[0] == "groups") {
            this.trigger("uiShouldShowSingleGroupView", {groupname: components[1]});
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
        }
        location.assign("#users");
      }

      this.after("initialize", function() {
        this.onHashchange();
        this.on(window, "hashchange", this.onHashchange);
      });
    }
  }
);
