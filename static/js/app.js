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

}]);