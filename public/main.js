var app = angular.module('app', ['ui.bootstrap', 'ui.router']);


app.controller('MainCtrl', ['$scope', '$http', function($scope, $http){
	$scope.poop = "POOP POOP POOP POOP";


	$scope.url = '';
	$scope.limit = 50;

	$scope.getDownloadLinks = function(){
		console.log('fuk')
		console.log($scope.url);
		console.log($scope.limit);

		var body = {
			'url': $scope.url,
			'limit': $scope.limit
		};

		// Simple POST request example (passing data) :
		$http.post('/downloads', body).
		  success(function(data, status, headers, config) {
		  	console.log(data);
		    // this callback will be called asynchronously
		    // when the response is available
		  }).
		  error(function(data, status, headers, config) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.
		  });

	}

	$scope.addLimit = function() {
		$scope.limit += 50;
	}

	$scope.subtractLimit = function() {
		$scope.limit -= 50;
	}
}]);