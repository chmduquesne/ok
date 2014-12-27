"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],

  function(defineComponent){
    return defineComponent(display);

    function display(){

      this.onUsersRendered = function(ev, data) {
        this.$node.html(data.markup);
      };

      this.onGroupsRendered = function(ev, data) {
        this.$node.html(data.markup);
      };

      this.onRestrictionsRendered = function(ev, data){
        this.$node.html(data.markup)
      };

      this.onUserRendered = function(ev, data){
        this.$node.html(data.markup)
      };

      this.onGroupRendered = function(ev, data){
        this.$node.html(data.markup)
      };

      this.onRestrictionRendered = function(ev, data){
        this.$node.html(data.markup)
      };

      this.after("initialize", function() {
        this.on("dataUsersEditorRendered", this.onUsersRendered);
        this.on("dataGroupsEditorRendered", this.onGroupsRendered);
        this.on("dataRestrictionsEditorRendered", this.onRestrictionsRendered);
        this.on("dataUserEditorRendered", this.onUserRendered);
        this.on("dataGroupEditorRendered", this.onGroupRendered);
        this.on("dataRestrictionEditorRendered", this.onRestrictionRendered);
      });
    }
  }
);
