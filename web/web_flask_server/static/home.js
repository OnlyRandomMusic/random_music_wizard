
//function connect(){
//    console.log("connect");
//    request('/connect')
//}

function request(route){
    axios.get(route)
      .then(function (response) {
        // handle success
        console.log(response);
        return response;
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
    request('/play');
    refresh();
}

function pause(){
    request('/pause');
    refresh();
}

function next(){
    request('/next');
    refresh();
}

function like(){
    request('/like');
    refresh();
}

function search(){
    content = document.getElementById("search_bar").value;
    document.getElementById("search_bar").value = '';
    request('/search/' + content);
    refresh();
}

function refresh(){
    title = request('/get_title/');
    document.getElementById("paragraph").value = title;
}
