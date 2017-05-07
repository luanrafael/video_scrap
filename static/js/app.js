var app = angular.module('videoSpider',['ngRoute','ngVideo']);

app.run(function($rootScope){
	$rootScope.globalData = { body_color : '' }
});

app.config(function($routeProvider) {

	$routeProvider.when('/login', {
		  templateUrl: 'partials/login.html',
		  controller: 'LoginController'
		}).when('/home', {
		  templateUrl: 'partials/home.html'
		}).otherwise({
		  redirectTo: '/login'
		});

});

app.service('utils', function() {

	this.update_height = function(element) {

		var wh = window.innerHeight;

		element.height(wh);
		element.removeClass('hide');

	}

});

app.controller('LoginController', function($scope, $location, utils){
	$scope.globalData.body_color = "blue";
	utils.update_height($('.login-form-container'));
	$('body').addClass('overflow-hidden')

	$scope.login = function() {
		$location.path("/home");
	}

});


app.controller('videoSpiderController', ['$scope','$http', 'video', function($scope, $http, video) {
	

	$('body').removeClass('overflow-hidden')
	$('.collapsible').collapsible();

	$('.modal').modal({
		dismissible: false,
		ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
	        $('#closeVideoModal').removeClass('hide')
      	},
      	complete: function() {
	        $('#closeVideoModal').addClass('hide')

      	}
	});

    document.addEventListener('webkitfullscreenchange', exitHandler, false);
    document.addEventListener('mozfullscreenchange', exitHandler, false);
    document.addEventListener('fullscreenchange', exitHandler, false);
    document.addEventListener('MSFullscreenChange', exitHandler, false);

	function exitHandler(){
	    if (document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement !== null) {
	    	document.querySelector("#videoModal").removeAttribute('controls');
	    }
	}

	$scope.globalData.body_color = "blue";
	$scope.ep = {"title":"", "video": ""};
	$scope.video = {"status" : ""};

	$http.get('/getSiders').then(function(response) {

		if(response){
			$scope.spiders = response.data;
		}


	});

	
	$scope.update_video = function(video_element){
		
		$scope.video.status = video_element.paused ? "play_circle_filled" : "pause_circle_filled"
		console.log($scope.video.status);
	}

	
	$scope.open_video_modal = function(ep) {

		$scope.ep.visited = false;
		// $scope.ep.status = '';
		if($scope.ep !== ep)
		 	$scope.ep = ep;

		// $('#videoModal').modal('open');
		$scope.ep.visited = true;
		$('#videoModal').modal('open');

		video.addSource('mp4', ep.video);
		
	}


	$scope.fullscreen_video = function(){
		

		var videoElement = document.querySelector("#videoModal");
		if (videoElement.requestFullscreen) {
		  videoElement.requestFullscreen();
		} else if (videoElement.mozRequestFullScreen) {
		  videoElement.mozRequestFullScreen();
		} else if (videoElement.webkitRequestFullscreen) {
		  videoElement.webkitRequestFullscreen();
		}

		videoElement.setAttribute('controls', false);

	}

	$scope.close_video_modal = function() {
		$('#videoModal').modal('close');
		$('#videoModal')[0].pause()
		//$scope.ep.status = "pause_circle_filled"
	}
}]);