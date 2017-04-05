var current_preset = 0;
var query1 = "SELECT FirtstName, LastName FROM Users WHERE FirstName = 'Conor' AND LastName = 'Lambert';";
var query2 = "SELECT FirtstName, LastName FROM Users WHERE ( FirstName = 'Conor' AND LastName = 'Lambert' ) OR Age > 20;";
var query3 = "SELECT FirtstName, LastName FROM Users WHERE Level = 'JuniorDeveloper' OR ( College = 'DIT' AND Grade = 'Honors' ) AND Age > 20;"
var presets = [query1,query2,query3];	
	
$(document).ready(function() {	
	$("#query-input").text(presets[current_preset]);	
	$(".chevron-left").on("mousedown", getPreviousPreset);
	$(".chevron-right").on("mousedown", getNextPreset);
	// make arrow keys trigger the above
});

function getNextPreset() {
	current_preset = (current_preset + 1) % presets.length;
	$("#query-input").text(presets[current_preset]);
	setTimeout(function() {
		$('#query-input').focus();
	}, 0);
}

function getPreviousPreset() {
	if(current_preset == 0)
		current_preset = presets.length;
	$("#query-input").text(presets[--current_preset]);
	setTimeout(function() {
		$('#query-input').focus();
	}, 0);
}

