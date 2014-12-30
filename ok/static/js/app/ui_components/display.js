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
        this.$node
          .find("#select-all-checkbox")
          .on("input propertychange", { launcher: this },
            function(ev) {
              /*TODO: check all slaves*/
              $(".user-select");
            });
        this.$node
          .find("#select-from-filter-checkbox")
          .on("input propertychange", { launcher: this },
            function(ev) {
              /*TODO: check all slaves*/
              $(".user-select");
            });
        this.$node
          .find("#delete-user-button")
          .on("click", { launcher: this },
            function(ev) {
              /*TODO: check all slaves*/
              $(".user-select");
              //ev.data.launcher.trigger("");
            });
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
        this.on("dataUsersDisplayRendered", this.onUsersRendered);
        this.on("dataGroupsDisplayRendered", this.onGroupsRendered);
        this.on("dataRestrictionsDisplayRendered", this.onRestrictionsRendered);
        this.on("dataUserDisplayRendered", this.onUserRendered);
        this.on("dataGroupDisplayRendered", this.onGroupRendered);
        this.on("dataRestrictionDisplayRendered", this.onRestrictionRendered);
      });
    }
  }
);
