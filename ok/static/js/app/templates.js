"use strict";

define(
  function() {
    var breadcrumbs='                               \
    {{#path}}                                       \
    <li>                                            \
      <a href="{{target}}">{{component}}</a>        \
    </li>                                           \
    {{/path}}';

    var navbar = '                                          \
    <ul class="nav navbar-nav">                             \
      <li {{#users}}class="active"{{/users}}>               \
        <a href="#users">Users</a>                          \
      </li>                                                 \
      <li {{#groups}}class="active"{{/groups}}>             \
        <a href="#groups">Groups</a>                        \
      </li>                                                 \
      <li {{#restrictions}}class="active"{{/restrictions}}> \
        <a href="#restrictions">Restrictions</a>            \
      </li>                                                 \
    </ul>                                                   \
    ';

    var usersDisplay='                              \
    {{^users}}                                      \
    <p class="text-center">No data</p>              \
    {{/users}}                                      \
    {{#users.length}}                               \
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
          </td>                                     \
      </tr>                                         \
      {{/users}}                                    \
      <tbody>                                       \
    </table>                                        \
    {{/users.length}}                               \
    ';

    var groupsDisplay='                             \
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
            <a href="#groups/{{encodedgroupname}}"> \
              {{groupname}}                         \
            </a>                                    \
          </td>                                     \
      </tr>                                         \
      {{/groups}}                                   \
      <tbody>                                       \
    </table>                                        \
    ';

    var restrictionsDisplay='                                   \
    <table class="table table-striped                           \
                  table-bordered table-hover">                  \
      <thead>                                                   \
          <tr>                                                  \
              <th>restriction</th>                              \
          </tr>                                                 \
      </thead>                                                  \
      <tbody>                                                   \
      {{#restrictions}}                                         \
      <tr>                                                      \
          <td>                                                  \
            <a href="#restrictions/{{encodedrestrictionname}}"> \
              {{restrictionname}}                               \
            </a>                                                \
          </td>                                                 \
      </tr>                                                     \
      {{/restrictions}}                                         \
      <tbody>                                                   \
    </table>                                                    \
    ';

    var userDisplay='                               \
    <table class="table table-striped               \
                  table-bordered table-hover">      \
      <thead>                                       \
          <tr>                                      \
              <th>groups</th>                       \
          </tr>                                     \
      </thead>                                      \
      <tbody>                                       \
      {{#groups}}                                   \
      <tr>                                          \
        <td>                                        \
          <a href="#groups/{{encodedgroupname}}">   \
          {{groupname}}                             \
          </a>                                      \
        </td>                                       \
      </tr>                                         \
      {{/groups}}                                   \
      <tbody>                                       \
    </table>                                        \
    ';

    var groupDisplay='                                          \
    <p><b>Hint</b></p>                                          \
    <pre>{{hint}}</pre>                                         \
    <hr>                                                        \
    {{^restrictions.length}}                                    \
    <p class="text-center">This group allows nothing</p>        \
    {{/restrictions.length}}                                    \
    {{#restrictions.length}}                                    \
    <table class="table table-striped                           \
                  table-bordered table-hover">                  \
      <thead>                                                   \
        <tr>                                                    \
          <th>pattern</th>                                      \
          <th>restriction</th>                                  \
          <th>parameters</th>                                   \
        </tr>                                                   \
      </thead>                                                  \
      <tbody>                                                   \
      {{#restrictions}}                                         \
      <tr>                                                      \
        <td>                                                    \
          {{pattern}}                                           \
        </td>                                                   \
        <td>                                                    \
          <a href="#restrictions/{{encodedrestrictionname}}">   \
          {{restrictionname}}                                   \
          </a>                                                  \
        </td>                                                   \
        <td>                                                    \
          {{parameters}}                                        \
        </td>                                                   \
      </tr>                                                     \
      {{/restrictions}}                                         \
      <tbody>                                                   \
    </table>                                                    \
    {{/restrictions.length}}                                    \
    ';

    var restrictionDisplay='                         \
    <p><b>Description</b></p>                       \
    <pre>                                           \
    {{description}}                                 \
    </pre>                                          \
    ';

    return {
      breadcrumbs: breadcrumbs,
      usersDisplay: usersDisplay,
      groupsDisplay: groupsDisplay,
      restrictionsDisplay: restrictionsDisplay,
      userDisplay: userDisplay,
      groupDisplay: groupDisplay,
      restrictionDisplay: restrictionDisplay,
      navbar: navbar
    }
  }
);
