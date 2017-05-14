var app = angular.module('videoSpider',['ngRoute']);

app.run(function($rootScope){
	$rootScope.globalData = { body_color : '' }
});

app.config(function($routeProvider) {

	$routeProvider.when('/login', {
		  templateUrl: 'partials/login.html',
		  controller: 'LoginController'
		}).when('/home', {
		  templateUrl: 'partials/home.html',
		  controller: 'videoSpiderController'
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


app.controller('videoSpiderController', ['$scope','$http', function($scope, $http) {
	
	$scope.globalData.body_color = "blue";
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


	$scope.video = {'paused' : false};



   	$scope.ep = {"title":"", "video": ""};

	$http.get('/getSpiders').then(function(response) {

		if(response){

			$scope.spiders = response.data;

		}

	});

	$scope.load_videos = function(index) {

		spider = $scope.spiders[index];
		if(!spider.data || spider.data.length == 0) {
			$http.get("/getSpiders/" + spider.id).then(function(response){
				$scope.spiders[index].data = response.data.data;
			})
		}

	}

	$scope.open_video_modal = function(ep) {

		if($scope.ep !== ep)
			$scope.ep = ep;
		$scope.ep.visited = true;
		$('#videoModal').modal('open');

	}

	$scope.play_pause_video = function() {
		$('#videoModal')[0].paused ? $scope.play_video() : $scope.pause_video();
	}

	$scope.play_video = function(){
		$('#videoModal')[0].play();
		$scope.update_video_status();
	}

	$scope.pause_video = function(){
		$('#videoModal')[0].pause();
		$scope.update_video_status();
	}

	$scope.close_video_modal = function() {
		$('#videoModal').modal('close');
		$('#videoModal')[0].pause();
	}

	var videoElement = $('#videoModal')[0];

	videoElement.addEventListener('play', function(){
		$scope.$apply(function() {
			$scope.update_video_status();
	  	});
	});

	videoElement.addEventListener('pause', function(){
		$scope.$apply(function() {
			$scope.update_video_status();
	  	});
	});

	$scope.update_video_status = function(){
		$scope.video.paused = !$('#videoModal')[0].paused;
		console.log($scope.video.paused);
	}


}]);