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

        // Load the route into an "a" anchor to simplify parsing
        var route = document.createElement("a");
        route.href = hash;

        var path = route.pathname;
        var components = path.split("/");
        // Remove the empty components
        for (var i = components.length - 1; i >= 0; i--){
          if (components[i] == ""){
            components.splice(i, 1);
          }
        }

        // If one of the query parameters is as_filter, then remove the
        // last component since it is part of the search
        var search = route.search;
        var as_filter = false;
        var search_components = (search.split("?")[1] || "").split("&");
        for (var i in search_components){
          var items = search_components[i].split("=");
          if (items[0] == "as_filter"){
            as_filter = true;
          }
        }
        if (as_filter){
          search = components[components.length - 1] + search;
          components.splice(components.length - 1, 1);
        }

        this.trigger("dataHashComponentsReceived", {components: components});

        if (components.length == 0 || components.length > 2){
          location.assign("#users");
          return;
        }
        if (components.length == 1) {
          if (components[0] == "users") {
            this.trigger("dataShouldGetUsers", {search: search});
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
        this.on("hashchange", this.onHashchange);
        this.on("dataUserCreated", this.onHashchange);
        this.on("dataGroupCreated", this.onHashchange);

        // Trigger the first "hash change"
        this.onHashchange();
      });
    }
  }
);
