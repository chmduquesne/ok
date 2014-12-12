"use strict";

define(
  [
    "js/app/ui_components/breadcrumbs",
    "js/app/ui_components/display",
    "js/app/data_components/breadcrumbs",
    "js/app/data_components/usersDisplay",
    "js/app/data_components/urlhash"
  ],
  function(
    breadcrumbsUI,
    displayUI,
    breadcrumbsData,
    usersDisplayData,
    urlhashData
    ) {
    function initialize() {
      // first, build the UI components, then launch the data
      breadcrumbsUI.attachTo("#breadcrumbs");
      displayUI.attachTo("#display");
      breadcrumbsData.attachTo(window);
      usersDisplayData.attachTo("#display");
      urlhashData.attachTo(window);
    }
    return initialize;
  }
);
