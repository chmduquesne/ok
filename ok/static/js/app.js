angular.module("okui", ['ui.bootstrap'])
    .controller("index", ["$scope", function($scope) {
        $scope.message = "Hello World";
    }]);
