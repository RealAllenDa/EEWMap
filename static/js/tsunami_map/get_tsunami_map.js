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
var latLngBounds_japan_map = L.latLngBounds([
    [46.042735653846506, 157.76367187500003],
    [29.113775395114416, 120.41015625000001]
]);
window.map_flash_interval = undefined;
var enable_okinawa_map = false;
var tsunami_map_layer1 = undefined;
var tsunami_map_layer2 = undefined;
var tsunami_map_layer3 = undefined;
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
    setMapInfo(result);
};
var setMapInfo = function (result) {
    var map_result = result["map"]["areas"];
    if (window.map_flash_interval != undefined) {
        clearInterval(window.map_flash_interval);
    }
    enable_okinawa_map = false;
    deleteAllStrokes();
    if (!(_.isEqual({}, map_result)) && parseInt(result["status"]) == 1) {
        // Tsunami warning in effect
        document.getElementById("receive-time").innerText = result["map"]["time"];
        var bound_japan = L.latLngBounds();
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer1 = L.geoJson(map_result, {
            style: parseMapStyle,
            onEachFeature: function (feature, layer) {
                if (latLngBounds_japan_map.contains([layer._bounds._northEast, layer._bounds._southWest])) {
                    bound_japan.extend([layer._bounds._northEast, layer._bounds._southWest]);
                }
                if (window.map_okinawa.getBounds().contains([layer._bounds._northEast, layer._bounds._southWest])) {
                    enable_okinawa_map = true;
                }
            }
        });
        if (enable_okinawa_map) {
            $("#map_okinawa_overlay")[0].style.display = "block";
        } else {
            $("#map_okinawa_overlay")[0].style.display = "none";
        }
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer2 = L.geoJson(map_result, {
            style: parseMapStyle
        });
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer3 = L.geoJson(map_result, {
            style: parseMapStyle
        });
        tsunami_map_layer1.addTo(window.map_japan);
        tsunami_map_layer2.addTo(window.map_okinawa);
        tsunami_map_layer3.addTo(window.map_ogasawara);
        window.map_japan.fitBounds(bound_japan, {padding: [0, 20]});
        setMapFlashInterval();
    } else {
        document.getElementById("receive-time").innerText = "XXXX-XX-XX XX:XX";
    }
};
var deleteAllStrokes = function () {
    try {
        if (tsunami_map_layer1 != undefined) {
            window.map_japan.removeLayer(tsunami_map_layer1);
        }
        if (tsunami_map_layer2 != undefined) {
            window.map_okinawa.removeLayer(tsunami_map_layer2);
        }
        if (tsunami_map_layer3 != undefined) {
            window.map_ogasawara.removeLayer(tsunami_map_layer3);
        }
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