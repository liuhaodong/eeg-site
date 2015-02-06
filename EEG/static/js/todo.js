var req;

// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/loginin/get-list", true);
    req.send(); 
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items
    var list = document.getElementById("grumblr");
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }

    // Parses the XML response to get a list of DOM nodes representing items
    var xmlData = req.responseXML;
    var items = xmlData.getElementsByTagName("item");
//console.log(items)
    // Adds each new todo-list item to the list
    for (var i = 0; i < items.length; ++i) {
        // Parses the item id and text from the DOM
        var id = items[i].getElementsByTagName("id")[0].textContent
        var itemText = items[i].getElementsByTagName("text")[0].textContent
        var dislikecount=items[i].getElementsByTagName("dislikecount")[0].textContent
        var itemdislike=items[i].getElementsByTagName("itemdislike")[0].textContent
        var image=items[i].getElementsByTagName("image")[0].textContent
        var user=items[i].getElementsByTagName("user")[0].textContent
        
        var comments=items[i].getElementsByTagName("comment")
        //var dislikecount=items[i].getElementsByTagName("dislikecount")[0].textContent
        //var dislikecount=items[i].getElementsByTagName("dislikecount")[0].textContent
        // Builds a new HTML list item for the todo-list item
        var newItem = document.createElement("li");
        newItem.innerHTML = '<h2 class="featurette-heading">'+user+':'+itemText+'</h2>'+'Total Dislike: '+dislikecount;
        if(itemdislike=='True'){
        newItem.innerHTML +='Disliked'
        }
        else{newItem.innerHTML +="<a class=\"btn btn-large btn-primary\" href=\"loginin/dislikeitem/" + id+ "\">dislike</a>"        }
       //newItem.innerHTML +="<form method=\"post\" action=\"/loginin/addcomment/"+id+"\"><input type=\"text\" name=\"comment\" placeholder=\"add comment\" class=\"form-control\"><input class=\"btn btn-large btn-primary\" type=\"submit\" value=\"add comment\"></form>"        //console.log(comments)
        newItem.innerHTML +="  <a class=\"btn btn-large btn-primary\" href=\"loginin/addcomment/" + id + "\">add comment</a>" 
        //console.log(comments.length)
        if (comments.length>0){
        for (var j = 0; j < comments.length; ++j) {
        //console.log(comments[j])
        var commenttext=comments[j].getElementsByTagName("commenttext")[0].textContent
        var commentuser=comments[j].getElementsByTagName("commentuser")[0].textContent
        var commenttime=comments[j].getElementsByTagName("commenttime")[0].textContent
        newItem.innerHTML +='<p>'+commenttext+'</p>'+'<small>'+commentuser+'at'+commenttime+'</small>'        }}
       
        
       if (image){
       newItem.innerHTML +='<br>'+'<img src='+image+' width="200px"></img>'
       }
        
        // Adds the todo-list item to the HTML list
        list.appendChild(newItem);
    }
}

// causes the sendRequest function to run every 10 seconds
window.setInterval(sendRequest, 10000);
