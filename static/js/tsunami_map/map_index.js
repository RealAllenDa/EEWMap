var initializeMap = function () {
    var map_url = "https://api.mapbox.com/styles/v1/allenda/ckp1ecj0u2dac18otb4iu0wdy/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiYWxsZW5kYSIsImEiOiJja241dWpnNWwwN3Q3MnRwNm1ueWJvaDUyIn0.mugew7hjEAG-zFoXg_pYiw";
    window.map_japan = L.map('map_main', {
        zoomControl: false,
        center: [38.06539235133249, 139.08691406250003],
        zoom: 5,
        attributionControl: false
    });
    window.map_okinawa = L.map('map_okinawa', {
        zoomControl: false,
        center: [25.918526162075153, 127.17773437500001],
        zoom: 5,
        attributionControl: false
    });
    window.map_ogasawara = L.map('map_ogasawara', {
        zoomControl: false,
        center: [26.902476886279832, 142.14111328125003],
        zoom: 7,
        attributionControl: false
    });
    L.tileLayer(map_url, {
        maxZoom: 8
    }).addTo(window.map_japan);
    L.tileLayer(map_url, {
        maxZoom: 8
    }).addTo(window.map_okinawa);
    L.tileLayer(map_url, {
        maxZoom: 8
    }).addTo(window.map_ogasawara);
    window.map_ogasawara.scrollWheelZoom.disable();
    window.map_ogasawara.dragging.disable();
    window.map_ogasawara.doubleClickZoom.disable();
    window.map_japan.scrollWheelZoom.disable();
    window.map_japan.dragging.disable();
    window.map_japan.doubleClickZoom.disable();
    window.map_okinawa.scrollWheelZoom.disable();
    window.map_okinawa.dragging.disable();
    window.map_okinawa.doubleClickZoom.disable();
};
window.onload = function () {
    try {
        initializeMap();
    } catch (e) {
        console.error("Failed to initialize the map. ", e);
    }
    setInterval(function () {
        getTsunamiMapInfo();
    }, 5000);
};