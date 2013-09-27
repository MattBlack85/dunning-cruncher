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
    //populate the field with the values from DB
    changedItem = dataEdit;
    var iid = dataEdit.itemid;

    $('h4').append('<span id="itemid">'+iid+'</span>');
    $('#id_market').val(dataEdit.market);
    $('#id_ccode').show();
    $('#id_ccode').val(dataEdit.ccode);
    $('#dln').val(dataEdit.remindernumber);
    $('#invn').val(dataEdit.invoicenumber);
    $('#id_invoicestatus').val(dataEdit.invoicestatus);
    $('#id_rejectreason').val(dataEdit.rejectreason);
    $('#id_paidon').val(dataEdit.paidon);
    $('#vendm').val(dataEdit.mailvendor);
    $('#vendn').val(dataEdit.vendor);
    $('#id_level').val(dataEdit.level);
    $('#dld').val(dataEdit.reminderdate);
    $('#modalreview').modal();
    $('#dld').datepicker();

    $('#save').on('click', function() {
	var obj = {
	    itemid: $('#itemid').text(),
	    mailvendor: $('#vendm').val(),
	    paidon: $('#id_paidon').val(),
	    vendor: $('#vendn').val(),
	    ccode: $('#id_ccode').val(),
	    market: $('#id_market').val(),
	    remindernumber: $('#dln').val(),
	    invoicenumber: $('#invn').val(),
	    invoicestatus: $('#id_invoicestatus').val(),
	    //actiontaken: $('#id_actiontaken').val(),
	    rejectreason: $('#id_rejectreason').val(),
	    level: $('#id_level').val(),
	    reminderdate: $('#dld').val(),
	    };

	$.each(obj, function(key, value) {
	    if (key !== "success" || key !== "error") {
		if (obj[key] !== changedItem[key]) {
		    changedStuff++;
		};
	    };
	});
	if (changedStuff != 0) {Update(obj)};
    });
};

function Update(item) {
    $.ajaxSetup({
	type: 'POST',
	dataType: 'json'
    });

    //the real AJAX request
    $.ajax({
	url: '/ajax/',
	data: {
	    form_type: 'update',
	    mass_data: JSON.stringify(item)
	},
	success: alert("success"), //todo
	error: function (ajaxObj, textStatus, error) {
	    alert(error);
	}
    });
    return true;
}
