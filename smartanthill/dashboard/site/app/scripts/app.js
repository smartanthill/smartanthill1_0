/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

'use strict';

angular.module('siteApp', [
  'ngAnimate',
  'ngResource',
  'ngRoute',
  'ngSanitize',
  'ngTouch',
  'ui.bootstrap',
  'ui.select',
  'toaster',
  'ngTable'
])

.constant('siteConfig', {
  apiURL: (parseInt(location.port) === 9000? '//localhost:8138' : '') + '/api/'
})

.config(function($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'views/dashboard.html',
      controller: 'DashboardCtrl'
    })
    .when('/devices/add', {
      templateUrl: 'views/device_addoredit.html',
      controller: 'DeviceAddOrEditCtrl'
    })
    .when('/devices/:deviceId/edit', {
      templateUrl: 'views/device_addoredit.html',
      controller: 'DeviceAddOrEditCtrl'
    })
    .when('/devices/:deviceId', {
      templateUrl: 'views/device_info.html',
      controller: 'DeviceInfoCtrl'
    })
    .when('/devices', {
      templateUrl: 'views/devices.html',
      controller: 'DevicesCtrl'
    })
    .when('/network', {
      templateUrl: 'views/network.html',
      controller: 'NetworkCtrl'
    })
    .when('/console', {
      templateUrl: 'views/console.html',
      controller: 'ConsoleCtrl'
    })
    .when('/settings', {
      templateUrl: 'views/settings.html',
      controller: 'SettingsCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
})

.factory('siteStorage', function($http, $resource, $cacheFactory, siteConfig) {
  $http.defaults.cache = $cacheFactory('api');
  return {
    clearCache: function() {
      $http.defaults.cache.removeAll();
    },
    operations: $resource(siteConfig.apiURL + 'operations'),
    boards: $resource(siteConfig.apiURL  + 'boards/:boardId', {
      boardId: '@id'
    }),
    devices: $resource(siteConfig.apiURL  + 'devices/:deviceId', {
      deviceId: '@id'
    })
  };
})

.controller('SiteController', function($scope, $rootScope, $location) {

  $scope.isRouteActive = function(route) {
    return $location.path().lastIndexOf(route, 0) === 0;
  };

  $scope.$watch(function() {
    return $location.path();
  }, function(path) {
    if (path === '/') {
      path = '/dashboard';
    }
    path = path.substring(1);
    $scope.currentPage = path.substring(0, 1).toUpperCase() + path.substring(1);
  });

});
