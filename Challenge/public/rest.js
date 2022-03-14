// Get response for object selection
function detectObject(){
    // Get the current index value from the text input box
    let object_name = document.getElementById('object').value;

    // This URL path is going to be the route defined in app.py
    let theURL = '/' + object_name;
    console.log("Making a RESTful request to the server!")

    // Fetch is a Javascript function that sends a request to a server
    console.log(theURL)
    fetch(theURL)
        .then(response => response.json()) // Convert response to JSON

        .then(function (response) {
            console.log(response)
        });

}

// Send request for storing address
function recordAddress() {
    // Get the current index value from the text input box
    let id = document.getElementById('object').value;

    // This URL path is going to be the route defined in app.py
    let theURL = '/record/' + id;
    console.log("Making a RESTful request to the server!")

    // Fetch is a Javascript function that sends a request to a server
    console.log(theURL)
    fetch(theURL)

}