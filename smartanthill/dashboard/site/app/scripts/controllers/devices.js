/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

'use strict';

angular.module('siteApp')

.controller('DevicesCtrl', function($scope, siteStorage) {
  $scope.devices = siteStorage.devices.query();
})

.controller('DeviceInfoCtrl', function($scope, $routeParams, $location,
  siteStorage, toaster) {
  $scope.operations = siteStorage.operations.query();
  $scope.device = siteStorage.devices.get({
      deviceId: $routeParams.deviceId
    },
    function(data) {
      $scope.board = siteStorage.boards.get({
        boardId: data.boardId
      });
    });

  $scope.deleteDevice = function() {
    if (!window.confirm('Are sure you want to delete this device?')) {
      return false;
    }

    var devId = $scope.device.id;
    $scope.device.$delete()

    .then(function() {
      toaster.pop(
        'success',
        'Device #' + devId,
        'Devices has been successfully deleted!');

      siteStorage.clearCache();
      $location.path('/devices');

    }, function(data) {
      toaster.pop(
        'error', ('An unexpected error occurred when deleteing device (' +
          data.data + ')')
      );
    });
  };

})

.controller('DeviceAddOrEditCtrl', function($q, $scope, $routeParams,
  siteStorage, toaster) {
  $scope.selectBoard = {};
  $scope.editMode = false;
  $scope.prevState = {};
  $scope.operations = siteStorage.operations.query();

  /**
   * Handlers
   */
  $scope.$watch('selectBoard.selected', function(newValue) {
    if (!angular.isObject(newValue)) {
      return;
    }
    $scope.device.boardId = newValue.id;
  });

  $scope.boardGroupBy = function(item) {
    return item.name.substr(0, item.name.indexOf('('));
  };

  $scope.flipDeviceOperIDs = function() {
    var _prevOpIDs = $scope.device.operationIds;
    $scope.device.operationIds = {};
    angular.forEach(_prevOpIDs, function(id) {
      $scope.device.operationIds[id] = true;
    });
  };

  $scope.submitForm = function() {
    if ($scope.device.id !== $scope.prevState.id &&
      usedDevIds[$scope.device.id]) {
      window.alert('This Device ID is already used by another device.');
      return;
    }

    $scope.submitted = true;
    $scope.disableSubmit = true;

    // convert dictionary to array
    var _prevOpIDs = $scope.device.operationIds;
    $scope.device.operationIds = [];
    angular.forEach(_prevOpIDs, function(value, id) {
      $scope.device.operationIds.push(parseInt(id));
    });

    $scope.device.$save()

    .then(function() {
      toaster.pop(
        'success',
        'Device #' + $scope.device.id,
        'Settings has been successfully ' + (
          $scope.editMode ? 'updated' : 'added'));

      $scope.flipDeviceOperIDs();
      $scope.prevState = angular.copy($scope.device);
      $scope.editMode = true;
      siteStorage.clearCache();

    }, function(data) {
      toaster.pop(
        'error', ('An unexpected error occurred when ' + (
            $scope.editMode ? 'updating' : 'adding') + ' settings (' +
          data.data + ')')
      );
      $scope.flipDeviceOperIDs();
    })

    .finally(function() {
      $scope.disableSubmit = false;
    });
  };

  $scope.resetForm = function() {
    angular.copy($scope.prevState, $scope.device);
    $scope.$broadcast('form-reset');
    $scope.submitted = false;
  };

  /* End Handlers block */

  var usedDevIds = {};
  siteStorage.devices.query(function(data) {
    angular.forEach(data, function(item) {
      usedDevIds[item.id] = true;
    });
  });

  if ($routeParams.deviceId) {

    var deferred = $q.defer();
    deferred.promise.then(function() {
      $scope.device = siteStorage.devices.get({
        deviceId: $routeParams.deviceId
      });
      return $scope.device.$promise;
    })
      .then(function() {
        $scope.boards = siteStorage.boards.query();
        return $scope.boards.$promise;
      })
      .then(function() {
        angular.forEach($scope.boards, function(item) {
          if (item.id === $scope.device.boardId) {
            $scope.selectBoard.selected = item;
          }
        });

        $scope.flipDeviceOperIDs();

        $scope.prevState = angular.copy($scope.device);
        $scope.editMode = true;
      });
    deferred.resolve();

  } else {

    $scope.boards = siteStorage.boards.query();
    $scope.device = new siteStorage.devices();

    // default operations
    $scope.device.operationIds = {};
    $scope.device.operationIds[0] = true; // PING
    $scope.device.operationIds[0x89] = true; // LIST_OPERATIONS

    $scope.prevState = angular.copy($scope.device);

  }

});
