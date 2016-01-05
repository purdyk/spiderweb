var spiderwebApp = angular.module('spiderwebApp', []);

spiderwebApp.controller('GroupDetailController', [$scope, $routeParams, $http, function($scope, $routeParams) {
  $http.get('groups/phones.json').success(function(data) {
    $scope.reports = data;
  });

  $scope.orderProp = 'age';
});
