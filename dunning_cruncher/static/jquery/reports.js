$(document).ready(function() {
    var rowSaldo = $('.saldo')

    $.each(rowSaldo, function() {
	var index = $(this).index()-1;
	var thiscountrydone = parseInt($('.alldone').eq(index).text().trim());
	var thiscountrytodo = parseInt($('.todo').eq(index).text().trim());

	$(this).text(thiscountrydone-thiscountrytodo);
    });
});
