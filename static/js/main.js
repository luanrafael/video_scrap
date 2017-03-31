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

	
})