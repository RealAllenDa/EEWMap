window.intensity_area_icons = {
    1: new L.Icon({
        iconUrl: "../static/image/intensity_big/1.png",
        iconSize: [25, 25]
    }),
    2: new L.Icon({
        iconUrl: "../static/image/intensity_big/2.png",
        iconSize: [25, 25]
    }),
    3: new L.Icon({
        iconUrl: "../static/image/intensity_big/3.png",
        iconSize: [25, 25]
    }),
    4: new L.Icon({
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
    1: new L.Icon({
        iconUrl: "../static/image/intensity_small/1.png",
        iconSize: [20, 20]
    }),
    2: new L.Icon({
        iconUrl: "../static/image/intensity_small/2.png",
        iconSize: [20, 20]
    }),
    3: new L.Icon({
        iconUrl: "../static/image/intensity_small/3.png",
        iconSize: [20, 20]
    }),
    4: new L.Icon({
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
   iconSize: [35, 35]
});
window.layers = [];
var initializeMap = function () {
    var map_url = "https://api.mapbox.com/styles/v1/allenda/ckp1e65ta2uk618rwi5ibfluz/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWxsZW5kYSIsImEiOiJja241dWpnNWwwN3Q3MnRwNm1ueWJvaDUyIn0.mugew7hjEAG-zFoXg_pYiw";
    window.map = L.map('map', {
        zoomControl: false,
        center: [38.272688535980976, 137],
        zoom: 5
    });
    L.tileLayer(map_url, {
        maxZoom: 8,
        attribution: "Data by <a href='http://www.jma.go.jp/jma/index.html'>JMA</a> | " +
            "EEWMap by AllenDa | " +
            "Map by <a href='https://mapbox.com'>Mapbox</a>"
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
        if (intensity == "1" || intensity == "2" || intensity == "3" || intensity == "4") {
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
        }
        window.layers.push(layer);
    }
    window.iconGroup = L.layerGroup(window.layers);
    window.map.addLayer(window.iconGroup);
};
var addEpicenter = function (latitude, longitude) {
    window.epicenterMarker = L.marker([latitude, longitude], {icon: window.epicenter_icon}).addTo(window.map);
    window.epicenterMarker.setZIndexOffset(50);
};
var deleteAllLayers = function () {
    try {
        if (window.epicenterMarker != undefined) {
            window.map.removeLayer(window.epicenterMarker);
        }
        if (window.colorMapLayer != undefined) {
            window.colorMapLayer.removeFrom(window.map);
        }
        if (window.iconGroup != undefined) {
            window.iconGroup.clearLayers();
            window.layers = [];
        }
        if (window.swave_circle != undefined) {
            window.map.removeLayer(window.swave_circle);
        }
    } catch (e){
        console.error("Failed to remove layers.", e);
    }
};
var parseMapScale = function (earthquakePoints, epicenterlat, epicenterlong) {
    if (epicenterlat == undefined || epicenterlong == undefined) {
        epicenterlat = 0;
        epicenterlong = 0;
        console.warn("No epicenter is defined. Check backend code.");
    }
    var longitude = [parseFloat(epicenterlong), parseFloat(epicenterlong)];
    var latitude = [parseFloat(epicenterlat), parseFloat(epicenterlat)];
    var sum_longitude = parseFloat(epicenterlong);
    var sum_latitude = parseFloat(epicenterlat);
    var point_count = 1;
    if (epicenterlat == 0 && epicenterlong == 0) {
        point_count = 0; // Without epicenter
    }
    var point_scale;
    for (var i in earthquakePoints) {
        sum_longitude += parseFloat(earthquakePoints[i]["longitude"]);
        sum_latitude += parseFloat(earthquakePoints[i]["latitude"]);
        longitude = [Math.max(longitude[0], parseFloat(earthquakePoints[i]["longitude"])), Math.min(longitude[1], parseFloat(earthquakePoints[i]["longitude"]))];
        latitude = [Math.max(latitude[0], parseFloat(earthquakePoints[i]["latitude"])), Math.min(latitude[1], parseFloat(earthquakePoints[i]["latitude"]))];
        point_count++;
    }
    var center = [sum_latitude / point_count, sum_longitude / point_count];
    if (epicenterlong == 0 && epicenterlat == 0) {
        latitude[1] = center[0];
        longitude[1] = center[1];
    }
    var distance = Math.sqrt(Math.pow((latitude[0]-latitude[1]), 2) + Math.pow((longitude[0]-longitude[1]), 2));
    console.log(latitude, longitude, [sum_latitude, sum_longitude], point_count, center, distance);
    if(distance < 1){
        point_scale = 8;
    } else if (distance >= 1 && distance < 2) {
        point_scale = 7;
    } else if (distance >= 2 && distance < 3){
        point_scale = 7;
    } else if (distance >= 3 && distance < 4){
        point_scale = 6;
    } else if (distance >= 100) {
        // Abnormal scaling, probably because less points are involved
        point_scale = 8;
    } else {
        point_scale = 5;
    }
    console.log(center, point_scale);
    window.map.setZoom(point_scale, {animate: false});
    window.map.panTo(center, {animate: false});
};
var parseEpicenterMapScale = function (epicenterlat, epicenterlong) {
    var earthquake_points = [];
    for (var i in window.iconGroup._layers) {
        earthquake_points[earthquake_points.length] = {
            "longitude": window.iconGroup._layers[i]._latlng["lng"],
            "latitude": window.iconGroup._layers[i]._latlng["lat"]
        };
    }
    parseMapScale(earthquake_points, epicenterlat, epicenterlong);
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
    color: "#ff7800",
    weight: 4,
    opacity: 1,
    fillColor: '#ff7800',
    fillOpacity: 0.2
  }).addTo(window.map);
};