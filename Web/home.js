
var socket = io.connect('http://10.57.167.107:8484');
socket.send('lalala');

function connect(){
	var socket = io.connect('127.0.0.1:8484');
}

function play(){
	socket.send('lalala');
}
