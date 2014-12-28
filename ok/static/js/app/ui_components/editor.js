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
          .find("#user-search-bar")
          .on("input propertychange", { launcher: this },
            function(ev) {
              var searchedUser = $("#user-search-bar").val();
              ev.data.launcher.trigger("dataShouldCheckIfUserExists",
                  {encodedUsername: encodeURIComponent(searchedUser)}
              );
            });
        this.$node
          .find("#user-create-button")
          .on("click", { launcher: this },
            function(ev) {
              var username = $("#user-search-bar").val();
              ev.data.launcher.trigger("dataShouldPostUser",
                  {encodedUsername: encodeURIComponent(username)}
              );
            });
      };

      this.onGroupsRendered = function(ev, data) {
        this.$node.html(data.markup);
        this.$node
          .find("#group-add-bar")
          .on("input propertychange", { launcher: this },
            function(ev) {
              var group = $("#group-add-bar").val();
              ev.data.launcher.trigger("dataShouldCheckIfGroupExists",
                  {encodedGroupname: encodeURIComponent(group)}
              );
            });
        this.$node
          .find("#group-create-button")
          .on("click", { launcher: this },
            function(ev) {
              var group = $("#group-add-bar").val();
              ev.data.launcher.trigger("dataShouldPostGroup",
                  {encodedGroupname: encodeURIComponent(group)}
              );
            });
      };

      this.onRestrictionsRendered = function(ev, data){
        this.$node.html(data.markup);
      };

      this.onUserRendered = function(ev, data){
        this.$node.html(data.markup);
      };

      this.onGroupRendered = function(ev, data){
        this.$node.html(data.markup);
      };

      this.onRestrictionRendered = function(ev, data){
        this.$node.html(data.markup);
      };

      this.onUpdateUserCreateButton = function(ev, data){
        if (ev.type == "dataUserDoesNotExist") {
          this.$node.find("#user-create-button").removeClass("disabled");
        }
        if (ev.type == "dataUserExists") {
          this.$node.find("#user-create-button").addClass("disabled");
        }
      };

      this.onUpdateGroupCreateButton = function(ev, data){
        if (ev.type == "dataGroupDoesNotExist") {
          this.$node.find("#group-create-button").removeClass("disabled");
        }
        if (ev.type == "dataGroupExists") {
          this.$node.find("#group-create-button").addClass("disabled");
        }
      };

      this.after("initialize", function() {
        this.on("dataUsersEditorRendered", this.onUsersRendered);
        this.on("dataGroupsEditorRendered", this.onGroupsRendered);
        this.on("dataRestrictionsEditorRendered", this.onRestrictionsRendered);
        this.on("dataUserEditorRendered", this.onUserRendered);
        this.on("dataGroupEditorRendered", this.onGroupRendered);
        this.on("dataRestrictionEditorRendered", this.onRestrictionRendered);
        this.on(window, "dataUserExists", this.onUpdateUserCreateButton);
        this.on(window, "dataUserDoesNotExist", this.onUpdateUserCreateButton);
        this.on(window, "dataGroupExists", this.onUpdateGroupCreateButton);
        this.on(window, "dataGroupDoesNotExist", this.onUpdateGroupCreateButton);
      });
    }
  }
);
