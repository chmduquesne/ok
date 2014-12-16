"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],
  function(defineComponent){
    return defineComponent(serverData);

    function serverData(){
      this.onDataShouldGetUsers(ev, data){
        $.ajax("/users/", {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUsersReceived", response);
            }
          });
      }
      this.onDataShouldGetUser(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUserReceived", response);
            }
          });
      }
      this.onDataShouldPutUser(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "PUT",
          dataType: "json",
          data: data.userData,
          context: this,
          success: function(response) {
              this.trigger("dataUserUpdated", response);
            }
          });
      }
      this.onDataShouldPostUser(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "POST",
          dataType: "json",
          data: data.userData,
          context: this,
          success: function(response) {
              this.trigger("dataUserCreated", response);
            }
          });
      }
      this.onDataShouldDeleteUser(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "DELETE",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUserDeleted", response);
            }
          });
      }
      this.onDataShouldGetGroups(ev, data){
        $.ajax("/groups/", {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupsReceived", response);
            }
          });
      }
      this.onDataShouldGetGroup(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupReceived", response);
            }
          });
      }
      this.onDataShouldPutGroup(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "PUT",
          dataType: "json",
          data: data.groupData,
          context: this,
          success: function(response) {
              this.trigger("dataGroupUpdated", response);
            }
          });
      }
      this.onDataShouldPostGroup(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "POST",
          dataType: "json",
          data: data.groupData,
          context: this,
          success: function(response) {
              this.trigger("dataGroupCreated", response);
            }
          });
      }
      this.onDataShouldDeleteGroup(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "DELETE",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupDeleted", response);
            }
          });
      }
      this.onDataShouldGetRestrictions(ev, data){
        $.ajax("/restrictions/", {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataRestrictionsReceived", response);
            }
          });
      }
      this.onDataShouldGetRestriction(ev, data){
        $.ajax("/restrictions/" + data.encodedRestrictionName, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataRestrictionReceived", response);
            }
          });
      }
    }
  }
);
