window.intensity_area_icons = {
    null: new L.divIcon({
        className: "intensity-big intensity-unknown",
        html: "?"
    }),
    "1": new L.divIcon({
        className: "intensity-big intensity-1",
        html: "1"
    }),
    "2": new L.divIcon({
        className: "intensity-big intensity-2",
        html: "2"
    }),
    "3": new L.divIcon({
        className: "intensity-big intensity-3",
        html: "3"
    }),
    "4": new L.divIcon({
        className: "intensity-big intensity-4",
        html: "4"
    }),
    "5-": new L.divIcon({
        className: "intensity-big intensity-5",
        html: "5<div class='intensity-add'>-</div>"
    }),
    "5+": new L.divIcon({
        className: "intensity-big intensity-6",
        html: "5<div class='intensity-add'>+</div>"
    }),
    "6-": new L.divIcon({
        className: "intensity-big intensity-7",
        html: "6<div class='intensity-add'>-</div>"
    }),
    "6+": new L.divIcon({
        className: "intensity-big intensity-8",
        html: "6<div class='intensity-add'>+</div>"
    }),
    "7": new L.divIcon({
        className: "intensity-big intensity-9",
        html: "7"
    }),
    "5?": new L.divIcon({
        className: "intensity-big intensity-5_and_up",
        html: "5<div class='intensity-add'>?</div>"
    })
};
window.intensity_station_icons = {
    null: new L.divIcon({
        className: "intensity-small intensity-unknown",
        html: "?"
    }),
    "1": new L.divIcon({
        className: "intensity-small intensity-1",
        html: "1"
    }),
    "2": new L.divIcon({
        className: "intensity-small intensity-2",
        html: "2"
    }),
    "3": new L.divIcon({
        className: "intensity-small intensity-3",
        html: "3"
    }),
    "4": new L.divIcon({
        className: "intensity-small intensity-4",
        html: "4"
    }),
    "5-": new L.divIcon({
        className: "intensity-small intensity-5",
        html: "5<div class='intensity-add'>-</div>"
    }),
    "5+": new L.divIcon({
        className: "intensity-small intensity-6",
        html: "5<div class='intensity-add'>+</div>"
    }),
    "6-": new L.divIcon({
        className: "intensity-small intensity-7",
        html: "6<div class='intensity-add'>-</div>"
    }),
    "6+": new L.divIcon({
        className: "intensity-small intensity-8",
        html: "6<div class='intensity-add'>+</div>"
    }),
    "7": new L.divIcon({
        className: "intensity-small intensity-9",
        html: "7"
    }),
    "5?": new L.divIcon({
        className: "intensity-small intensity-5_and_up",
        html: "5<div class='intensity-add special-intensity-add'>?</div>"
    })
};
window.epicenter_icon = new L.Icon({
    iconUrl: "../static/image/epicenter.svg",
    iconSize: [40, 40]
});
window.iconGroup = L.featureGroup();
window.epicenterGroup = L.featureGroup(); // Extremely unlikely, but dual epicenters can happen.
window.INTENSITY_COLORS = {
    "0": "#666666",
    "1": "#46646E",
    "2": "#1E6EE6",
    "3": "#00C8C8",
    "4": "#FAFA64",
    "5-": "#FFB400",
    "5+": "#FF7800",
    "5?": "#FFFF00",
    "6-": "#E60000",
    "6+": "#A00000",
    "7": "#960096"
};
var initializeMap = function () {
    window.map = L.map('map', {
        zoomControl: false,
        center: [38.272688535980976, 137],
        zoom: 5,
        maxZoom: 8,
        minZoom: 1.5,
        zoomSnap: 0.01,
        zoomDelta: 0.5
    });
    var attribution = window.map.attributionControl;
    attribution.setPrefix("QuakeMap by AllenDa");
    attribution.addAttribution("Map: Natural Earth | " +
        "Map Data: JMA");
    L.geoJSON(_GEOJSON_COUNTRIES, {
        style: () => {
            return {
                stroke: true,
                fill: true,
                fillColor: "#3a3a3a",
                fillOpacity: 1,
                weight: 1,
                color: "#3a3a3a"
            }
        },
        pane: "tilePane"
    }).addTo(window.map);
    // Background (shapes)
    L.geoJSON(_GEOJSON_JAPAN, {
        style: () => {
            return {
                stroke: false,
                fill: true,
                fillColor: "#3a3a3a",
                fillOpacity: 1
            }
        },
        pane: "tilePane"
    }).addTo(window.map);
    // Borderlines
    window._SUB_AREAS_LAYER = L.geoJSON(_GEOJSON_JAPAN_WITH_SUB_AREAS, {
        style: () => {
            return {
                stroke: true,
                fill: false,
                color: "#565656",
                weight: 0.5
            }
        },
        pane: "tilePane"
    });
    window._PREF_LAYER = L.geoJSON(_GEOJSON_JAPAN, {
        style: () => {
            return {
                stroke: true,
                fill: false,
                color: "#838383",
                weight: 0.5
            }
        },
        pane: "tilePane"
    }).addTo(window.map);
    window.map.on('zoomend', function () {
        if (window.map.getZoom() < 6) {
            if (window.map.hasLayer(window._SUB_AREAS_LAYER)) {
                map.removeLayer(window._SUB_AREAS_LAYER);
            }
        } else {
            if (!map.hasLayer(window._SUB_AREAS_LAYER)) {
                map.addLayer(window._SUB_AREAS_LAYER);
            }
        }
    });
};
var addMapIntensities = function (intensityList) {
    for (var i in intensityList) {
        var intensity = intensityList[i]["intensity"];
        var latitude = intensityList[i]["latitude"];
        var longitude = intensityList[i]["longitude"];
        if (intensityList[i]["is_area"] == true) {
            var layer = L.marker([latitude, longitude], {icon: window.intensity_area_icons[intensity]});
        } else {
            layer = L.marker([latitude, longitude], {icon: window.intensity_station_icons[intensity]});
        }
        if (intensity == "0" || intensity == "1" || intensity == "2" || intensity == "3" || intensity == "4") {
            layer.setZIndexOffset(parseInt(intensity) * 100);
        } else if (intensity == "5-") {
            layer.setZIndexOffset(500);
        } else if (intensity == "5+") {
            layer.setZIndexOffset(600);
        } else if (intensity == "6-") {
            layer.setZIndexOffset(700);
        } else if (intensity == "6+") {
            layer.setZIndexOffset(800);
        } else if (intensity == "7") {
            layer.setZIndexOffset(900);
        } else if (intensity == "5?") {
            layer.setZIndexOffset(450);
        } else {
            layer.setZIndexOffset(0);
        }
        window.iconGroup.addLayer(layer);
    }
    window.map.addLayer(window.iconGroup);
};
var addEpicenter = function (latitude, longitude) {
    var epicenterMarker = L.marker([latitude, longitude], {icon: window.epicenter_icon});
    epicenterMarker.setZIndexOffset(5000000);
    window.epicenterGroup.addLayer(epicenterMarker);
    if (window.epicenterGroup != undefined) {
        window.map.removeLayer(window.epicenterGroup);
    }
    window.map.addLayer(window.epicenterGroup);
};
var deleteAllLayers = function () {
    try {
        if (window.colorMapLayer != undefined) {
            window.colorMapLayer.removeFrom(window.map);
        }
        if (window.iconGroup != undefined) {
            window.iconGroup.clearLayers();
        }
        if (window.epicenterGroup != undefined) {
            window.epicenterGroup.clearLayers();
        }
        if (window.swave_circle != undefined) {
            window.map.removeLayer(window.swave_circle);
        }
        if (window.pwave_circle != undefined) {
            window.map.removeLayer(window.pwave_circle);
        }
    } catch (e) {
        console.error("Failed to remove layers." + e);
    }
};
var parseMapScale = function (isEEW = false) {
    var currentBounds = L.latLngBounds();
    var isBoundsChanged = false;
    if (window.iconGroup != undefined && window.map.hasLayer(window.iconGroup)) {
        console.log("Icon Group Bounds =>", window.iconGroup.getBounds());
        currentBounds.extend(window.iconGroup.getBounds());
        isBoundsChanged = true;
    }
    if (window.colorMapLayer != undefined && window.map.hasLayer(window.colorMapLayer)) {
        console.log("Color Map Bounds =>", window.colorMapLayer.getBounds());
        currentBounds.extend(window.colorMapLayer.getBounds());
        isBoundsChanged = true;
    }
    if (isEEW && isBoundsChanged) {
        currentBounds = currentBounds.pad(-0.85);
    }
    if (window.epicenterGroup != undefined && window.map.hasLayer(window.epicenterGroup)) {
        console.log("Epicenter Bounds =>", window.epicenterGroup.getBounds());
        currentBounds.extend(window.epicenterGroup.getBounds());
    }
    console.log("Final Bounds =>", currentBounds);
    window.map.fitBounds(currentBounds, {padding: [0, 30]});
};
var addMapColoring = function (intensities) {
    areaIntensityToColor(intensities);
    window.colorMapLayer = L.geoJson(_GEOJSON_JAPAN_WITH_SUB_AREAS,
        {
            style: parseColorStyle,
            filter: filterMapColoring,
            pane: "tilePane"
        }
    );
    window.colorMapLayer.addTo(window.map);
};
var areaIntensityToColor = function (intensities) {
    window.mapColoring = {
        "colors": {},
        "areas": []
    };
    for (var i in intensities) {
        window.mapColoring["colors"][i] = window.INTENSITY_COLORS[intensities[i]["intensity"]];
        window.mapColoring["areas"].push(i);
    }
};
var filterMapColoring = function (feature) {
    /**
     * @typedef {Object} feature
     * @property {Object} properties
     * @property {String} intensity_color
     * @property {String} name
     */
    return window.mapColoring["areas"].indexOf(feature.properties.name) != -1;
};
var parseColorStyle = function (feature) {
    /**
     * @typedef {Object} feature
     * @property {Object} properties
     * @property {String} intensity_color
     * @property {String} name
     */
    return {
        fillColor: window.mapColoring["colors"][feature.properties.name],
        fillOpacity: 1.0,
        stroke: true,
        color: "#000000",
        weight: 2
    }
};
var addSWaveCircle = function (epicenter, swave_distance) {
    window.swave_circle = L.circle([epicenter["latitude"], epicenter["longitude"]], swave_distance * 1000, {
        color: "#E65A5A",
        weight: 2,
        opacity: 1,
        fillColor: '#E65A5A',
        fillOpacity: 0.2
    }).addTo(window.map);
    window.swave_circle.bringToFront();
};
var addPWaveCircle = function (epicenter, pwave_distance) {
    window.pwave_circle = L.circle([epicenter["latitude"], epicenter["longitude"]], pwave_distance * 1000, {
        color: "#50A0FA",
        weight: 2,
        opacity: 1,
        fill: false
    }).addTo(window.map);
    window.pwave_circle.bringToFront();
};