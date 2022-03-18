// Get response for object selection
function detectObject(){
    // Get the current index value from the text input box
    const object_name = document.getElementById('object').value;
    const coordinate = document.getElementById('coordinate') 
    const city = document.getElementById('city')

    // This URL path is going to be the route defined in app.py
    const theURL = '/object/' + object_name;
    console.log("Making a RESTful request to the server!")

    coordinate.innerHTML = "GPS Coordinate: "
    city.innerHTML = "City: "

    // Fetch is a Javascript function that sends a request to a server
    fetch(theURL)
        .then(response => response.json()) // Convert response to JSON

        .then(function (response) {
            console.log(response)

            // Changes inner HTML to detected object GPS location
            coordinate.innerHTML = "GPS Coordinate: " + response['coordinate']
            city.innerHTML = "City: " + response['city']
        });
}

// Send request for storing address
function recordAddress() {
    // Get the current index value from the text input box
    const object_name = document.getElementById('object').value;

    let coordinate = document.getElementById('coordinate').innerHTML;
    coordinate = coordinate.replace('GPS Coordinate: ', '')

    // This URL path is going to be the route defined in app.py
    const theURL = '/record/' + object_name + '/' + coordinate;
    console.log("Making a RESTful request to the server!")

    fetch(theURL);
}