$(document).ready(function() {
    $("#mailbutton").on("click", function() {
	var mailData = $(".mailbody").html();

	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: "mailsend",
		id: $(".mailbody").attr("id"),
		mailbody: JSON.stringify(mailData),
	    },
	    success: window.location.replace("/overview/"),
	    error: function (ajaxObj, textStatus, error) {
		alert(error);
	    }
	});
	return true;
    });
});
