$(document).ready(function() {
    $('.mainitems, .secondaryitems').each(function() {
	var cleanclass = $(this).children('td:first').text().replace('/','').trim();
	$(this).addClass(cleanclass);
    });
    $('tr').on('click', function() {
	var num = $(this).children("td:first").text().replace('/', '').trim();
	$('.secondaryitems.' + num).toggle();
    });
});
