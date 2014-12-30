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

      this.renderUsersDisplay = function(ev, data) {
        var params = {"users": [], "pages": [], "search": ""};
        if (data.search){
          params.search = data.search;
        }
        for (var user in data.response.users){
          var groupList = [];
          var first = true;
          for (var i in data.response.users[user]["groups"]){
            var groupname = data.response.users[user]["groups"][i];
            groupList.push({
              "groupname": groupname,
              "encodedgroupname": encodeURIComponent(groupname),
              "first": first
            });
            if (first){
              first = false;
            }
          }
          params.users.push({
            "username": user,
            "encodedusername": encodeURIComponent(user),
            "groups": groupList
          });
        }
        var p = data.response.page;
        var n = p;
        if (data.response.more_results) {
          n = p + 1;
        }
        if (data.response.total_pages) {
          n = data.response.total_pages;
        }
        params.first_page = 1;
        params.last_page = n;
        params.prev_page = Math.max(1, p - 1);
        params.next_page = Math.min(n, p + 1);
        var start = Math.max(1, p - 5);
        var stop = Math.min(n, p + 5);
        if (start > p - 5){
          stop = Math.min(n, stop + start - (p - 5));
        }
        if (stop < p + 5){
          start = Math.max(1, start - (p + 5 - stop));
        }
        for (var i = start; i <= stop; i++){
          var page = {"page": i}
          if (i == p){
            page.active = true;
          }
          params.pages.push(page);
        }
        console.log(params);
        var markup = Mustache.render(templates.usersDisplay, params);
        this.trigger("#display", "dataUsersDisplayRendered", {markup: markup});
      }

      this.renderGroupsDisplay = function(ev, data) {
        var params = {"groups": []};
        for (var group in data.response.groups){
          params.groups.push({"groupname": group, "encodedgroupname": encodeURIComponent(group)});
        }
        var markup = Mustache.render(templates.groupsDisplay, params);
        this.trigger("#display", "dataGroupsDisplayRendered", {markup: markup});
      }

      this.renderRestrictionsDisplay = function(ev, data){
        var params = {"restrictions": []};
        for (var restriction in data.response.restrictions){
          params.restrictions.push({
            "restrictionname": restriction,
            "encodedrestrictionname": encodeURIComponent(restriction)
          });
        }
        var markup = Mustache.render(templates.restrictionsDisplay, params);
        this.trigger("#display", "dataRestrictionsDisplayRendered", {markup: markup});
      };

      this.renderUserDisplay = function(ev, data){
        var params = {"groups": []};
        for (var i in data.response["groups"]){
          params.groups.push({
            "groupname": data.response["groups"][i],
            "encodedgroupname": encodeURIComponent(data.response["groups"][i])
          });
        }
        var markup = Mustache.render(templates.userDisplay, params);
        this.trigger("#display", "dataUserDisplayRendered", {markup: markup});
      };

      this.renderGroupDisplay = function(ev, data){
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
        var markup = Mustache.render(templates.groupDisplay, params);
        this.trigger("#display", "dataGroupDisplayRendered", {markup: markup});
      };

      this.renderRestrictionDisplay = function(ev, data){
        var params = {"description": data.response.description.doc};
        var markup = Mustache.render(templates.restrictionDisplay, params);
        this.trigger("#display", "dataRestrictionDisplayRendered", {markup: markup});
      };

      this.after("initialize", function() {
        this.on("dataUsersReceived", this.renderUsersDisplay);
        this.on("dataSearchedUsersReceived", this.renderUsersDisplay);
        this.on("dataGroupsReceived", this.renderGroupsDisplay);
        this.on("dataRestrictionsReceived", this.renderRestrictionsDisplay);
        this.on("dataUserReceived", this.renderUserDisplay);
        this.on("dataGroupReceived", this.renderGroupDisplay);
        this.on("dataRestrictionReceived", this.renderRestrictionDisplay);
      });
    }
  }
);
