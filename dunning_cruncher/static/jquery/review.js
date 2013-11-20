$(document).ready(function() {
    $('.draftbutt').on('click', function() {
	var dnum = $(this).parent().parent().next('.secondaryitems').attr('id');
	var mark = $(this).parent().parent().find('td :first').next().text().trim();
	var langSelect = whatLanguage(mark);

	$('#lansel').append('<p attr="hidden">'+dnum+'</p>');

	for (var langKey in langSelect) {
	    if (langSelect.hasOwnProperty(langKey)) {
		var langValue = langSelect[langKey];
		$('#lansel').append('<option val='+langKey+'>'+langValue+'</option>')
	    };
	};

	$('#modalreview2').modal();

	$('#loaddraft').on('click', function() {
	    window.location.replace('/mail/'+dnum+'/'+$('#lansel option:selected').attr('val')+'/');
	});
    });

    $(".glyphicon-ok").on("click", function(event) {
	event.stopPropagation();
	var itemNumber = $(this).parent().parent().attr("class").substr(10)
	var secItems = $(document).find(".secondaryitems."+itemNumber)
	var secondaryIdArray = new Array()

	$.each(secItems, function() {
	    secondaryIdArray.push(this.id)
	});

	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: 'done',
		idarray: JSON.stringify(secondaryIdArray)
	    },
	    success: function(response) {
		if ( response.success === true ) {
		    window.location.replace("/overview/");
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

    $(".glyphicon-remove").on("click", function(event) {
	event.stopPropagation();
	var itemNumber = $(this).parent().parent().attr("class").substr(10)
	var secItems = $(document).find(".secondaryitems."+itemNumber)
	var secondaryIdArray = new Array()

	$.each(secItems, function() {
	    secondaryIdArray.push(this.id)
	});

	//setup the AJAX request
	$.ajaxSetup({
	    type: 'POST',
	    dataType: 'json'
	});

	//the real AJAX request
	$.ajax({
	    url: '/ajax/',
	    data: {
		form_type: 'del_item',
		idarray: JSON.stringify(secondaryIdArray)
	    },
	    success: function(response) {
		if ( response.success === true ) {
		    window.location.replace("/overview/");
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

    $('.mainitems, .secondaryitems').each(function() {
	var cleanclass = $(this).children('td:first').text().replace('/','').trim();
	$(this).addClass(cleanclass);
    });

    $('tr.mainitems').on('click', function() {
	var num = $(this).children("td:first").text().replace('/', '').trim();
	$('.secondaryitems.' + num).toggle();
    });

    $(document).on('click', '.editbutton', function() {
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
    changedStuff = 0;
    var iid = dataEdit.itemid;

    $("#id_paidon").datepicker({dateFormat: 'yyyy-mm-dd'});
    $('h4').append('<span id="itemid">'+iid+'</span>');
    $('#id_market').val(dataEdit.market);
    $('#id_ccode').show();
    $('#id_ccode').val(dataEdit.ccode);
    $('#dln').val(dataEdit.remindernumber);
    $('#invn').val(dataEdit.invoicenumber);
    $('#id_invoicestatus').val(dataEdit.invoicestatus);
    $('#id_rejectreason').val(dataEdit.rejectreason);
    $('#id_paidon').val(dataEdit.paidon);
    $("#id_amount").val(dataEdit.amount);
    $("#id_currency").val(dataEdit.currency);
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
	    paidon: $("#id_paidon").val(),
	    vendor: $('#vendn').val(),
	    ccode: $('#id_ccode').val(),
	    market: $('#id_market').val(),
	    remindernumber: $('#dln').val(),
	    invoicenumber: $('#invn').val(),
	    invoicestatus: $('#id_invoicestatus').val(),
	    amount: $("#id_amount").val(),
	    currency: $("#id_currency").val(),
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
	success: window.location.replace("/overview/"),
	error: function (ajaxObj, textStatus, error) {
	    alert(error);
	}
    });
    return true;
}

function whatLanguage(market) {

    switch(market)
    {
	case "IT":
	var lObj = {IT: "Italian", EN: "English"};
	break;
	case "DE":
	var lObj = {EN: "English", DE: "German"};
	break;
	case "FI":
	var lObj = {EN: "English", FI: "Finnish"};
	break;
	case "SE":
	var lObj = {EN: "English", SE: "Swedish"};
	break;
	case "DK":
	var lObj = {EN: "English", DK: "Danish"};
	break;
	case "CH":
	var lObj = {EN: "English", DE: "German"};
	break;
	case "NO":
	var lObj = {EN: "English"};
	break;
    };

    return lObj;
};
