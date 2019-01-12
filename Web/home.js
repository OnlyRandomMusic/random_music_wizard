
//var socket = io.connect('http://10.57.167.107:8484');
//socket.send('lalala');

function connect(){
	var socket = io.connect('http://10.57.167.107:8484');
}

function play(){
	socket.send('lalala');
}

function other_test(){
    var io = io.emitter({ host: '10.57.167.107', port: 8484 });
    setInterval(function(){
        io.emit('time', new Date);
    }, 5000);
}
