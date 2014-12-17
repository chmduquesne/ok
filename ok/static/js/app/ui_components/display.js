"use strict";

define(
  [
    "bower_components/flight/lib/component",
    "bower_components/flight-with-state/lib/with-state"
  ],

  function(defineComponent, withState){
    return defineComponent(withState, display);

    function display(){

      this.attributes({
        initialView: "multipleUsers"
      });

      this.initialState({
        view: "multipleUsers"
      });

      this.switchView = function(ev, data){
        var views = {
          "uiShouldShowMultipleUsersView": "multipleUsers",
          "uiShouldShowMultipleGroupsView": "multipleGroups",
          "uiShouldShowMultipleRestrictionsView": "multipleRestrictions",
          "uiShouldShowSingleUserView": "singleUser",
          "uiShouldShowSingleGroupView": "singleGroup",
          "uiShouldShowSingleRestrictionView": "singleRestriction"
        };
        this.mergeState({
          view: views[ev.type]
        });
        this.requestData(ev, data);
      };

      this.requestData = function(ev, data){
        var dataEvents = {
          "uiShouldShowMultipleUsersView": "dataShouldGetUsers",
          "uiShouldShowMultipleGroupsView": "dataShouldGetGroups",
          "uiShouldShowMultipleRestrictionsView": "dataShouldGetRestriction",
          "uiShouldShowSingleUserView": "dataShouldGetUser",
          "uiShouldShowSingleGroupView": "dataShouldGetGroup",
          "uiShouldShowSingleRestrictionView": "dataShouldGetRestriction"
        };
        this.trigger(window, dataEvents[ev.type], data);
      };

      this.onUsersRendered = function(ev, data) {
        console.log(this.state.view);
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
      };

      this.onGroupsRendered = function(ev, data) {
        console.log(this.state.view);
        if (this.state.view != "multipleGroups"){
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
      };

      this.after("initialize", function() {
        this.on(window, "uiShouldShowMultipleUsersView", this.switchView);
        this.on(window, "uiShouldShowMultipleGroupsView", this.switchView);
        this.on(window, "uiShouldShowMultipleRestrictionsView", this.switchView);
        this.on(window, "uiShouldShowSingleUserView", this.switchView);
        this.on(window, "uiShouldShowSingleGroupView", this.switchView);
        this.on(window, "uiShouldShowSingleRestrictionView", this.switchView);
        this.on("dataUsersMarkupRendered", this.onUsersRendered);
        this.on("dataGroupsMarkupRendered", this.onGroupsRendered);
      });
    }
  }
);
