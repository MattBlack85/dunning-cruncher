$(document).ready(function() {
    var rowBalance = $('.balance')
    var path = window.location.pathname.split('/')
    var year = path[2]
    var month = path[3]

    $('#monthchoice').val(month);

    $('#repobutton').on('click', function() {
	var market = $('#market').val();
	var ryear = $('#year').val();
	var rfmonth = $('#fmonth').val();
	var rtmonth = $('#tmonth').val();

	window.location.replace('/sreport/'+market+'/'+ryear+'/'+rfmonth+'/'+rtmonth+'/');
    });

    $.each(rowBalance, function() {
	var index = $(this).index()-1;
	var thiscountrydone = parseInt($('.alldone').eq(index).text().trim());
	var thiscountrytodo = parseInt($('.todo').eq(index).text().trim());
	var thiscountrybacklog = parseInt($('.backlog').eq(index).text().trim());

	$(this).text(thiscountrydone-thiscountrytodo);

	if ( parseInt($(this).text()) < 0 ) {
	    $(this).addClass('negative');
	};
    });

    $('#monthchoice,#yearchoice').on('change', function() {
	if ( $(this).attr('id') == 'monthchoice' ) {
	    var cMonth = $(this).val();
	    ChangePeriod(year, cMonth);
	} else if ( $(this).attr('id') == 'yearchoice' ) {
	    var cYear = $(this).val();
	    ChangePeriod(cYear, month);
	} else {
	    alert('Wanna cheat uh?');
	};
    });
});

function ChangePeriod(cYear, cMonth) {
    window.location.replace('/reporting/'+cYear+'/'+cMonth+'/')
};
