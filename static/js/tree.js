var radius = 30;	// how big the circle is
var space_mult = 5.0;	// how far apart each node is from one another
var text_px = radius - 10;	// size of the text within the circles
var edge_offset = radius + 20; // offset from the edge of canvas to avoid obscurity
var rh = radius * space_mult;
var rw = radius * space_mult;		
var lineWidth = 2;
var level = 0;
	
var canvas;
var context;
var left_leaf_node;
var right_leaf_node;
var scale;

$(document).ready(function() {
	canvas = document.getElementById('myCanvas');
	context = canvas.getContext('2d');
	context.font = 'italic 40pt Calibri, sans-serif';
});

function plotDiagram(tree_structure) {	
	left_leaf_node = getLeftMostLeaf(tree_structure);
	right_leaf_node = getRightMostLeaf(tree_structure);
	scale = setScale(tree_structure);
	var actual_canvas_width = (right_leaf_node.x * rw) - (left_leaf_node.x * rw);
	canvas.width = (actual_canvas_width * scale) + edge_offset + radius + 30;// * scale;
	canvas.height = window.innerHeight; //(left_leaf_node.y * rh + edge_offset + radius) + 20;  // $('#tree-container').height();
	context.scale(scale, scale);
	context.lineWidth = lineWidth;
	context.strokeStyle = "black";			
	drawDiagram(tree_structure);
	drawConn(tree_structure);
	$("#query").text(presets[current_preset]);
}

	
function getLeftMostLeaf(tree_node) {					
	while(tree_node['children'][0] != undefined) {
		tree_node = tree_node['children'][0];
	}
	return tree_node;
}

function getRightMostLeaf(tree_node) {
	while(tree_node['children'][tree_node['children'].length - 1] != undefined) {
		tree_node = tree_node['children'][tree_node['children'].length - 1];
	}
	return tree_node;
}

function setScale(tree_node) {			
	findMaxLevel(tree_node);					
	var min_levels = 3;
	var scale = 0.9;
	if(level > min_levels) {
		return scale - ((level - min_levels) * 0.2); 
	} else {
		return scale;
	}
}

function findMaxLevel(tree_node) {
	var y = tree_node['y'];		
	setMaxLevel(y);				
	for (var key in tree_node['children']){
		findMaxLevel(tree_node['children'][key]);				
	}
}

function setMaxLevel(y) {
	if(y > level)
		level = y;
}

function drawDiagram(tree_node) {
	var text = tree_node['text'];			
	var x = tree_node['x'];			
	var y = tree_node['y'];		
	setMaxLevel(y);
	if(tree_node['children'].length > 0) {				
		drawOval(x, y);
		for (var key in tree_node['children']){
			drawDiagram(tree_node['children'][key]);				
		}				
	} else {
		drawSquare(x, y, text);
	}
	drawText(x, y, text);
}

	function drawOval(x, y) {			
		context.fillStyle = "red";
		context.beginPath();			  
		context.arc( calculateXPosition(x), calculateYPosition(y), radius, 0, Math.PI * 2);
		context.closePath();
		context.fill();	
		context.stroke();				
	}
	
	function drawSquare(x, y, text) {				
		context.font = "bold " + text_px + "px serif";
		var width = context.measureText(text).width;				
		context.beginPath();
		var padding = 10;
		context.rect((calculateXPosition(x)) - (width/2) - padding, (calculateYPosition(y) - (radius / 2)), width + (padding * 2), text_px + 10);
		context.fillStyle = 'yellow';
		context.fill();
		context.stroke();
	}
	
	function drawText(x, y, text) {
		context.fillStyle = "black"; // font color to write the text with
		context.font = "bold " + text_px + "px serif";
		var width = context.measureText(text).width;
		var height = radius;
		context.fillText(text, (calculateXPosition(x)) - (width/2), (calculateYPosition(y)) + ((height / 2) - (text_px / 2)));
	}

function drawConn(tree_node) {
	var text = tree_node['text'];			
	var x = tree_node['x'];			
	var y = tree_node['y'];
	for (var child in tree_node['children']){
		drawLine(calculateXPosition(x), calculateYPosition(y) + radius, calculateXPosition(tree_node['children'][child]['x']), calculateYPosition(y+1) - radius);				
		drawConn(tree_node['children'][child]);
	}			
}

	function drawLine(startx, starty, endx, endy) {
		context.beginPath();
		context.moveTo(startx, starty);
		context.lineTo(endx, endy);
		context.stroke();
	}
	
// functional operations
function calculateXPosition(x) {
	return x * rw + edge_offset + 10;
}		
function calculateYPosition(y) {
	return y * rh + edge_offset; // + lineWidth;
}
