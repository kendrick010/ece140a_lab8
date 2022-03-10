// Get response for object selection
function detectObject(){
    // Get the current index value from the text input box
    let id = document.getElementById('object').value;

    // This URL path is going to be the route defined in app.py
    let theURL = '/photos/' + id;
    console.log("Making a RESTful request to the server!")

    console.log(theURL)

    fetch(theURL)
        .then(response=>response.json()) // Convert response to JSON

        .then(function(response) {
            // Set the value of the img_src attribute of the img tag to the value received from the server
            console.log(response)

        });

}