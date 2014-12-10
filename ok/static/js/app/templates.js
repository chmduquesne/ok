"use strict";

define(
  function() {
    var breadcrumbs='{{#path}}<li><a href="{{target}}">{{component}}</a></li>{{/path}}';
    var users='                  \
    {{#users}}                   \
      <tr>                       \
          <td>{{username}}</td>  \
          <td>                   \
          {{#groups}}            \
          {{/groups}}            \
          </td>                  \
      </tr>                      \
    {{/users}}                   \
      <tr>  \
          <td>2</td>  \
          <td>Jacob</td>  \
          <td>Thornton</td>  \
      </tr>  \
      <tr>  \
          <td>3</td>  \
          <td>Larry</td>  \
          <td>the  \
              Bird</td>  \
      </tr>  \
  \
    ';
    return {
      breadcrumbs: breadcrumbs
    }
  }
);
