var getTsunamiMapInfo = function () {
    $.ajax({
        type: "GET",
        url: "/api/tsunami_info",
        cache: false,
        dataType: "JSON",
        timeout: 3500,
        success: parseMapInfo,
        error: function () {
            console.warn("Failed to retrieve data.");
        }
    });
};
var last_message = {};
var parseMapInfo = function (result) {
    console.debug(result);
    var result_for_compare = result;
    if (_.isEqual(last_message, result_for_compare)) {
        console.debug("Identical information. No need to update.");
        return;
    }
    last_message = result_for_compare;
    console.debug("Updated message. Parsing...");
    var map_result = result["map"]["areas"];
    if (window.map_flash_interval != undefined) {
        clearInterval(window.map_flash_interval);
    }
    deleteAllStrokes();
    if (!(_.isEqual({}, map_result)) && parseInt(result["status"]) == 1) {
        // Tsunami warning in effect
        document.getElementById("receive-time").innerText = result["map"]["time"];
        window.tsunami_map_layer = L.geoJson(map_result, {
            style: parseMapStyle
        });
        window.tsunami_map_layer.addTo(window.map_japan);
        window.tsunami_map_layer.addTo(window.map_okinawa);
        window.tsunami_map_layer.addTo(window.map_ogasawara);
        setMapFlashInterval();
    } else {
        document.getElementById("receive-time").innerText = "XXXX-XX-XX XX:XX";
    }
};
var deleteAllStrokes = function () {
    try {
        // Dumb approach, but it works
        $(".leaflet-interactive").remove();
    } catch (e) {
        console.error("Failed to delete layers. ", e);
    }
};
var parseMapStyle = function (feature) {
     return {
         stroke: true,
         color: feature.properties.intensity_color,
         weight: 4
     }
};
var setMapFlashInterval = function () {
    window.map_flash_interval = setInterval(function () {
        var paths = $(".leaflet-interactive");
        for (var i = 0; i < paths.length; i++) {

        paths[i].style.display = "block";
        }
        setTimeout(function () {
        for (var i = 0; i < paths.length; i++) {

        paths[i].style.display = "none";
        }
        }, 1000);
    }, 1500);
};