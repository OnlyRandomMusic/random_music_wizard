var socket = io.connect('http://127.0.0.1:8484');

function play(){
	socket.send('lalala');
}