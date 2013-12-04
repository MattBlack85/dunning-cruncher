$(document).ready(function(){
    $('table').on('click', 'td', function() {
	// Make the cell editable
	$(this).attr('contentEditable', true);
    });

    $('td').on('focusout', function() {
	// Make the cell no editable
	$(this).attr('contentEditable', false);

	// Get the value just entered and the class (date) of the item
	var newVal = $(this).text();
	var itemDate = $(this).attr('class');
	var marketVal = $(this).closest('table').find('th').eq($(this).index()).text();

	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: 'reminders',
		new_value: newVal,
		item_date: itemDate,
		market_val: marketVal,
	    },
	    success: function(response) {
		if ( response.success === true ) {
		    ;
		} else {
		    alert(response.error);
		};
	    },
	    error: function (ajaxObj, textStatus, error) {
		alert(error);
	    }
	});

    });
});
