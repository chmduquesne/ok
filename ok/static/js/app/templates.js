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
      {{#u ers}}                                    \
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
            <a href="#groups/{{encodedgroupname}}"> \
              {{groupname}}                         \
            </a>                                    \
          </td>                                     \
      </tr>                                         \
      {{/groups}}                                   \
      <tbody>                                       \
    </table>                                        \
    ';

    var restrictionsMarkup='                                    \
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

    var userMarkup='                                \
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

    var groupMarkup='                                           \
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

    var restrictionMarkup='                         \
    <p><b>Description</b></p>                       \
    <pre>                                           \
    {{description}}                                 \
    </pre>                                          \
    ';

    return {
      breadcrumbs: breadcrumbs,
      usersMarkup: usersMarkup,
      groupsMarkup: groupsMarkup,
      restrictionsMarkup: restrictionsMarkup,
      userMarkup: userMarkup,
      groupMarkup: groupMarkup,
      restrictionMarkup: restrictionMarkup
    }
  }
);
