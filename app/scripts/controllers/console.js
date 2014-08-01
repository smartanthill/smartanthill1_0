/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

'use strict';

angular.module('siteApp')

.controller('ConsoleCtrl', function($scope, ngTableParams, siteStorage) {
  $scope.tableParams = new ngTableParams({ // jshint ignore:line
    count: -1,
    sorting: {
      id: 'asc'
    }
  }, {
    total: 0,
    counts: [],
    getData: function($defer, params) {
      siteStorage.devices.query(params.url(), function(data) {
        params.total(data.length);
        $defer.resolve(data);
      });
    }
  });
})
