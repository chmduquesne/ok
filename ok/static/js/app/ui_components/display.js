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
        $("#select-all-checkbox")
          .on("change",
            function(ev) {
              var checked = $(this).prop("checked");
              $(".user-select").prop("checked", checked);
            });
        $(":checkbox")
          .on("change", { launcher: this },
            function(ev) {
              var evName = "uiShouldHideUsersDeleteControls";
              if ($(":checkbox:checked").length > 0) {
                evName = "uiShouldShowUsersDeleteControls";
              }
              ev.data.launcher.trigger("#editor", evName);
            });
      };

      this.onGroupsRendered = function(ev, data) {
        this.$node.html(data.markup);
        this.$node
          .find("#select-all-checkbox")
          .on("change", { launcher: this },
            function(ev) {
              var b = $(this).prop("checked");
              $(".group-select").prop("checked", b);
            });
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
