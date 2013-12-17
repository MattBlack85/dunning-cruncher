$(document).ready(function() {
    $('#generate').on('click', function() {
	var mailData = $("#pdf").html();
	
	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});
	
	//the real AJAX request
	$.ajax({
	    url: '/pdfgen/',
	    data: {
		html: JSON.stringify(mailData),
		id: $('.iddiv').attr('id'),
	    },
	    success: function(response) {
		window.location = '/pdf_get/'+response.url+'/';
	    },
	    error: function () {
		alert('error');
	    } 
	});
    });
});
