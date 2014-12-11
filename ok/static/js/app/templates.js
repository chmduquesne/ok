"use strict";

define(
  function() {
    var breadcrumbs='                               \
    {{#path}}                                       \
    <li>                                            \
      <a href="{{target}}">{{component}}</a>        \
    </li>                                           \
    {{/path}}';

    var usersDisplay='                              \
    <table class="table table-striped               \
                  table-bordered table-hover">      \
      <thead>                                       \
          <tr>                                      \
              <th>username</th>                     \
              <th>groups</th>                       \
          </tr>                                     \
      </thead>                                      \
      <tbody>                                       \
      {{#users}}                                    \
      <tr>                                          \
          <td>                                      \
            <a href="#users/{{username}}">          \
              {{username}}                          \
            </a>                                    \
          <td>                                      \
          {{#groups}}                               \
            {{^first}}                              \
            ,                                       \
            {{/first}}                              \
            <a href="#groups/{{groupname}}">        \
            {{groupname}}                           \
            </a>                                    \
          {{/groups}}                               \
            <button                                 \
              type="button"                         \
              class="btn btn-default btn-xs         \
                     glyphicon glyphicon-remove     \
                     pull-right"                    \
                     title="delete">                \
            </button>                               \
          </td>                                     \
      </tr>                                         \
      {{/users}}                                    \
      <tbody>                                       \
    </table>                                        \
    ';
    return {
      breadcrumbs: breadcrumbs,
      usersDisplay: usersDisplay
    }
  }
);
