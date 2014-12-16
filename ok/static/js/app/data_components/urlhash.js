"use strict";

define(
  [
    "bower_components/flight/lib/component"
  ],

  function(defineComponent){
    return defineComponent(urlhash);

    function urlhash(){

      this.onHashchange = function() {
        // See http://stackoverflow.com/questions/1703552/encoding-of-window-location-hash
        var hash = location.href.split("#")[1] || "";
        var components = hash.split("/");
        console.log("hash changed to " + hash);
        if (components.length == 0 || components.length > 2){
          location.assign("#users");
          return;
        }
        if (components.length == 1) {
          if (components[0] == "users") {
            this.trigger("uiShouldShowMultipleUsersView");
            this.trigger("dataShouldGetUsers");
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
          if (components[0] == "groups") {
            this.trigger("uiShouldShowMultipleGroupsView");
            this.trigger("dataShouldGetGroups");
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
          if (components[0] == "restrictions") {
            this.trigger("uiShouldShowMultipleRestrictionsView");
            this.trigger("dataShouldGetRestrictions");
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
        }
        if (components.length == 2) {
          if (components[0] == "users") {
            this.trigger("uiShouldShowSingleUserView", {username: components[1]});
            this.trigger("dataShouldGetUser", {encodedUsername: components[1]});
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
          if (components[0] == "groups") {
            this.trigger("uiShouldShowSingleGroupView", {groupname: components[1]});
            this.trigger("dataShouldGetGroup", {encodedGroupname: components[1]});
            this.trigger("dataShouldRenderBreadCrumbs", {components: components});
            return;
          }
          if (components[0] == "restrictions") {
            this.trigger("uiShouldShowSingleRestrictionView", {groupname: components[1]});
            this.trigger("dataShouldGetRestriction", {encodedRestrictionName: components[1]});
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
