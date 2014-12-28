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
    <div class="spaced">                                                \
      <form class="form-inline">                                        \
        <button class="btn btn-default disabled" role="button">         \
          Delete                                                        \
        </button>                                                       \
        <div class="checkbox">                                          \
          <input type="checkbox">                                       \
            All users matching the active filter                        \
          </input>                                                      \
        </div>                                                          \
      </form>                                                           \
    </div>                                                              \
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
    <nav>                                                               \
      <ul class="pagination">                                           \
        <li>                                                            \
          <a href="#" aria-label="Previous">                            \
            <span aria-hidden="true">&laquo;</span>                     \
          </a>                                                          \
        </li>                                                           \
        <li><a href="#/users/">1</a></li>                               \
        <li>                                                            \
          <a href="#" aria-label="Next">                                \
            <span aria-hidden="true">&raquo;</span>                     \
          </a>                                                          \
        </li>                                                           \
      </ul>                                                             \
    </nav>                                                              \
    {{/users.length}}                                                   \
    ';

    var groupsDisplay='                                                 \
    <div class="spaced">                                                \
      <button class="btn btn-default disabled" role="button">           \
        Delete                                                          \
      </button>                                                         \
    </div>                                                              \
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
    <div class="spaced">                                                \
      <button class="btn btn-default disabled" role="button">           \
        Remove from selected groups                                     \
      </button>                                                         \
    </div>                                                              \
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
    {{^restrictions.length}}                                            \
    <p class="text-center">This group allows nothing</p>                \
    {{/restrictions.length}}                                            \
    {{#restrictions.length}}                                            \
    <div class="spaced">                                                \
      <button class="btn btn-default disabled" role="button">           \
        Remove                                                          \
      </button>                                                         \
    </div>                                                              \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col"><input type="checkbox"/></th>             \
          <th>Path in the url</th>                                      \
          <th>Restriction to apply</th>                                 \
          <th>Parameters of the restriction</th>                        \
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
    <div class="page-header">                                           \
      <h3>Json hint returned in case of success</h3>                    \
    </div>                                                              \
    <textarea class="form-control spaced">{{hint}}</textarea>           \
    <button class="btn btn-default disabled" role="button">             \
      Modify                                                            \
    </button>                                                           \
    ';

    var restrictionDisplay='                                            \
    <div class="page-header">                                           \
      <h3>Description</h3>                                              \
    </div>                                                              \
    <pre>{{description}}</pre>                                          \
    ';

    var usersEditor='                                                   \
      <div class="input-group spaced">                                  \
        <input id="user-search-bar" type="text"                         \
               class="form-control" placeholder="Filter">               \
        <span class="input-group-btn">                                  \
          <button id="user-create-button"                               \
                  class="btn btn-default disabled" type="button">       \
            Create                                                      \
          </button>                                                     \
        </span>                                                         \
      </div>                                                            \
    ';

    var groupsEditor='                                                  \
      <div class="input-group spaced">                                  \
        <input type="text" class="form-control" placeholder="New group">\
        <span class="input-group-btn">                                  \
          <button class="btn btn-default disabled" type="button">       \
            Create                                                      \
          </button>                                                     \
        </span>                                                         \
      </div><!-- /input-group -->                                       \
    ';

    var userEditor='                                                    \
      <div class="spaced">                                              \
      <form class="form-inline"                                         \
      <div class="form-group">                                          \
        <select class="form-control">                                   \
          <option>users</option>                                        \
          <option>unrestricted</option>                                 \
        </select>                                                       \
        <button class="btn btn-default" type="button">                  \
          Add to group                                                  \
        </button>                                                       \
      </div>                                                            \
      </form>                                                           \
      </div>                                                            \
    ';

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
