//HERE IS THE CODE RELATIVE TO THE FRONT ANIMATION

// to activate search bar on enter pressed :
// Get the input field
var input = document.getElementById("search_bar");

// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
    // Cancel the default action, if needed
    event.preventDefault();

    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        search();
    }

    adjust_size(input);
});

input.addEventListener("keydown", function(event){
    adjust_size(input);
});

function adjust_size(element) {
    function f(x) {
        var y = 800 / (x + 5);
        if(y>13){
            return y;
        }
        return 14;
    }

    var new_size;

    if(element.value.length == 0){
        new_size = f(8);
    }else{
        new_size = f(element.value.length);
    }
    
    element.style.fontSize = new_size +'px';

    // console.log(String(input.style.fontSize));
    // console.log(String(input.value.length));
}

adjust_size(input);

//HERE IS THE CODE RELATIVE TO THE COMMUNICATION WITH THE BACKEND

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

function volume_up(){
    post_request('/volume_up/');
    refresh();
}

function volume_down(){
    post_request('/volume_down/');
    refresh();
}

function refresh(){
    post_request('/get_title/', document.getElementById("music_0"));
}

//post request function
function post_request(url, where_to_post_result) {
    var req = new XMLHttpRequest();

    if (where_to_post_result !== undefined){
        req.onreadystatechange = function()
        {
          if(this.readyState == 4 && this.status == 200) {
            where_to_post_result.innerHTML = this.responseText;
            console.log("response");
          }
        }
    }

    req.open('POST', url, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.send( null );
}
