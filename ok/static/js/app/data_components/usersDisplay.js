"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(usersDisplay);

    function usersDisplay(){

      // Build the html for the usersDisplay from the current url hash
      this.renderUsersDisplay = function() {
        var params = {
          "users": [
            { "username": "mark",
              "groups": [
                {"groupname": "users", "first": true},
                {"groupname": "admin"},
                {"groupname": "audio"}
              ]
            },
            { "username": "john",
              "groups": [
                {"groupname": "users", "first": true},
                {"groupname": "video"},
                {"groupname": "sudo"}
              ]
            },
            { "username": "mary",
              "groups": [
                {"groupname": "users", "first": true},
                {"groupname": "vbox"},
              ]
            },
          ]
        }
        var markup = Mustache.render(templates.usersDisplay, params);
        this.trigger("dataUsersDisplayRendered", {markup: markup});
      }

      this.after("initialize", function() {
        // serve once before attaching
        this.renderUsersDisplay();
      });
    }
  }
);
