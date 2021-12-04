window.intensity_area_icons = {
    null: new L.Icon({
        iconUrl: "../static/image/intensity_big/0.png",
        iconSize: [25, 25]
    }),
    "1": new L.Icon({
        iconUrl: "../static/image/intensity_big/1.png",
        iconSize: [25, 25]
    }),
    "2": new L.Icon({
        iconUrl: "../static/image/intensity_big/2.png",
        iconSize: [25, 25]
    }),
    "3": new L.Icon({
        iconUrl: "../static/image/intensity_big/3.png",
        iconSize: [25, 25]
    }),
    "4": new L.Icon({
        iconUrl: "../static/image/intensity_big/4.png",
        iconSize: [25, 25]
    }),
    "5-": new L.Icon({
        iconUrl: "../static/image/intensity_big/5-.png",
        iconSize: [25, 25]
    }),
    "5+": new L.Icon({
        iconUrl: "../static/image/intensity_big/5+.png",
        iconSize: [25, 25]
    }),
    "6-": new L.Icon({
        iconUrl: "../static/image/intensity_big/6-.png",
        iconSize: [25, 25]
    }),
    "6+": new L.Icon({
        iconUrl: "../static/image/intensity_big/6+.png",
        iconSize: [25, 25]
    }),
    "7": new L.Icon({
        iconUrl: "../static/image/intensity_big/7.png",
        iconSize: [25, 25]
    }),
    "5?": new L.Icon({
        iconUrl: "../static/image/intensity_big/5_.png",
        iconSize: [25, 25]
    })
};
window.intensity_station_icons = {
    null: new L.Icon({
        iconUrl: "../static/image/intensity_small/0.png",
        iconSize: [20, 20]
    }),
    "1": new L.Icon({
        iconUrl: "../static/image/intensity_small/1.png",
        iconSize: [20, 20]
    }),
    "2": new L.Icon({
        iconUrl: "../static/image/intensity_small/2.png",
        iconSize: [20, 20]
    }),
    "3": new L.Icon({
        iconUrl: "../static/image/intensity_small/3.png",
        iconSize: [20, 20]
    }),
    "4": new L.Icon({
        iconUrl: "../static/image/intensity_small/4.png",
        iconSize: [20, 20]
    }),
    "5-": new L.Icon({
        iconUrl: "../static/image/intensity_small/5-.png",
        iconSize: [20, 20]
    }),
    "5+": new L.Icon({
        iconUrl: "../static/image/intensity_small/5+.png",
        iconSize: [20, 20]
    }),
    "6-": new L.Icon({
        iconUrl: "../static/image/intensity_small/6-.png",
        iconSize: [20, 20]
    }),
    "6+": new L.Icon({
        iconUrl: "../static/image/intensity_small/6+.png",
        iconSize: [20, 20]
    }),
    "7": new L.Icon({
        iconUrl: "../static/image/intensity_small/7.png",
        iconSize: [20, 20]
    }),
    "5?": new L.Icon({
        iconUrl: "../static/image/intensity_small/5_.png",
        iconSize: [20, 20]
    })
};
window.epicenter_icon = new L.Icon({
    iconUrl: "../static/image/epicenter.png",
    iconSize: [40, 40]
});
window.iconGroup = L.featureGroup();
var initializeMap = function () {
    window.map = L.map('map', {
        zoomControl: false,
        center: [38.272688535980976, 137],
        zoom: 5,
        maxZoom: 8,
        minZoom: 2,
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
        }
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
        }
    }).addTo(window.map);
    // Borderlines
    L.geoJSON(_GEOJSON_JAPAN_WITH_SUB_AREAS, {
        style: () => {
            return {
                stroke: true,
                fill: false,
                color: "#4e4e4e",
                weight: 1
            }
        }
    }).addTo(window.map);
    L.geoJSON(_GEOJSON_JAPAN, {
        style: () => {
            return {
                stroke: true,
                fill: false,
                color: "#7e7e7e",
                weight: 1
            }
        }
    }).addTo(window.map);
};
var addMapIntensities = function (intensityList) {
    for (var i in intensityList) {
        var intensity = intensityList[i]["intensity"];
        var latitude = intensityList[i]["latitude"];
        var longitude = intensityList[i]["longitude"];
        if (intensityList[i]["is_area"] == "true") {
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
            layer.setZIndexOffset(50);
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
    window.iconGroup.addLayer(epicenterMarker);
};
var deleteAllLayers = function () {
    try {
        if (window.colorMapLayer != undefined) {
            window.colorMapLayer.removeFrom(window.map);
        }
        if (window.iconGroup != undefined) {
            window.iconGroup.clearLayers();
        }
        if (window.swave_circle != undefined) {
            window.map.removeLayer(window.swave_circle);
        }
        if (window.pwave_circle != undefined) {
            window.map.removeLayer(window.pwave_circle);
        }
    } catch (e) {
        window.logger.error("Failed to remove layers." + e);
    }
};
var parseMapScale = function () {
    window.logger.info(window.iconGroup.getBounds());
    window.map.fitBounds(window.iconGroup.getBounds(), {padding: [0, 30]});
};
var addMapColoring = function (geojson_content) {
    window.colorMapLayer = L.geoJson(geojson_content,
        {style: parseColorStyle}
    );
    window.colorMapLayer.addTo(window.map);
};
var parseColorStyle = function (feature) {
    /**
     * @typedef {Object} feature
     * @property {Object} properties
     * @property {String} intensity_color
     */
    return {
        fillColor: feature.properties.intensity_color,
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