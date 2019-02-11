
//function connect(){
//    console.log("connect");
//    request('/connect')
//}

function request(route){
    axios.get(route)
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
}

function play(){
    request('/play')
}

function pause(){
    request('/pause')
}

function next(){
    request('/next')
}

function like(){
    request('/like')
}

function search(){
    content = document.getElementById("search_bar").value;
    document.getElementById("search_bar").value = '';
    request('/search/' + content)
}
