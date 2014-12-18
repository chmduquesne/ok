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
        this.on("dataDisplayUsersRendered", this.onUsersRendered);
        this.on("dataDisplayGroupsRendered", this.onGroupsRendered);
        this.on("dataDisplayRestrictionsRendered", this.onRestrictionsRendered);
        this.on("dataDisplayUserRendered", this.onUserRendered);
        this.on("dataDisplayGroupRendered", this.onGroupRendered);
        this.on("dataDisplayRestrictionRendered", this.onRestrictionRendered);
      });
    }
  }
);
