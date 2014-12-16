"use strict";

define(
  [
    "js/app/ui_components/breadcrumbs",
    "js/app/ui_components/display",
    "js/app/data_components/breadcrumbs",
    "js/app/data_components/usersMarkup",
    "js/app/data_components/urlhash",
    "js/app/serverData",
  ],
  function(
    breadcrumbsUI,
    displayUI,
    breadcrumbsData,
    usersMarkupData,
    urlhashData,
    serverData
    ) {
    function initialize() {
      // first, build the UI components, then launch the data
      breadcrumbsUI.attachTo("#breadcrumbs");
      displayUI.attachTo("#display");
      breadcrumbsData.attachTo(window);
      usersMarkupData.attachTo("#display");
      urlhashData.attachTo(window);
      serverData.attachTo(window);
    }
    return initialize;
  }
);
