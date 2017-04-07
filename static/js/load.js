window.onload = function(){
	update_height(document.querySelector('.login-form-container '));

	window.onresize = function(){
		update_height(document.querySelector('.login-form-container'));
	};
}

function update_height(element) {

	var wh = window.innerHeight - 20;

	element.height(wh);
	element.removeClass('hide');


}