"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "bower_components/flight-with-state/lib/with-state"
  ],

  function(defineComponent, withState){
    return defineComponent(display, withState);

    function display(){

      this.attributes({
        initialView: "multipleUsers"
      });

      this.initialState({
        view: "multipleUsers"
      });

      this.switchToView = function(ev, data){
        views = {
          "uiShouldShowMultipleUsersView": "multipleUsers",
          "uiShouldShowMultipleGroupsView": "multipleGroups",
          "uiShouldShowMultipleRestrictionsView": "multipleRestrictions",
          "uiShouldShowSingleUserView": "singleUser",
          "uiShouldShowSingleGroupView": "singleGroup",
          "uiShouldShowSingleRestrictionView": "singleRestriction"
        };
        dataEvents = {
          "uiShouldShowMultipleUsersView": "dataShouldGetUsers",
          "uiShouldShowMultipleGroupsView": "dataShouldGetGroups",
          "uiShouldShowMultipleRestrictionsView": "dataShouldGetRestriction",
          "uiShouldShowSingleUserView": "dataShouldGetUser",
          "uiShouldShowSingleGroupView": "dataShouldGetGroup",
          "uiShouldShowSingleRestrictionView": "dataShouldGetRestriction"
        }
        this.mergeState({
          view: views[ev]
        });
        this.trigger(dataEvents[ev], data);
      };

      this.onUsersRendered = function(ev, data) {
        if (this.state.view != "multipleUsers"){
          return;
        }
        this.$node.html(data.markup);
        this.$node.find("tr").hover(
            function(){
              $(".btn", this).removeClass("invisible");
            },
            function(){
              $(".btn", this).addClass("invisible");
            }
            );
        this.$node.find(".btn.glyphicon-remove").click(function(){
          var user = $( this ).attr("userid");
          console.log("delete " + user);
        });
      }

      this.after("initialize", function() {
        this.on("uiShouldShowMultipleUsersView", this.switchToView);
        this.on("uiShouldShowMultipleGroupsView", this.switchToView);
        this.on("uiShouldShowMultipleRestrictionsView", this.switchToView);
        this.on("uiShouldShowSingleUserView", this.switchToView);
        this.on("uiShouldShowSingleGroupView", this.switchToView);
        this.on("uiShouldShowSingleRestrictionView", this.switchToView);
        this.on("dataUsersDisplayRendered", this.onUsersRendered);
      });
    }
  }
);
