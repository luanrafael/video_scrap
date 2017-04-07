angular.module('videoSpider').controller('videoSpiderController', function($scope, $http) {
	
	$scope.ep = {"title":"", "video": ""};

	$http.get('/getSiders').then(function(response) {

		if(response){

			$scope.spiders = response.data;

		}

	});

	$scope.open_video_modal = function(ep) {

		if($scope.ep !== ep)
			$scope.ep = ep;

		$('#videoModal').modal('open');
	}

	$scope.close_video_modal = function() {
		$('#videoModal').modal('close');
		$('#videoModal')[0].pause()
	}
})