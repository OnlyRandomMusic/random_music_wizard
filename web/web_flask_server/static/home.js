//const axios = require('axios');
//var socket = io.connect('http://10.57.167.107:8484');
//socket.send('lalala');

//var socket = io.connect('http://10.57.167.107:8484');

function connect(){
    console.log("connect");
    axios.get('/you')
      .then(function (response) {
        // handle success
        console.log(response);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
//	var socket = io.connect('http://10.57.167.107:8484');
}

function play(){
//	socket.send('lalala');
}

function other_test(){
//    var io = io.emitter({ host: '10.57.167.107', port: 8484 });
//    setInterval(function(){
//        io.emit('time', new Date);
//    }, 5000);
}

console.log("test");