$(document).ready(function(){
    $('table').on('click', 'td', function() {
	// Make the cell editable
	$(this).attr('contentEditable', true);
    });

    $('button').on('click', function() {
	// Get the current addres and split every element into an array
	var path = window.location.pathname.split('/');
	var year = path[2]
	var week = path[3]

	if ( $(this).hasClass('next') ) {
	    var where = parseInt(week)+1
	} else if ( $(this).hasClass('prev') ) {
	    var where = parseInt(week)-1
	} else {
	    alert("Wanna cheat?")
	};

	ChangeWeek(year, where);
    });

    $('td').on('focusout', function() {
	// Make the cell no editable
	$(this).attr('contentEditable', false);

	// Get the value just entered, the class (date) of the item and the relative header
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

function ChangeWeek(actualYear, actualWeek) {
    window.location.replace('/reminders/'+actualYear+'/'+actualWeek+'/')
};
