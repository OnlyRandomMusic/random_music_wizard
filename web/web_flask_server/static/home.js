
function post_request(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request
    xmlHttp.send( null );
}

function get_request(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, true ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
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
    document.getElementById("paragraph").value = title;
}
