"use strict";

define(
  function() {
    var breadcrumbs='{{#path}}<li><a href="{{target}}">{{component}}</a></li>{{/path}}';
    return {
      breadcrumbs: breadcrumbs
    }
  }
);
