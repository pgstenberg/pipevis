var app = angular.module('pipevis', []);



app.controller('pipelineCtrl', function($scope, $http, $interval) {

  $scope.calc_col = function(num_stages){
    if(12 / num_stages > 3){
      return Math.ceil(12 / num_stages);
    }else{
      return 3;
    }
  }

  $interval(function() {
  $http.get("pipeline/get").success(function(data, status, headers, config) {
    $scope.pipeline = data;
    $scope.pipeline.progress = Math.ceil($scope.pipeline.progress)


  });
  }, 1000);

});
