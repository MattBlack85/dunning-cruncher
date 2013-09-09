$(document).ready(function(){
    var nofinv = 1;
    $('#id_invoicenumber').addClass('invoice'+nofinv);
    $('#id_invoicestatus').addClass('invoice'+nofinv);
    
    $('#trbutton').on('click', function(){
	$('#trbutton').fadeOut('slow', function(){
	    $('#trform').fadeIn('slow');
	    $('#ptrack').html('Please fill in all the fields.');
	});
    });
    
    $('#id_reminderdate').datepicker();
    $('#id_paidon').datepicker();
    
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

    $('#id_invoicestatus').on('change', function() {
	var status = $(this).val();

	if ($('#rejpaidform').is(':hidden')){
	    ;
	} else {
	    $('#rejpaidform').hide();
	    if ($('#id_paidon').is(':hidden')) {$('#id_paidon').show()};
	    if ($('#id_rejectreason').is(':hidden')) {$('#id_rejectreason').show()};
	    $('#rejpaidform').find('label').show();
	}

	if (status == 'RJ'){
	    $('#id_paidon').hide();
	    $('#rejpaidform').find('label:last').hide();
	    $('#rejpaidform').fadeIn('slow');
	} else if (status == 'PD') {
	    $('#id_rejectreason').hide();
	    $('#rejpaidform').find('label:first').hide();
	    $('#rejpaidform').fadeIn('slow');
	};
    });
});
