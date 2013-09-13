$(document).ready(function(){
    var nofinv = 1;
    $('#id_invoicenumber').addClass('invoice'+' '+nofinv);
    $('#id_invoicestatus').addClass('invoiceadditional'+' '+nofinv);
    
    $('#trbutton').on('click', function(){
	$('#trbutton').fadeOut('slow', function(){
	    $('#trform').fadeIn('slow');
	    $('#ptrack').html('Please fill in all the fields.');
	});
    });
    
    $('#id_reminderdate').datepicker();
    $('.paid:first').datepicker();
    
    var $name = $('#vclerk').attr('value');
    $('#id_clerk').val($name);
    
    $('#id_clerk').attr('readonly', true);
    $('#id_actiondate').attr('readonly', true);

    $('#id_market').on('change', function(){
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
	    return false;
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
	    if (nextform.find('.reject').is(':hidden')) {nextform.find('.reject').show()};
	    nextform.find('label').show();
	}

	if (status == 'RJ'){
	    nextform.find('.paid').hide();
	    nextform.find('label:last').hide();
	    nextform.fadeIn('slow');
	} else if (status == 'PD') {
	    nextform.find('.reject').hide();
	    nextform.find('label:first').hide();
	    nextform.fadeIn('slow');
	};
    });

    $('#addbutt').on('click', function() {
	if (nofinv == 1) {
	    $('.addhiddendata:first').find('#id_invoicenumber').attr('id', 'id_invoicenumber'+nofinv);
	    $('.addhiddendata:first').find('#id_invoicestatus').attr('id', 'id_invoicestatus'+nofinv);
	}

	var formToApp = $('.addhiddendata:first').clone();
	formToApp.find('button').remove();
	formToApp.find('.paid').removeClass('hasDatepicker');
	formToApp.find('#id_invoicenumber1').removeClass('invoice'+' '+nofinv);
	formToApp.find('#id_invoicestatus1').removeClass('invoiceadditional'+' '+nofinv);
	nofinv = nofinv + 1;
	formToApp.find('.paid').val('');
	formToApp.find('.paid').attr('name', 'paid'+nofinv);
	formToApp.find('.reject').attr('name', 'reject'+nofinv);
	formToApp.find('.paid').attr('id', 'id_paidon'+nofinv);
	formToApp.find('.reject').attr('id', 'id_rejectreason'+nofinv);
	formToApp.find('#id_invoicenumber1').addClass('invoice'+' '+nofinv);
	formToApp.find('#id_invoicenumber1').attr('name', 'invoicenumber'+nofinv);
	formToApp.find('#id_invoicenumber1').attr('id', 'id_invoicenumber'+nofinv);
	formToApp.find('#id_invoicestatus1').addClass('invoiceadditional'+' '+nofinv);
	formToApp.find('#id_invoicestatus1').attr('name', 'invoicestatus'+nofinv);
	formToApp.find('#id_invoicestatus1').attr('id', 'id_invoicestatus'+nofinv);
	$('#vendorform').before(formToApp);
	formToApp.find('.paid').datepicker();
    });

    $('#rembutt').on('click', function() {
	// need to modify if the item is the last, actually is a bug because it's removed as well
	$('.addhiddendata:last').remove();
    });
});
