window.layers = [];
window.iconGroup = undefined;
window.intensity_area_icons = {
    1: new L.Icon({
        iconUrl: "../static/image/intensity_area/1.png",
        iconSize: [25, 25]
    }),
    2: new L.Icon({
        iconUrl: "../static/image/intensity_area/2.png",
        iconSize: [25, 25],
    }),
    3: new L.Icon({
        iconUrl: "../static/image/intensity_area/3.png",
        iconSize: [25, 25],
    }),
    4: new L.Icon({
        iconUrl: "../static/image/intensity_area/4.png",
        iconSize: [25, 25],
    }),
    "5-": new L.Icon({
        iconUrl: "../static/image/intensity_area/5.png",
        iconSize: [25, 25],
    }),
    "5+": new L.Icon({
        iconUrl: "../static/image/intensity_area/6.png",
        iconSize: [25, 25],
    }),
    "6-": new L.Icon({
        iconUrl: "../static/image/intensity_area/7.png",
        iconSize: [25, 25],
    }),
    "6+": new L.Icon({
        iconUrl: "../static/image/intensity_area/8.png",
        iconSize: [25, 25],
    }),
    "7": new L.Icon({
        iconUrl: "../static/image/intensity_area/9.png",
        iconSize: [25, 25],
    })
};
window.epicenter_icon = new L.Icon({
   iconUrl: "../static/image/epicenter.png",
   iconSize: [25, 25]
});
var initializeMap = function () {
    var map_url = "https://www.jma.go.jp/tile/jma/transparent-cities/{z}/{x}/{y}.png";
    window.map = L.map('map', {
        zoomControl: false
    }).setView([38.272688535980976, 137], 5);
    L.tileLayer(map_url, {
        maxZoom: 8
    }).addTo(window.map);
};
var addMapIntensities = function (intensityList) {
    for (var i in intensityList) {
        var intensity = intensityList[i]["intensity"];
        var latitude = intensityList[i]["latitude"];
        var longitude = intensityList[i]["longitude"];
        var layer = new L.marker([latitude, longitude], {icon: window.intensity_area_icons[intensity]});
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
    window.epicenterMarker.setZIndexOffset(10000);
};
var deleteAllIcons = function () {
    try {
        window.map.removeLayer(window.epicenterMarker);
        window.iconGroup.clearLayers();
        window.layers = [];
    } catch {}
};
var parseMapScale = function (earthquakePoints, epicenterlat, epicenterlong) {
    var longitude = [parseInt(epicenterlong), parseInt(epicenterlong)];
    var latitude = [parseInt(epicenterlat), parseInt(epicenterlat)];
    var sum_longitude = parseInt(epicenterlong);
    var sum_latitude = parseInt(epicenterlat);
    var point_count = 1;
    if (epicenterlong == 0 && epicenterlat == 0) {
        point_count--;
    }
    var point_scale = 8;
    for (var i in earthquakePoints) {
        sum_longitude += parseInt(earthquakePoints[i]["longitude"]);
        sum_latitude += parseInt(earthquakePoints[i]["latitude"]);
        longitude = [Math.max(longitude[0], parseInt(earthquakePoints[i]["longitude"])), Math.min(longitude[1], parseInt(earthquakePoints[i]["longitude"]))];
        latitude = [Math.max(latitude[0], parseInt(earthquakePoints[i]["latitude"])), Math.min(latitude[1], parseInt(earthquakePoints[i]["latitude"]))];
        point_count++;
    }
    var center = [sum_latitude / point_count, sum_longitude / point_count];
    var distance = Math.sqrt(Math.pow((latitude[0]-latitude[1]), 2) + Math.pow((longitude[0]-longitude[1]), 2));
    console.log(latitude, longitude, [sum_latitude, sum_longitude], point_count, center, distance);
    if(distance < 1){
        point_scale = 8;
    }
    if(distance >= 1 && distance < 2){
        point_scale = 7;
    }
    if(distance >= 2 && distance < 3){
        point_scale = 6;
    }
    if(distance >= 3 && distance < 4){
        point_scale = 5;
    }
    if(distance >= 4 && distance < 5){
        point_scale = 5;
    }
    if(distance >= 5 && distance < 6){
        point_scale = 5;
    }
    if(distance >= 6 && distance < 7){
        point_scale = 5;
    }
    if(distance >= 7 && distance < 8){
        point_scale = 5;
    }
    if(distance >= 8 && distance < 9){
        point_scale = 5;
    }
    if(distance >= 9 && distance < 10){
        point_scale = 5;
    }
    if(distance >= 10){
        point_scale = 5;
    }
    console.log(center, point_scale);
    window.map.setZoom(point_scale, {animate: false});
    window.map.panTo(center, {animate: false});
};
