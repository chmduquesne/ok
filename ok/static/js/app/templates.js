"use strict";

define(
  function() {
    var breadcrumbs='                                                   \
    {{#path}}                                                           \
    <li>                                                                \
      <a href="{{target}}">{{component}}</a>                            \
    </li>                                                               \
    {{/path}}';

    var navbar = '                                                      \
    <ul class="nav navbar-nav">                                         \
      <li {{#users}}class="active"{{/users}}>                           \
        <a href="#users">Users</a>                                      \
      </li>                                                             \
      <li {{#groups}}class="active"{{/groups}}>                         \
        <a href="#groups">Groups</a>                                    \
      </li>                                                             \
      <li {{#restrictions}}class="active"{{/restrictions}}>             \
        <a href="#restrictions">Restrictions</a>                        \
      </li>                                                             \
    </ul>                                                               \
    ';

    var usersDisplay='                                                  \
    {{^users}}                                                          \
    <p class="text-center">No data</p>                                  \
    {{/users}}                                                          \
    {{#users.length}}                                                   \
    <button class="btn btn-default disabled" role="button">             \
      Delete                                                            \
    </button>                                                           \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col"><input type="checkbox"/></th>             \
          <th>username</th>                                             \
          <th>groups</th>                                               \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
      {{#users}}                                                        \
      <tr>                                                              \
        <td><input type="checkbox"/></td>                               \
        <td>                                                            \
          <a href="#users/{{encodedusername}}">                         \
          {{username}}                                                  \
          </a>                                                          \
        </td>                                                           \
        <td>                                                            \
          {{#groups}}                                                   \
          {{^first}}                                                    \
          ,                                                             \
          {{/first}}                                                    \
          <a href="#groups/{{encodedgroupname}}">                       \
          {{groupname}}                                                 \
          </a>                                                          \
          {{/groups}}                                                   \
        </td>                                                           \
      </tr>                                                             \
      {{/users}}                                                        \
      <tbody>                                                           \
    </table>                                                            \
    {{/users.length}}                                                   \
    ';

    var groupsDisplay='                                                 \
    <button class="btn btn-default disabled" role="button">             \
      Delete                                                            \
    </button>                                                           \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col"><input type="checkbox"/></th>             \
          <th>group</th>                                                \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
        {{#groups}}                                                     \
        <tr>                                                            \
          <td><input type="checkbox"/></td>                             \
          <td>                                                          \
            <a href="#groups/{{encodedgroupname}}">                     \
              {{groupname}}                                             \
            </a>                                                        \
          </td>                                                         \
        </tr>                                                           \
        {{/groups}}                                                     \
      <tbody>                                                           \
    </table>                                                            \
    ';

    var restrictionsDisplay='                                           \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
          <tr>                                                          \
              <th>restriction</th>                                      \
          </tr>                                                         \
      </thead>                                                          \
      <tbody>                                                           \
      {{#restrictions}}                                                 \
      <tr>                                                              \
          <td>                                                          \
            <a href="#restrictions/{{encodedrestrictionname}}">         \
              {{restrictionname}}                                       \
            </a>                                                        \
          </td>                                                         \
      </tr>                                                             \
      {{/restrictions}}                                                 \
      <tbody>                                                           \
    </table>                                                            \
    ';

    var userDisplay='                                                   \
    <button class="btn btn-default disabled" role="button">             \
      Remove                                                            \
    </button>                                                           \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
          <tr>                                                          \
              <th class="xxs-col"><input type="checkbox"/></th>         \
              <th>groups</th>                                           \
          </tr>                                                         \
      </thead>                                                          \
      <tbody>                                                           \
      {{#groups}}                                                       \
        <tr>                                                            \
          <td><input type="checkbox"/></td>                             \
          <td>                                                          \
            <a href="#groups/{{encodedgroupname}}">                     \
            {{groupname}}                                               \
            </a>                                                        \
          </td>                                                         \
        </tr>                                                           \
      {{/groups}}                                                       \
      <tbody>                                                           \
    </table>                                                            \
    ';

    var groupDisplay='                                                  \
    <p><b>Hint</b></p>                                                  \
    <pre>{{hint}}</pre>                                                 \
    <hr>                                                                \
    {{^restrictions.length}}                                            \
    <p class="text-center">This group allows nothing</p>                \
    {{/restrictions.length}}                                            \
    {{#restrictions.length}}                                            \
    <button class="btn btn-default disabled" role="button">             \
      Remove                                                            \
    </button>                                                           \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col"><input type="checkbox"/></th>             \
          <th>pattern</th>                                              \
          <th>restriction</th>                                          \
          <th>parameters</th>                                           \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
      {{#restrictions}}                                                 \
      <tr>                                                              \
        <td><input type="checkbox"/></td>                               \
        <td>                                                            \
          {{pattern}}                                                   \
        </td>                                                           \
        <td>                                                            \
          <a href="#restrictions/{{encodedrestrictionname}}">           \
          {{restrictionname}}                                           \
          </a>                                                          \
        </td>                                                           \
        <td>                                                            \
          {{parameters}}                                                \
        </td>                                                           \
      </tr>                                                             \
      {{/restrictions}}                                                 \
      <tbody>                                                           \
    </table>                                                            \
    {{/restrictions.length}}                                            \
    ';

    var restrictionDisplay='                                            \
    <p><b>Description</b></p>                                           \
    <pre>                                                               \
    {{description}}                                                     \
    </pre>                                                              \
    ';

    var usersEditor='                                                   \
      <div class="input-group">                                         \
        <input type="text" class="form-control" placeholder="Filter">   \
        <span class="input-group-btn">                                  \
          <button class="btn btn-default disabled" type="button">       \
            Create                                                      \
          </button>                                                     \
        </span>                                                         \
      </div><!-- /input-group -->                                       \
      <hr>                                                              \
    ';

    var groupsEditor='                                                  \
      <div class="input-group">                                         \
        <input type="text" class="form-control" placeholder="New group">\
        <span class="input-group-btn">                                  \
          <button class="btn btn-default disabled" type="button">       \
            Create                                                      \
          </button>                                                     \
        </span>                                                         \
      </div><!-- /input-group -->                                       \
      <hr>                                                              \
    ';

    var userEditor='';

    var groupEditor='';

    var emptyEditor='';

    return {
      breadcrumbs: breadcrumbs,
      usersDisplay: usersDisplay,
      groupsDisplay: groupsDisplay,
      restrictionsDisplay: restrictionsDisplay,
      userDisplay: userDisplay,
      groupDisplay: groupDisplay,
      restrictionDisplay: restrictionDisplay,
      navbar: navbar,
      usersEditor: usersEditor,
      groupsEditor: groupsEditor,
      userEditor: userEditor,
      groupEditor: groupEditor,
      emptyEditor: emptyEditor
    }
  }
);
