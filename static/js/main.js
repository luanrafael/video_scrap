$(document).ready(function(){

	$('.modal').modal({
		dismissible: false,
		ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
	        $('#closeVideoModal').removeClass('hide')
      	},
      	complete: function() {
	        $('#closeVideoModal').addClass('hide')

      	}
	});


	update_height($('.login-form-container '));

	window.onresize = function(){
		update_height($('.login-form-container'));
	};
	
})


function update_height(element) {

	var wh = window.innerHeight - 20;

	element.height(wh);
	element.removeClass('hide');


}