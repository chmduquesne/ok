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
      breadcrumbsData.attachTo(window);
      breadcrumbsUI.attachTo(".breadcrumb");
    }
    return initialize;
  }
);
