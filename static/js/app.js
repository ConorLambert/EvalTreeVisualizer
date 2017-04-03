$(document).ready(function() {
	$('#query-input').keypress(function (e) {
	  if (e.which == 13) {
		$('form').submit();
		return false;    //<---- Add this line
	  }
	});
});