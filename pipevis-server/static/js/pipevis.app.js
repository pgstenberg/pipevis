var app = angular.module('pipevis', []);



app.controller('pipelineCtrl', function($scope, $http, $interval, $sce) {

  $scope.calc_col = function(num_stages){
    if(12 / num_stages > 3){
      return Math.ceil(12 / num_stages);
    }else{
      return 3;
    }
  }

  $scope.test = function(){
    return "<strong>Warning!</strong> {{ notifications.meesage}} <a href='#' class='alert-link'>good</a>";
  }

  $interval(function() {
  $http.get("pipeline/get").success(function(data, status, headers, config) {
    $scope.pipeline = data;
    $scope.pipeline.progress = Math.ceil($scope.pipeline.progress)
  });
  }, 1000);

});


app.directive('notification', function ($compile,$sce) {
  return {
    restrict: 'A',
    replace: true,
    link: function (scope, ele, attrs) {

      scope.$watch(attrs.notification, function(notification) {

        var alertBox = "<div class='alert alert-info' role='alert'>"

        if(notification['type'] != undefined){
          if(notification['type'] == 'WARNING'){
            alertBox = "<div class='alert alert-danger' role='alert'>"
          }else if(notification['type'] == 'ARTIFACT'){
            alertBox = "<div class='alert alert-success' role='alert'>"
          }
        }

        for (var linkKey in notification.links) {
          notification.message = notification.message.replace("{{ " + linkKey + " }}", "<a href='" + notification.links[linkKey]['url'] + "' class='alert-link'>" + notification.links[linkKey]['text'] + "</a>");
        }

        var return_html = alertBox;
        if(notification.title != undefined){
          return_html = return_html + "<strong>" + notification.title + "</strong> ";
        }
        return_html = return_html + notification.message + "</div>";



        ele.html(return_html);
        $compile(ele.contents())(scope);
      });
    }
  };
});
