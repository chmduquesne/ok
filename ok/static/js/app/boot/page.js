"use strict";

define(
  [
    "js/app/data_components/breadcrumbs",
    "js/app/ui_components/breadcrumbs"
  ],
  function(
    breadcrumbsData,
    breadcrumbsUI
    ) {
    function initialize() {
      breadcrumbsUI.attachTo(".breadcrumb");
      breadcrumbsData.attachTo(window);
    }
    return initialize;
  }
);
