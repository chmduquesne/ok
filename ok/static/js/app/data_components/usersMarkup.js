"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(usersMarkup);

    function usersMarkup(){

      this.renderUsersMarkup = function() {
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
        var markup = Mustache.render(templates.usersMarkup, params);
        this.trigger("dataUsersDisplayRendered", {markup: markup});
      }

      this.after("initialize", function() {
        this.renderUsersMarkup();
      });
    }
  }
);
