"use strict";

define(
  [
    "js/app/ui_components/breadcrumbs",
    "js/app/ui_components/display",
    "js/app/data_components/breadcrumbs",
    "js/app/data_components/display",
    "js/app/data_components/urlhash",
    "js/app/serverData",
  ],
  function(
    breadcrumbsUI,
    displayUI,
    breadcrumbsData,
    displayData,
    urlhashData,
    serverData
    ) {
    function initialize() {
      // first, build the UI components, then launch the data
      breadcrumbsUI.attachTo("#breadcrumbs");
      displayUI.attachTo("#display");
      breadcrumbsData.attachTo(window);
      displayData.attachTo(window);
      serverData.attachTo(window);

      // The urlhash is the main trigger, initialize it after everything
      // else is ready and interconnected.
      urlhashData.attachTo(window);
    }
    return initialize;
  }
);
