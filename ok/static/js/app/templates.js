"use strict";

define(
  function() {
    var breadcrumbs='                               \
    {{#path}}                                       \
    <li>                                            \
      <a href="{{target}}">{{component}}</a>        \
    </li>                                           \
    {{/path}}';

    var usersDisplay='                               \
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
    ';

    var groupsDisplay='                              \
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

    var restrictionsDisplay='                                    \
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

    var userDisplay='                                \
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

    var groupDisplay='                                           \
    <p><b>Hint</b></p>                                          \
    <pre>                                                       \
    {{hint}}                                                    \
    </pre>                                                      \
    <hr>                                                        \
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
      restrictionDisplay: restrictionDisplay
    }
  }
);
