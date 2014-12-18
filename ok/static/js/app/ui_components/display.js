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

      this.onRestrictionsRendered = function(ev, data){ this.$node.html(data.markup) };
      this.onUserRendered = function(ev, data){ this.$node.html(data.markup) };
      this.onGroupRendered = function(ev, data){ this.$node.html(data.markup) };
      this.onRestrictionRendered = function(ev, data){ this.$node.html(data.markup) };

      this.after("initialize", function() {
        this.on("dataUsersRendered", this.onUsersRendered);
        this.on("dataGroupsRendered", this.onGroupsRendered);
        this.on("dataRestrictionsRendered", this.onRestrictionsRendered);
        this.on("dataUserRendered", this.onUserRendered);
        this.on("dataGroupRendered", this.onGroupRendered);
        this.on("dataRestrictionRendered", this.onRestrictionRendered);
      });
    }
  }
);
