$(document).ready(function(){
    var nofinv = 1;
    $('#id_invoicenumber').addClass('invoice'+' '+nofinv);
    $('#id_invoicestatus').addClass('invoiceadditional'+' '+nofinv);
    $('#id_paidon').addClass('paid'+' '+nofinv);
    $('#id_rejectreason').addClass('reject'+' '+nofinv);
    $("#id_amount").addClass("amount"+" "+nofinv);
    $("#id_currency").addClass("currency"+" "+nofinv);
    $("#id_reasonother").addClass("other"+" "+nofinv);
    $('.addhiddendata:first').find('#id_invoicenumber').attr('id', 'id_invoicenumber'+nofinv);
    $('.addhiddendata:first').find('#id_invoicestatus').attr('id', 'id_invoicestatus'+nofinv);
    $('.addhiddendata:first').find('#id_paidon').attr('id', 'id_paidon'+nofinv);
    $('.addhiddendata:first').find('#id_rejectreason').attr('id', 'id_rejectreason'+nofinv);
    $(".addhiddendata:first").find("#id_amount").attr("id", "id_amount"+nofinv);
    $(".addhiddendata:first").find("#id_currency").attr("id", "id_currency"+nofinv);
    $("#id_reasonother").attr("id", "id_reasonother"+nofinv);
    
    $('#trbutton').on('click', function(){
	$('#trbutton').fadeOut('slow', function(){
	    $('#trform').fadeIn('slow');
	    $('#ptrack').html('Please fill in all the fields.');
	});
    });
    
    $('#id_reminderdate').datepicker({
	dateFormat: 'yy-mm-dd',
	constrainInput: false
    });
    $('.paid:first').datepicker({
	dateFormat: 'yy-mm-dd',
	constrainInput: false
    });
    
    var $name = $('#vclerk').attr('value');
    $('#id_clerk').val($name);
    
    $('#id_clerk').attr('readonly', true);
    $('#id_actiondate').attr('readonly', true);

    $('#id_market').on('change', function(){
	//show the ccode choice if is hidden
	if ($('#id_ccode').is(':hidden')) {$('#id_ccode').show()};

	$('#id_ccode option').each(function(){
	    $(this).show();
	});

	var market = $('#id_market').val();
	if (market == 'IT') {
	    var marketArray = ['', '11', '13', '15', '16'];
	} else if (market == 'DE') {
	    var marketArray = ['', '13', '52', '55', '60', '64', '66'];
	} else if (market == 'PT' || market == 'PL' || market == 'NL' || market == 'NO') {
	    var marketArray = ['', '10'];
	} else if (market == 'BE') {
	    var marketArray = ['', '12', '14', '18', '31'];
	} else if (market == 'SE') {
	    var marketArray = ['', '16'];
	} else if (market == 'FI') {
	    var marketArray = ['', '11'];
	} else if (market == 'DK') {
	    var marketArray = ['', '12'];
	} else {
	    var marketArray = [''];
	}

	$('#id_ccode option').each(function(){
	    var ccodeOpt = $(this).val();	    
	    if ($.inArray(ccodeOpt, marketArray) > -1){
		;
	    } else {
		$(this).hide();
	    }
	});

    });

    $(document).on('change', '.status', function() {
	var status = $(this).val();
	var nextform = $(this).parent().parent().parent().next();

	if (nextform.is(':hidden')){
	    ;
	} else {
	    nextform.hide();
	    if (nextform.find('.paid').is(':hidden')) {nextform.find('.paid').show()};
	    if (nextform.find('.other').is(':hidden')) {nextform.find('.other').show()};
	    if (nextform.find('.reject').is(':hidden')) {nextform.find('.reject').show()};
	    nextform.find('label').show();
	}

	if (status == 'RJ'){
	    nextform.find('.paid').hide();
	    nextform.find('label:last').hide();
	    nextform.fadeIn('slow');
	} else if (status == 'PD') {
	    nextform.find('.reject').hide();
	    nextform.find(".other").hide();
	    nextform.find('label:first').hide();
	    nextform.find('label:first').next().next("label").hide();
	    nextform.fadeIn('slow');
	};
    });

    $('#addbutt').on('click', function() {
	var formToApp = $('.addhiddendata:first').clone();
	formToApp.find('button').remove();
	formToApp.find('.paid').removeClass('hasDatepicker');
	formToApp.find('.paid').val('');
	formToApp.find('#id_invoicenumber1').removeClass('invoice'+' '+nofinv);
	formToApp.find('#id_invoicestatus1').removeClass('invoiceadditional'+' '+nofinv);
	formToApp.find('#id_paidon1').removeClass('paid'+' '+nofinv);
	formToApp.find('#id_rejectreason1').removeClass('reject'+' '+nofinv);
	formToApp.find("#id_amount1").removeClass("amount"+" "+nofinv);
	formToApp.find("#id_currency1").removeClass("currency"+" "+nofinv);
	formToApp.find("#id_reasonother1").removeClass("other"+" "+nofinv);
	nofinv = nofinv + 1;
	formToApp.find('#id_rejectreason1').addClass('reject'+' '+nofinv);
	formToApp.find('#id_rejectreason1').attr('name', 'reject'+nofinv);
	formToApp.find('#id_rejectreason1').attr('id', 'id_rejectreason'+nofinv);
	formToApp.find('#id_paidon1').addClass('paid'+' '+nofinv);
	formToApp.find('#id_paidon1').attr('name', 'paid'+nofinv);
	formToApp.find('#id_paidon1').attr('id', 'id_paidon'+nofinv);
	formToApp.find('#id_invoicenumber1').addClass('invoice'+' '+nofinv);
	formToApp.find('#id_invoicenumber1').attr('name', 'invoicenumber'+nofinv);
	formToApp.find('#id_invoicenumber1').attr('id', 'id_invoicenumber'+nofinv);
	formToApp.find('#id_invoicestatus1').addClass('invoiceadditional'+' '+nofinv);
	formToApp.find('#id_invoicestatus1').attr('name', 'invoicestatus'+nofinv);
	formToApp.find('#id_invoicestatus1').attr('id', 'id_invoicestatus'+nofinv);
	formToApp.find("#id_amount1").addClass("amount"+" "+nofinv);
	formToApp.find("#id_amount1").attr("name", "amount"+nofinv);
	formToApp.find("#id_amount1").attr("id", "id_amount"+nofinv);
	formToApp.find("#id_currency1").addClass("currency"+" "+nofinv);
	formToApp.find("#id_currency1").attr("name", "currency"+nofinv);
	formToApp.find("#id_currency1").attr("id", "id_currency"+nofinv);
	formToApp.find('#id_reasonother1').addClass('other'+' '+nofinv);
	formToApp.find('#id_reasonother1').attr('name', 'reasonother'+nofinv);
	formToApp.find('#id_reasonother1').attr('id', 'id_reasonother'+nofinv);
	$('#vendorform').before(formToApp);
	formToApp.find('.paid').datepicker({
	    dateFormat: 'yy-mm-dd',
	    constrainInput: false
	});
    });

    $('#rembutt').on('click', function() {
	//Remove additional invoices if there are at least 2 of them.
	if ($('.invoice').length == 1) {
	    ;
	} else {
	    $('.addhiddendata:last').remove();
	};
    });

    $('#id_reminderdate').on('change', function() {
	var rdate = $(this).val().split('-');
	var market = $('#id_market').val();
	$('#id_remindernumber').val('');
	$('#id_remindernumber').val(market+rdate[0]+rdate[1]+rdate[2]+'/');
    });

    function DunningTrack() {
	// get the total number of invoices.
	var invo = $('.invoice').length;

	var data = new Array()

	//loop through the invoice to create our data to post
	for (x = 1; x <= invo; x++) {
	    var formn = 'form'+x;
	    var obj = {
		market: $('#id_market').val(),
		ccode: $('#id_ccode').val(),
		clerk: $('#id_clerk').val(),
		actiondate: $('#id_actiondate').val(),
		reminderdate: $('#id_actiondate').val(),
		level: $('#id_level').val(),
		amount: $("#id_amount"+x).val(),
		currency: $("#id_currency"+x).val(),
		remindernumber: $('#id_remindernumber').val(),
		vendor: $('#id_vendor').val(),
		mailvendor: $('#id_mailvendor').val(),
		invoicenumber: $('#id_invoicenumber'+x).val(),
		invoicestatus: $('#id_invoicestatus'+x).val(),
		actiontaken: actionArray(),
		rejectreason: $('#id_rejectreason'+x).val(),
		paidon: $('#id_paidon'+x).val()
		//attachment:
	    };
	    data.push(obj);
	}

	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: 'multi',
		mass_data: JSON.stringify(data)
	    },
	    success: window.location.replace("/main/"),
	    error: function (ajaxObj, textStatus, error) {
		alert(error);
	    }
	});
	return true;
    };

    $('#trackbutton').on('click', ValidateForm);
    $("#trform :input").on("change", function() {
	if ( $(this).val() != "" ) {
	    if ( $(this).parent().parent().hasClass("has-error") ) {
		$(this).parent().parent().removeClass("has-error");
	    }
	}
    });

});

function SuccessfulTracking() {
    alert("Item correctly tracked");
};

function actionArray() {
    var actionPool = $(".actioncheck :input");
    var actionList = new Array()

    $.each(actionPool, function() {
	if ($(this).prop("checked")) {actionList.push($(this).val())}
    });

    actionList = actionList.join(",")
    return actionList;
};

function ValidateForm() {
    error = 0;
    var howManyErrors = $(".has-error").length;
    var fieldsToCheck = ["market", "ccode", "reminderdate", "remindernumber",
			 "level", "vendor", "mailvendor"]
    if ( howManyErrors == 0 ) {
	//checks if some fields are not correctly filled (1st check)
	$.each(fieldsToCheck, function() {
	    if ($("#id_"+this).val() == "") {
		if (! $("#id_"+this).parent().parent().hasClass("has-error")) {
		    $("#id_"+this).parent().parent().addClass("has-error");
		    error++;
		}
	    } else {
		if ($("id_"+this).parent().parent().hasClass(".has-error")) {
		    $("#id_"+this).removeClass("has-error");
		}
	    };
	});
    } else {
	// no errors
	;
    }
    // return the total number of errors
    var errorSum = error + additionalErrorCheck()
    return errorSum
};

function additionalErrorCheck() {
    var error = 0;
    var vendor = $("#id_vendor")
    var mailVendor = $("#id_mailvendor")

    //check if email field is e-mail like
    if ( !isValidEmailAddress(mailVendor.val()) ) {
	if ( !mailVendor.hasClass("has-error") ) { mailVendor.parent().parent().addClass("has-error") }
	error++
    };

    //check if vendor number has 9 characters or if starts with 100 or if there are no characters into the field
    if ( !(vendor.val().length == 9) || !(vendor.val().substr(0, 3) == "100") || !isInteger(vendor.val()) ) {
	if ( ! vendor.hasClass("has-error") ) { vendor.parent().parent().addClass("has-error") }
	error++
    };

    //returns the number of errors
    return error
};

function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
    return pattern.test(emailAddress);
};

function isInteger(value) {
    var intPattern = new RegExp(/^[0-9]+$/)
    return intPattern.test(value);
};
