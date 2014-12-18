"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "js/app/templates",
    "bower_components/mustache/mustache"
  ],

  function(defineComponent, templates, Mustache){
    return defineComponent(markup);

    function markup(){

      this.renderUsers = function(ev, data) {
        var params = {"users": []};
        for (var user in data.response){
          var groupList = []
          for (var i in data.response[user]){
            groupname = data.response[user]["groups"][i];
            groupList.push({
              "groupname": groupname,
              "encodedgroupname": encodeURIComponent(groupname)
            });
          }
          params.users.push({
            "username": user,
            "encodedusername": encodeURIComponent(user),
            "groups": groupList
          });
        }
        var markup = Mustache.render(templates.usersMarkup, params);
        this.trigger("#display", "dataUsersRendered", {markup: markup});
      }

      this.renderGroups = function(ev, data) {
        var params = {"groups": []};
        for (var group in data.response){
          params.groups.push({"groupname": group, "encodedgroupname": encodeURIComponent(group)});
        }
        var markup = Mustache.render(templates.groupsMarkup, params);
        this.trigger("#display", "dataGroupsRendered", {markup: markup});
      }

      this.renderRestrictions = function(ev, data){
        var params = {"restrictions": []};
        for (var restriction in data.response){
          params.restrictions.push({
            "restrictionname": restriction,
            "encodedrestrictionname": encodeURIComponent(restriction)
          });
        }
        var markup = Mustache.render(templates.restrictionsMarkup, params);
        this.trigger("#display", "dataRestrictionsRendered", {markup: markup});
      };

      this.renderUser = function(ev, data){
        var params = {"groups": []};
        for (var i in data.response["groups"]){
          params.groups.push({
            "groupname": data.response["groups"][i],
            "encodedgroupname": encodeURIComponent(data.response["groups"][i])
          });
        }
        var markup = Mustache.render(templates.userMarkup, params);
        this.trigger("#display", "dataUserRendered", {markup: markup});
      };

      this.renderGroup = function(ev, data){
        var params = {"restrictions": [], "hint": true};
        params["hint"] = JSON.stringify(data.response["hint"]);
        for (var i in data.response["restrictions"]){
          var r = data.response.restrictions[i];
          params.restrictions.push({
            "pattern": r[0],
            "restrictionname": r[1],
            "encodedrestrictionname": encodeURIComponent(r[1]),
            "parameters": JSON.stringify(r[2])
          });
        }
        var markup = Mustache.render(templates.groupMarkup, params);
        this.trigger("#display", "dataGroupRendered", {markup: markup});
      };

      this.renderRestriction = function(ev, data){
        var params = {"description": data.response.description.doc};
        var markup = Mustache.render(templates.restrictionMarkup, params);
        this.trigger("#display", "dataRestrictionRendered", {markup: markup});
      };

      this.after("initialize", function() {
        this.on("dataUsersReceived", this.renderUsers);
        this.on("dataGroupsReceived", this.renderGroups);
        this.on("dataRestrictionsReceived", this.renderRestrictions);
        this.on("dataUserReceived", this.renderUser);
        this.on("dataGroupReceived", this.renderGroup);
        this.on("dataRestrictionReceived", this.renderRestriction);
      });
    }
  }
);
