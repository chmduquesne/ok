"use strict";

define(
  function() {
    var breadcrumbs='                        \
    {{#path}}                                \
    <li>                                     \
      <a href="{{target}}">{{component}}</a> \
    </li>                                    \
    {{/path}}';
    var users='                 \
    {{#users}}                  \
      <tr>                      \
          <td>{{username}}</td> \
          <td>                  \
          {{#groups}}           \
          {{#first}}            \
          {{groupname}}         \
          {{/first}}            \
          ,{{groupname}}        \
          {{/groups}}           \
          </td>                 \
      </tr>                     \
    ';
    return {
      breadcrumbs: breadcrumbs
    }
  }
);
