var getTsunamiForecastMapInfo = function () {
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
    [30.01895937888477, 120.75209544783516],
    [45.95879780704559, 156.09067453695047]
]);
var latLngBounds_ogasawara = L.latLngBounds([
    [20.81525687520561, 139.56552841954462],
    [31.90715387478476, 155.35768301846318]
]);
window.map_flash_interval = undefined;
var enable_okinawa_map = false;
var enable_ogasawara_map = false;
var tsunami_map_layer1 = undefined;
var tsunami_map_layer2 = undefined;
var tsunami_map_layer3 = undefined;
var last_message = {};
var is_first_time = true;
var parseMapInfo = function (result) {
    console.debug(result);
    if (is_first_time) {
        setMapInfo(result);
        is_first_time = false;
        last_message = result;
        return;
    }
    if (_.isEqual(last_message, result)) {
        console.debug("Identical information. No need to update.");
        return;
    }
    window.location.reload();
};
var parseTsunamiFCAreas = function (result) {
    window.TSUNAMI_FORECAST_AREAS = [];
    result.forEach(content => {
        window.TSUNAMI_FORECAST_AREAS.push(content.name);
    })
};
var setMapInfo = function (result) {
    var map_result = result["info"]["forecast_areas"];
    if (window.map_flash_interval != undefined) {
        clearInterval(window.map_flash_interval);
    }
    enable_okinawa_map = false;
    deleteAllStrokes();
    if (map_result == undefined) {
        return;
    }
    parseTsunamiFCAreas(map_result);
    if (!(_.isEqual({}, map_result)) && parseInt(result["status_forecast"]) == 1) {
        // Tsunami warning in effect
        document.getElementById("receive-time").innerText = result["info"]["receive_time"];
        var bound_japan = L.latLngBounds();
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer1 = L.geoJson(_GEOJSON_TSUNAMI, {
            pane: "tilePane",
            style: parseMapStyle,
            onEachFeature: function (feature, layer) {
                if (feature.properties.name == "奄美群島・トカラ列島") {
                    layer.options.stroke = false;
                }
                if (latLngBounds_japan_map.contains([layer._bounds._northEast, layer._bounds._southWest])) {
                    bound_japan.extend([layer._bounds._northEast, layer._bounds._southWest]);
                }
                if (window.map_okinawa.getBounds().contains([layer._bounds._northEast, layer._bounds._southWest])) {
                    enable_okinawa_map = true;
                }
                if (latLngBounds_ogasawara.contains([layer._bounds._northEast, layer._bounds._southWest])) {
                    enable_ogasawara_map = true;
                }
            }
        });
        if (enable_okinawa_map) {
            $("#map_okinawa_overlay")[0].style.display = "block";
        } else {
            $("#map_okinawa_overlay")[0].style.display = "none";
        }
        if (enable_ogasawara_map) {
            $("#map_ogasawara_overlay")[0].style.display = "block";
        } else {
            $("#map_ogasawara_overlay")[0].style.display = "none";
        }
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer2 = L.geoJson(_GEOJSON_TSUNAMI, {
            pane: "tilePane",
            style: parseMapStyle
        });
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer3 = L.geoJson(_GEOJSON_TSUNAMI, {
            pane: "tilePane",
            style: parseMapStyle
        });
        tsunami_map_layer1.addTo(window.map_japan);
        tsunami_map_layer2.addTo(window.map_okinawa);
        tsunami_map_layer3.addTo(window.map_ogasawara);
        if (!(bound_japan.getNorthEast() == undefined && bound_japan.getSouthWest() == undefined)) {
            window.map_japan.fitBounds(bound_japan, {padding: [0, 20]});
        } else {
            window.map_japan.fitBounds(latLngBounds_japan_map);
        }
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
    var color = "";
    if (window.TSUNAMI_FORECAST_AREAS.indexOf(feature.properties.name) > 0) {
        color = "#00aaff";
    }
    return {
        stroke: true,
        color: color,
        weight: 5
    }
};
var setMapFlashInterval = function () {
    window.map_flash_interval = setInterval(function () {
        var paths = $(".leaflet-tile-pane");
        for (var i = 0; i < paths.length; i++) {
            paths[i].style.display = "block";
        }
        setTimeout(function () {
            for (var i = 0; i < paths.length; i++) {
                paths[i].style.display = "none";
            }
        }, 3000);
    }, 3500);
};