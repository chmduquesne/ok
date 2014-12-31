"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],
  function(defineComponent){

    return defineComponent(serverData);

    function serverData(){

      this.onDataShouldGetUsers = function(ev, data){
        $.ajax("/users/" + data.search + data.page, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUsersReceived",
                  {response: response, search: data.search});
            }
          });
      }

      this.onDataShouldGetUser = function(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUserReceived", {response: response});
            }
          });
      }

      this.onDataShouldPutUser = function(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "PUT",
          dataType: "json",
          data: data.userData,
          context: this,
          success: function(response) {
              this.trigger("dataUserUpdated", {response: response});
            }
          });
      }

      this.onDataShouldPostUser = function(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "POST",
          dataType: "json",
          data: data.userData,
          context: this,
          success: function(response) {
              this.trigger("dataUserCreated", {response: response});
            }
          });
      }

      this.onDataShouldDeleteUser = function(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "DELETE",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUserDeleted", {response: response});
            }
          });
      }

      this.onDataShouldGetGroups = function(ev, data){
        $.ajax("/groups/", {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupsReceived", {response: response});
            }
          });
      }

      this.onDataShouldGetGroup = function(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupReceived", {response: response});
            }
          });
      }

      this.onDataShouldPutGroup = function(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "PUT",
          dataType: "json",
          data: data.groupData,
          context: this,
          success: function(response) {
              this.trigger("dataGroupUpdated", {response: response});
            }
          });
      }

      this.onDataShouldPostGroup = function(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "POST",
          dataType: "json",
          data: data.groupData,
          context: this,
          success: function(response) {
              this.trigger("dataGroupCreated", {response: response});
            }
          });
      }

      this.onDataShouldDeleteGroup = function(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "DELETE",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupDeleted", {response: response});
            }
          });
      }

      this.onDataShouldGetRestrictions = function(ev, data){
        $.ajax("/restrictions/", {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataRestrictionsReceived", {response: response});
            }
          });
      }

      this.onDataShouldGetRestriction = function(ev, data){
        $.ajax("/restrictions/" + data.encodedRestrictionName, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataRestrictionReceived", {response: response});
            }
          });
      }

      this.onDataShouldCheckIfUserExists = function(ev, data){
        $.ajax("/users/" + data.encodedUsername, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataUserExists");
            },
          statusCode: {
            404: function(response) {
                this.trigger("dataUserDoesNotExist");
              }
            }
          });
      }

      this.onDataShouldSearchUsers = function(ev, data){
        console.log("/users/" + data.search + "?page=1");
        $.ajax("/users/" + data.search + "?page=1", {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
            this.trigger("dataSearchedUsersReceived",
              {response: response, search: data.search});
            }
          });
      }

      this.onDataShouldCheckIfGroupExists = function(ev, data){
        $.ajax("/groups/" + data.encodedGroupname, {
          type: "GET",
          dataType: "json",
          context: this,
          success: function(response) {
              this.trigger("dataGroupExists");
            },
          statusCode: {
            404: function(response) {
                this.trigger("dataGroupDoesNotExist");
              }
            }
          });
      }

      this.after("initialize", function() {
        this.on("dataShouldGetUsers", this.onDataShouldGetUsers);
        this.on("dataShouldGetUser", this.onDataShouldGetUser);
        this.on("dataShouldPutUser", this.onDataShouldPutUser);
        this.on("dataShouldPostUser", this.onDataShouldPostUser);
        this.on("dataShouldDeleteUser", this.onDataShouldDeleteUser);
        this.on("dataShouldGetGroups", this.onDataShouldGetGroups);
        this.on("dataShouldGetGroup", this.onDataShouldGetGroup);
        this.on("dataShouldPutGroup", this.onDataShouldPutGroup);
        this.on("dataShouldPostGroup", this.onDataShouldPostGroup);
        this.on("dataShouldDeleteGroup", this.onDataShouldDeleteGroup);
        this.on("dataShouldGetRestrictions", this.onDataShouldGetRestrictions);
        this.on("dataShouldGetRestriction", this.onDataShouldGetRestriction);
        this.on("dataShouldCheckIfUserExists", this.onDataShouldCheckIfUserExists);
        this.on("dataShouldSearchUsers", this.onDataShouldSearchUsers);
        this.on("dataShouldCheckIfGroupExists", this.onDataShouldCheckIfGroupExists);
      });
    }
  }
);
