
function post_request(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request
    xmlHttp.send( null );
}

function get_request(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request
    xmlHttp.send( null );
    result = xmlHttp.responseText;
    console.log(result);
    return result;
}

function play(){
    post_request('/play/');
    refresh();
}

function pause(){
    post_request('/pause/');
    refresh();
}

function next(){
    post_request('/next/');
    refresh();
}

function like(){
    post_request('/like/');
    refresh();
}

function search(){
    content = document.getElementById("search_bar").value;
    document.getElementById("search_bar").value = '';
    post_request('/search/' + content);
    refresh();
}

function refresh(){
    title = get_request('/get_title/');
//    document.getElementById("paragraph").value = 'rere';
}

// Get the input field
var input = document.getElementById("search_bar");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Cancel the default action, if needed
  event.preventDefault();
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Trigger the button element with a click
    document.getElementById("search_button").click();
  }
});
