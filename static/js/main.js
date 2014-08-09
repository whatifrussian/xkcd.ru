$(document).ready(function(){ 

	// Figures
	$(".illustration").click(function(e) {
		$(this).parent().toggleClass("active");
	});

	// Spoiler (comment)
	$("#comment_button").click(function(e) {
		$("#comment").toggleClass("active");
		return false;
	});

});
