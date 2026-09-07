// ======================================================
// SLEEPWELL - LOCATION & NEARBY SLEEP CARE
// ======================================================


// ======================================================
// 1. FIND CARE USING CURRENT LOCATION
// ======================================================

function findSleepCare() {

    // Area where messages will be displayed
    const status =
        document.getElementById("location-status");

    // Get ML prediction from result.html
    const condition =
        document.getElementById("sleep-condition").value;


    // Check whether browser supports location
    if (!navigator.geolocation) {

        status.innerHTML =
            "⚠️ Location services are not supported by your browser.";

        return;
    }


    // Tell user that location is being detected
    status.innerHTML =
        "📍 Detecting your current location...";


    // Request location from browser
    navigator.geolocation.getCurrentPosition(

        // ==============================================
        // LOCATION SUCCESS
        // ==============================================

        function(position) {

            const latitude =
                position.coords.latitude;

            const longitude =
                position.coords.longitude;


            // ------------------------------------------
            // SELECT SEARCH BASED ON ML PREDICTION
            // ------------------------------------------

            let searchQuery;


            // INSOMNIA
            if(condition=="Sleep Apnea")
{
    searchQuery="Sleep Disorder Treatment Center";
}

else if(condition=="Insomnia")
{
    searchQuery="Insomnia Treatment Center";
}

else
{
    searchQuery="Sleep Clinic";
}

            // Update message
            status.innerHTML =
                "✅ Location detected. Opening nearby sleep care...";


            // ------------------------------------------
            // CREATE GOOGLE MAPS URL
            // ------------------------------------------

            const mapsURL =
                "https://www.google.com/maps/search/?api=1&query=" +
                encodeURIComponent(
                    searchQuery +
                    " near " +
                    latitude +
                    "," +
                    longitude
                );


            // ------------------------------------------
            // OPEN GOOGLE MAPS
            // ------------------------------------------

            window.open(
                mapsURL,
                "_blank"
            );

        },


        // ==============================================
        // LOCATION ERROR
        // ==============================================

        function(error) {

            // Permission denied
            if (error.code === error.PERMISSION_DENIED) {

                status.innerHTML =
                    "⚠️ Location permission was denied. " +
                    "Please allow location access or enter your city, area or PIN code below.";

            }


            // Location unavailable
            else if (error.code === error.POSITION_UNAVAILABLE) {

                status.innerHTML =
                    "⚠️ Your current location could not be determined. " +
                    "Please enter your city manually.";

            }


            // Location timed out
            else if (error.code === error.TIMEOUT) {

                status.innerHTML =
                    "⚠️ Location request timed out. Please try again.";

            }


            // Other error
            else {

                status.innerHTML =
                    "⚠️ Unable to access your location.";

            }

        },


        // ==============================================
        // LOCATION OPTIONS
        // ==============================================

        {
            enableHighAccuracy: true,

            timeout: 10000,

            maximumAge: 60000
        }

    );

}



// ======================================================
// 2. FIND CARE USING CITY / AREA / PIN CODE
// ======================================================

function searchByCity() {

    // Get location typed by user
    const city =
        document
            .getElementById("city-input")
            .value
            .trim();


    // Get predicted condition
    const condition =
        document
            .getElementById("sleep-condition")
            .value;


    // Message area
    const status =
        document
            .getElementById("location-status");


    // ==============================================
    // CHECK EMPTY INPUT
    // ==============================================

    if (city === "") {

        status.innerHTML =
            "⚠️ Please enter your city, area or PIN code.";

        return;
    }


    // ==============================================
    // SELECT SPECIALIST BASED ON PREDICTION
    // ==============================================

    let searchQuery;


    // INSOMNIA
    if (condition === "Insomnia") {

        searchQuery =
            "sleep clinic insomnia specialist neurologist";

    }


    // SLEEP APNEA
    else if (condition === "Sleep Apnea") {

        searchQuery =
            "Sleep Clinic sleep clinic sleep specialist hospital";

    }


    // HEALTHY
    else {

        searchQuery =
            "sleep clinic sleep specialist hospital";

    }


    // Show search message
    status.innerHTML =
        "🔎 Searching for appropriate sleep care near " +
        city +
        "...";


    // ==============================================
    // CREATE GOOGLE MAPS SEARCH
    // ==============================================

    const mapsURL =
        "https://www.google.com/maps/search/?api=1&query=" +
        encodeURIComponent(
            searchQuery +
            " in " +
            city
        );


    // ==============================================
    // OPEN GOOGLE MAPS
    // ==============================================

    window.open(
        mapsURL,
        "_blank"
    );

}



// ======================================================
// 3. ALLOW ENTER KEY FOR CITY SEARCH
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const cityInput =
            document.getElementById("city-input");


        // Make sure input exists
        if (cityInput) {

            cityInput.addEventListener(
                "keypress",
                function(event) {

                    // User pressed Enter
                    if (event.key === "Enter") {

                        event.preventDefault();

                        searchByCity();

                    }

                }
            );

        }

    }
);