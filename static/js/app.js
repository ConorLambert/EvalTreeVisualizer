var current_preset = 0;
var query1 = "SELECT FirtstName, LastName FROM Users WHERE FirstName = 'Conor' AND LastName = 'Lambert';";
var query2 = "SELECT FirtstName, LastName FROM Users WHERE ( FirstName = 'Conor' AND LastName = 'Lambert' ) OR Age > 20;";
var query3 = "SELECT FirtstName, LastName FROM Users WHERE Level = 'JuniorDeveloper' OR ( College = 'DIT' AND Grade = 'Honors' ) AND Age > 20;"
var presets = [query1,query2,query3];

$(document).ready(function() {
	$('body').keypress(function (e) {
	  if (e.which == 13) {
		$('form').submit();
		return false;    //<---- Add this line
	  }
	});
	$("#query-input").text(presets[current_preset]);
	$(".chevron-left").on("click", getPreviousPreset);
	$(".chevron-right").on("click", getNextPreset);
});

function getNextPreset() {
	current_preset = (current_preset + 1) % presets.length;
	$("#query-input").text(presets[current_preset]);
}

function getPreviousPreset() {
	if(current_preset == 0)
		current_preset = presets.length - 1;
	$("#query-input").text(presets[current_preset]);	
}