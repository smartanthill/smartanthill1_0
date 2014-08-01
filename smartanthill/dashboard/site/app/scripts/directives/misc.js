/**
 * Copyright (C) Ivan Kravets <me@ikravets.com>
 * See LICENSE for details.
 */

'use strict';

angular.module('siteApp')

.directive('showFormErrors', function() {
  return {
    restrict: 'A',
    require: '^form',
    link: function(scope, element, attrs, formCtrl) {
      if (attrs.showFormErrors) {
        scope.$watch(function() {
          return scope.$eval(attrs.showFormErrors);
        }, function(newValue, oldValue) {
          element.toggleClass('has-success',
                              oldValue === true && newValue !== true);
          element.toggleClass('has-error', newValue === true);
        });
      } else {
        var oInput = angular.element(element[0].querySelector('[name]'));
        if (!oInput) {
          return;
        }
        var inputName = oInput.attr('name');
        oInput.bind('blur', function() {
          element.toggleClass('has-success', !formCtrl[inputName].$invalid);
          element.toggleClass('has-error', formCtrl[inputName].$invalid);
        });
      }

      scope.$on('form-reset', function() {
        element.removeClass('has-success has-error');
      });
    }
  };
})

.directive('loadingContainer', function() {
  return {
    restrict: 'A',
    scope: false,
    link: function(scope, element, attrs) {
      var loadingLayer = angular.element('<div class="loading"></div>');
      element.append(loadingLayer);
      element.addClass('loading-container');
      scope.$watch(attrs.loadingContainer, function(value) {
        loadingLayer.toggleClass('ng-hide', !value);
      });
    }
  };
});
