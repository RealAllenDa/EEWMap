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
var current_grade_list = {
    "Advisory": false,
    "Warning": false,
    "MajorWarning": false
};
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
var setMapInfo = function (result) {
    var map_result = result["map"]["areas"];
    if (window.map_flash_interval != undefined) {
        clearInterval(window.map_flash_interval);
    }
    enable_okinawa_map = false;
    deleteAllStrokes();
    if (map_result == undefined) {
        return;
    }
    if (!(_.isEqual({}, map_result)) && parseInt(result["status"]) == 1) {
        // Tsunami warning in effect
        document.getElementById("receive-time").innerText = result["map"]["time"];
        var bound_japan = L.latLngBounds();
        // noinspection JSUnusedGlobalSymbols
        tsunami_map_layer1 = L.geoJson(map_result, {
            style: parseMapStyle,
            onEachFeature: function (feature, layer) {
                var current_area_grade = feature["properties"]["grade"];
                if (current_area_grade == "Watch") {
                    current_grade_list["Advisory"] = true;
                }
                if (current_area_grade == "Warning") {
                    current_grade_list["Warning"] = true;
                }
                if (current_area_grade == "MajorWarning") {
                    current_grade_list["MajorWarning"] = true;
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
        if (!(bound_japan.getNorthEast() == undefined && bound_japan.getSouthWest() == undefined)) {
            window.map_japan.fitBounds(bound_japan, {padding: [0, 20]});
        } else {
            window.map_japan.fitBounds(latLngBounds_japan_map);
        }
        setMapLegends(current_grade_list);
        setMapFlashInterval();
    } else {
        document.getElementById("receive-time").innerText = "XXXX-XX-XX XX:XX";
    }
};
var setMapLegends = function (current_grade_list) {
    var legends_div = $("#legends div");
    var major_legend = legends_div[0];
    var warn_legend = legends_div[1];
    var advisory_legend = legends_div[2];
    major_legend.style.display = "none";
    warn_legend.style.display = "none";
    advisory_legend.style.display = "none";
    if (current_grade_list["Advisory"]) {
        advisory_legend.style.display = "flex";
    }
    if (current_grade_list["Warning"]) {
        warn_legend.style.display = "flex";
    }
    if (current_grade_list["MajorWarning"]) {
        major_legend.style.display = "flex";
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