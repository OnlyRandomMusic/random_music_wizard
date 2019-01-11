
function connect(){
	var socket = io.connect('http://127.0.0.1:6001');
}

function play(){
	socket.send('lalala');
}