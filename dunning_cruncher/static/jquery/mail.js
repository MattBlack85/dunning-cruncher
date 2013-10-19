$(document).ready(function() {
    //make a p element editable
    $("p").bind('dblclick', function() {
        $(this).attr('contentEditable', true);
    });

    $("p").on("focusout", function() {
	$(this).attr('contentEditable', false);
    });

    $("#mailbuttonvendor").on("click", function() {
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

    $("#mailbuttonbuy").on("click", function() {
	$("#buyermod").modal();
    });

    $("#mailbuttonshub").on("click", function() {
	$("#shubmod").modal();
    });

    $("#buyermod").on("click", "button :last",  function() {
	var mailTo = $("#modalmailemail").val();
	var mailData = $("#modalmailbody").html();

	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: "mailsendbuy",
		mailbody: JSON.stringify(mailData),
		mailto: JSON.stringify(mailTo),
	    },
	    //success: window.location.replace("/overview/"),
	    error: function (ajaxObj, textStatus, error) {
		alert(error);
	    }
	});
	return true;
    });

    $("#shubmod").on("click", "button :last",  function() {
	var mailTo = $("#modalmailshub").val();
	var mailData = $("#shubmodalmailbody").html();

	//check if there is any file
	if ( $("#scanattach").get(0).files[0] ) {
	    file = $("#scanattach").get(0).files[0];
	    var formdata = new FormData();
	    formdata.append('form_type', 'shubmail');
	    formdata.append('mailto', mailTo);
	    formdata.append('maildata', mailData);
	    formdata.append('file_upload', file);

	    //the real AJAX request
	    $.ajax({
		url: '/ajax/',
		type: 'POST',
		data: formdata,
		processData: false,
		contentType: false,
		success: alert("Mail sent!"),
		error: function (ajaxObj, textStatus, error) {
		    alert(error);
		}
	    });
	} else {
	    // if not throw an alert
	    alert("You must select a file!");
	};
    });
});
