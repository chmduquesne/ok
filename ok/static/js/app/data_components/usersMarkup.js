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
                {"groupname": "users", "first": true, "encodedgroupname": "users"},
                {"groupname": "admin", "encodedgroupname": "admin"},
                {"groupname": "audio", "encodedgroupname": "audio"}
              ]
            },
            { "username": "john",
              "groups": [
                {"groupname": "users", "first": true, "encodedgroupname": "users"},
                {"groupname": "video", "encodedgroupname": "video"},
                {"groupname": "sudo", "encodedgroupname": "sudo"}
              ]
            },
            { "username": "mary",
              "groups": [
                {"groupname": "users", "first": true, "encodedgroupname": "users"},
                {"groupname": "vbox", "encodedgroupname": "vbox"},
              ]
            },
          ]
        }
        var markup = Mustache.render(templates.usersMarkup, params);
        this.trigger("dataUsersMarkupRendered", {markup: markup});
      }

      this.after("initialize", function() {
        this.renderUsersMarkup();
      });
    }
  }
);
