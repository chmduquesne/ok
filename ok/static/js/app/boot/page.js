"use strict";

define(
  [
    "js/app/ui_components/breadcrumbs",
    "js/app/ui_components/display",
    "js/app/data_components/breadcrumbs",
    "js/app/data_components/usersDisplay"
  ],
  function(
    breadcrumbsUI,
    displayUI,
    breadcrumbsData,
    usersDisplayData
    ) {
    function initialize() {
      // first, build the UI components, then launch the data
      breadcrumbsUI.attachTo("#breadcrumbs");
      displayUI.attachTo("#display");
      breadcrumbsData.attachTo(window);
      usersDisplayData.attachTo("#display");
    }
    return initialize;
  }
);
