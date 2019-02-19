
//function post_request(url){
//    var request = new XMLHttpRequest();
//    request.open( "POST", url, false); // false for synchronous request
//    request.send( null );
//}
//
//function get_request(url){
//    var request = new XMLHttpRequest();
//    request.open( "GET", url, false); // false for synchronous request
//    request.send( null );
//    var result = XMLHttpRequest.responseText;
//    console.log(result);
//    return result;
//}

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
    var content = document.getElementById("search_bar").value;
    document.getElementById("search_bar").value = '';
    post_request('/search/' + content);
    refresh();
}

function refresh(){
    post_request('/get_title/', document.getElementById("music_0"))
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

//function post_request(url) {
//    var req = new XMLHttpRequest();
//    req.open('POST', url, true);
//    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
//    req.send( null );
//}

function post_request(url, where_to_post_result) {
    var req = new XMLHttpRequest();

    if (where_to_post_result !== undefined){
        req.onreadystatechange = function()
        {
          if(this.readyState == 4 && this.status == 200) {
            where_to_post_result.innerHTML = this.responseText;
            console.log("response")
          }
        }
    }

    req.open('POST', url, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send( null );
}
