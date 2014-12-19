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

        this.trigger("dataHashComponentsReceived", {components: components});

        if (components.length == 0 || components.length > 2){
          location.assign("#users");
          return;
        }
        if (components.length == 1) {
          if (components[0] == "users") {
            this.trigger("dataShouldGetUsers");
            return;
          }
          if (components[0] == "groups") {
            this.trigger("dataShouldGetGroups");
            return;
          }
          if (components[0] == "restrictions") {
            this.trigger("dataShouldGetRestrictions");
            return;
          }
        }
        if (components.length == 2) {
          if (components[0] == "users") {
            this.trigger("dataShouldGetUser", {encodedUsername: components[1]});
            return;
          }
          if (components[0] == "groups") {
            this.trigger("dataShouldGetGroup", {encodedGroupname: components[1]});
            return;
          }
          if (components[0] == "restrictions") {
            this.trigger("dataShouldGetRestriction", {encodedRestrictionName: components[1]});
            return;
          }
        }
        location.assign("#users");
      }

      this.after("initialize", function() {
        this.on(window, "hashchange", this.onHashchange);

        // Trigger the first "hash change"
        this.onHashchange();
      });
    }
  }
);
