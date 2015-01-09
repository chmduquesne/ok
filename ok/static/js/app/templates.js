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
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col">                                          \
            <input id="select-all-checkbox" type="checkbox"/>           \
            </th>                                                       \
          <th>username</th>                                             \
          <th>groups</th>                                               \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
      {{#users}}                                                        \
      <tr>                                                              \
        <td>                                                            \
          <input type="checkbox" class="user-select"                    \
                 username="{{encodedusername}}"/>                       \
        </td>                                                           \
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
    {{#pages.length}}                                                   \
    <nav>                                                               \
      <ul class="pagination">                                           \
        <li>                                                            \
          <a href="#/users/{{search}}?page={{first_page}}"              \
             aria-label="First">                                        \
            <span class="glyphicon glyphicon-fast-backward"             \
                  aria-hidden="true">                                   \
            </span>                                                     \
          </a>                                                          \
        </li>                                                           \
        <li>                                                            \
          <a href="#/users/{{search}}?page={{prev_page}}"               \
             aria-label="Previous">                                     \
            <span class="glyphicon glyphicon-step-backward"             \
                  aria-hidden="true">                                   \
            </span>                                                     \
          </a>                                                          \
        </li>                                                           \
        {{#pages}}                                                      \
        <li                                                             \
          {{#active}}class="active"{{/active}}                          \
          >                                                             \
          <a href="#/users/{{search}}?page={{page}}">{{page}}</a>       \
        </li>                                                           \
        {{/pages}}                                                      \
        <li>                                                            \
          <a href="#/users/{{search}}?page={{next_page}}"               \
             aria-label="Next">                                         \
            <span class="glyphicon glyphicon-step-forward"              \
                  aria-hidden="true">                                   \
            </span>                                                     \
          </a>                                                          \
        </li>                                                           \
        <li>                                                            \
          <a href="#/users/{{search}}?page={{last_page}}"               \
             aria-label="Last">                                         \
            <span class="glyphicon glyphicon-fast-forward"              \
                  aria-hidden="true">                                   \
            </span>                                                     \
          </a>                                                          \
        </li>                                                           \
      </ul>                                                             \
    </nav>                                                              \
    {{/pages.length}}                                                   \
    {{/users.length}}                                                   \
    ';

    var groupsDisplay='                                                 \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col">                                          \
            <input id="select-all-checkbox" type="checkbox"/>           \
          </th>                                                         \
          <th>group</th>                                                \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
        {{#groups}}                                                     \
        <tr>                                                            \
          <td>                                                          \
            <input class="group-select"                                 \
                   type="checkbox" groupname={{encodedgroupname}}/>     \
          </td>                                                         \
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
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col">                                          \
            <input id="select-all-checkbox" type="checkbox"/>           \
          </th>                                                         \
          <th>                                                          \
            groups                                                      \
          </th>                                                         \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
      {{#groups}}                                                       \
        <tr>                                                            \
          <td><input class="group-select" type="checkbox"/></td>        \
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
    <p class="text-center">                                             \
      You need to specify restrictions for this group                   \
    </p>                                                                \
    {{/restrictions.length}}                                            \
    {{#restrictions.length}}                                            \
    <table class="table table-striped                                   \
                  table-bordered table-hover">                          \
      <thead>                                                           \
        <tr>                                                            \
          <th class="xxs-col">                                          \
            <input id="select-all-checkbox" type="checkbox"/>           \
          </th>                                                         \
          <th>Path in the url</th>                                      \
          <th>Restriction to apply</th>                                 \
          <th>Parameters of the restriction</th>                        \
        </tr>                                                           \
      </thead>                                                          \
      <tbody>                                                           \
      {{#restrictions}}                                                 \
      <tr>                                                              \
        <td><input class="restriction-select" type="checkbox"/></td>    \
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
      <div class="page-header">                                         \
        <h3>Description</h3>                                            \
      </div>                                                            \
      <pre>{{description}}</pre>                                        \
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
      <div class="spaced">                                              \
        <form id="users-delete-controls" class="form-inline hidden">    \
          <button id="users-delete-button"                              \
            class="btn btn-default"                                     \
            role="button">                                              \
            Delete                                                      \
          </button>                                                     \
          <div class="checkbox">                                        \
            <input id="select-from-filter-checkbox" type="checkbox">    \
              All users matching the active filter                      \
            </input>                                                    \
          </div>                                                        \
        </form>                                                         \
      </div>                                                            \
    ';

    var groupsEditor='                                                  \
      <div class="input-group spaced">                                  \
        <input id="group-add-bar" type="text"                           \
               class="form-control" placeholder="New group">            \
        <span class="input-group-btn">                                  \
          <button id="group-create-button"                              \
                  class="btn btn-default disabled" type="button">       \
            Create                                                      \
          </button>                                                     \
        </span>                                                         \
      </div>                                                            \
    <div class="spaced">                                                \
      <button id="groups-delete-button"                                 \
              class="btn btn-default hidden" role="button">             \
        Delete                                                          \
      </button>                                                         \
    </div>                                                              \
    ';

    var userEditor='                                                    \
      <form class="form-inline spaced">                                 \
        <div class="form-group">                                        \
          <button class="btn btn-default" type="button">                \
            Add in group                                                \
          </button>                                                     \
          <select class="form-control">                                 \
            <option>users</option>                                      \
            <option>unrestricted</option>                               \
          </select>                                                     \
        </div>                                                          \
      </form>                                                           \
      <div class="spaced">                                              \
        <button class="btn btn-default disabled" role="button">         \
          Remove from selected groups                                   \
        </button>                                                       \
      </div>                                                            \
    ';

    var groupEditor='                                                   \
      <form class="form-inline spaced">                                 \
        <form>                                                          \
          <div class="form-group">                                      \
              <button class="btn btn-default" type="button">            \
                Add restriction                                         \
              </button>                                                 \
          </div>                                                        \
          <div class="form-group">                                      \
            <input id="pattern" type="text"                             \
                   class="form-control" placeholder="path pattern">     \
          </div>                                                        \
          <div class="form-group">                                      \
            <select class="form-control">                               \
              <option>unrestricted</option>                             \
              <option>sudoers</option>                                  \
            </select>                                                   \
          <div class="form-group">                                      \
            <input id="pattern" type="text"                             \
                   class="form-control" placeholder="parameters">       \
          </div>                                                        \
          </div>                                                        \
        </form>                                                         \
      </form>                                                           \
      <div class="spaced">                                              \
        <button id="groups-delete-button"                               \
                class="btn btn-default disabled"                        \
                role="button">                                          \
          Remove selected restrictions                                  \
        </button>                                                       \
      </div>                                                            \
      ';

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
