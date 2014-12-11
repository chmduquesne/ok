"use strict";

define(
  [
    "bower_components/flight/lib/component",
  ],

  function(defineComponent, templates, Mustache){
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
      }

      this.after("initialize", function() {
        this.on("dataUsersDisplayRendered", this.onUsersRendered);
      });
    }
  }
);
