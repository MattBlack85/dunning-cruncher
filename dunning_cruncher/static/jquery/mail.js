$(document).ready(function() {
    //make a p element editable
    $("p,td").bind('click', function() {
        $(this).attr('contentEditable', true);
    });

    $("p,td").on("focusout", function() {
	$(this).attr('contentEditable', false);
    });

    $("#mailbuttonvendor").on("click", function() {
	$("#vendormodal").modal();
    });

    $("#efax,#vendorok").on("click", function() {
	//Check which kind of request we are dealing with
	if ( $(this).attr("id") == "vendorok" ) {
	    var sendType = "email";
	    var mailData = $(".mailbody").html();
	} else if ( $(this).attr("id") == "efax" ) {
	    var sendType = "efax";
	    var mailData = $("#efaxentire").html();
	} else {
	    alert("You are trying to cheat me uh?");
	}

	var formdata = new FormData();
	var formbcc = $("#vendorbcc").val().split(",")
	var formcc = $("#vendorcc").val().split(",")

	if ( $("#vendorattach").get(0).files[0] ) {
	    formdata.append('newattach', $("#vendorattach").get(0).files[0]);
	};

	formdata.append('form_type', 'mailsend');
	formdata.append('send_type', sendType);
	formdata.append('id', $(".mailbody").attr("id"));
	formdata.append('mailbody', mailData);
	formdata.append('bcc', formbcc);
	formdata.append('cc', formcc);

	$.ajax({
	    url: '/ajax/',
	    type: 'POST',
	    data: formdata,
	    processData: false,
	    contentType: false,
	    success: function(response) {
		if ( response.success === true ) {
		    vmailSuccess();
		} else {
		    alert(response.error);
		};
	    },
	    error: function (ajaxObj, textStatus, error) {
		alert(error);
	    }
	});
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
	var itemID = $(".mailbody").attr("id");

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
		itemid: JSON.stringify(itemID),
	    },
	    success: function(response){
		if ( response.success === true ) {
		    alert("Mail sent!");
		} else {
		    alert(response.error);
		};
	    },
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

function vmailSuccess() {
    $("#vendormodal").modal("hide");
    alert("Mail sent");
};
