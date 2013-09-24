$(document).ready(function() {
    $('.mainitems, .secondaryitems').each(function() {
	var cleanclass = $(this).children('td:first').text().replace('/','').trim();
	$(this).addClass(cleanclass);
    });

    $('tr.mainitems').on('click', function() {
	var num = $(this).children("td:first").text().replace('/', '').trim();
	$('.secondaryitems.' + num).toggle();
    });

    $(document).on('click', '.editbutton', function() {
	//need to build an ajax call which will populate the modal with the data from the item
	var objId = parseInt($(this).parent().parent().attr('id'));
	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: 'edit',
		id: objId
	    },
	    success: function(json_data) {
		modalEdit(json_data);
		},
	    error: function (ajaxObj, textStatus, error) {
		alert(error);
	    }
	});
	return true;
    });
});

function modalEdit(dataEdit) {
    var formData = JSON.stringify(dataEdit)
    $('#modbody').text(formData)
    $('#modalreview').modal();
};
