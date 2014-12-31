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

      this.renderUsersEditor = function(ev, data) {
        var params = null;
        var markup = Mustache.render(templates.usersEditor, params);
        this.trigger("#editor", "dataUsersEditorRendered", {markup: markup, search: data.search});
      }

      this.renderGroupsEditor = function(ev, data) {
        var params = null;
        var markup = Mustache.render(templates.groupsEditor, params);
        this.trigger("#editor", "dataGroupsEditorRendered", {markup: markup});
      }

      this.renderRestrictionsEditor = function(ev, data){
        var params = null;
        var markup = Mustache.render(templates.emptyEditor, params);
        this.trigger("#editor", "dataRestrictionsEditorRendered", {markup: markup});
      };

      this.renderUserEditor = function(ev, data){
        var params = null;
        var markup = Mustache.render(templates.userEditor, params);
        this.trigger("#editor", "dataUserEditorRendered", {markup: markup});
      };

      this.renderGroupEditor = function(ev, data){
        var params = null;
        var markup = Mustache.render(templates.groupEditor, params);
        this.trigger("#editor", "dataGroupEditorRendered", {markup: markup});
      };

      this.renderRestrictionEditor = function(ev, data){
        var params = null;
        var markup = Mustache.render(templates.emptyEditor, params);
        this.trigger("#editor", "dataRestrictionEditorRendered", {markup: markup});
      };

      this.after("initialize", function() {
        this.on("dataUsersReceived", this.renderUsersEditor);
        this.on("dataGroupsReceived", this.renderGroupsEditor);
        this.on("dataRestrictionsReceived", this.renderRestrictionsEditor);
        this.on("dataUserReceived", this.renderUserEditor);
        this.on("dataGroupReceived", this.renderGroupEditor);
        this.on("dataRestrictionReceived", this.renderRestrictionEditor);
      });
    }
  }
);
