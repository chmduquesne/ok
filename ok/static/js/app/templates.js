"use strict";

define(
  function() {
    var breadcrumbs='                               \
    {{#path}}                                       \
    <li>                                            \
      <a href="{{target}}">{{component}}</a>        \
    </li>                                           \
    {{/path}}';

    var usersMarkup='                               \
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
            <a href="#users/{{encodedusername}}">   \
              {{username}}                          \
            </a>                                    \
          </td>                                     \
          <td>                                      \
          {{#groups}}                               \
            {{^first}}                              \
            ,                                       \
            {{/first}}                              \
            <a href="#groups/{{encodedgroupname}}"> \
            {{groupname}}                           \
            </a>                                    \
          {{/groups}}                               \
            <button                                 \
              userid="{{encodedusername}}"          \
              type="button"                         \
              class="btn btn-default btn-xs         \
                     glyphicon glyphicon-remove     \
                     pull-right invisible"          \
                     title="delete">                \
            </button>                               \
          </td>                                     \
      </tr>                                         \
      {{/users}}                                    \
      <tbody>                                       \
    </table>                                        \
    ';

    var groupsMarkup='                              \
    <table class="table table-striped               \
                  table-bordered table-hover">      \
      <thead>                                       \
          <tr>                                      \
              <th>group</th>                        \
          </tr>                                     \
      </thead>                                      \
      <tbody>                                       \
      {{#groups}}                                   \
      <tr>                                          \
          <td>                                      \
            <a href="#users/{{encodedgroupname}}">  \
              {{groupname}}                         \
            </a>                                    \
            <button                                 \
              groupid="{{encodedgroupname}}"        \
              type="button"                         \
              class="btn btn-default btn-xs         \
                     glyphicon glyphicon-remove     \
                     pull-right invisible"          \
                     title="delete">                \
            </button>                               \
          </td>                                     \
      </tr>                                         \
      {{/groups}}                                   \
      <tbody>                                       \
    </table>                                        \
    ';

    var singleGroupMarkup='                         \
    <table class="table table-striped               \
                  table-bordered table-hover">      \
      <thead>                                       \
          <tr>                                      \
              <th>pattern</th>                      \
              <th>restriction</th>                  \
              <th>parameters</th>                   \
          </tr>                                     \
      </thead>                                      \
      <tbody>                                       \
      {{#rules}}                                    \
      <tr>                                          \
          <td>                                      \
              {{pattern}}                           \
          </td>                                     \
          <td>                                      \
              {{restriction}}                       \
          </td>                                     \
          <td>                                      \
              {{parameters}}                        \
              <button                               \
                groupid="{{encodedgroupname}}"      \
                type="button"                       \
                class="btn btn-default btn-xs       \
                      glyphicon glyphicon-remove    \
                      pull-right invisible"         \
                      title="delete">               \
              </button>                             \
          </td>                                     \
      </tr>                                         \
      {{/rules}}                                    \
      <tbody>                                       \
    </table>                                        \
    ';
    return {
      breadcrumbs: breadcrumbs,
      usersMarkup: usersMarkup,
      groupsMarkup: groupsMarkup
    }
  }
);
