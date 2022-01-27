var initializeMap = function () {
    window.map_japan = L.map('map_main', {
        zoomControl: false,
        center: {
            "lat": 38.426610210705135,
            "lng": 138.42138499239283
        },
        attributionControl: false,
        maxZoom: 8,
        minZoom: 2,
        zoomSnap: 0.01,
        zoomDelta: 0.01,
        zoom: 5.1,
    });
    window.map_okinawa = L.map('map_okinawa', {
        zoomControl: false,
        center: {
            "lat": 26.674949874061767,
            "lng": 127.24804714322093
        },
        zoom: 5,
        attributionControl: false,
        maxZoom: 8,
        minZoom: 2,
        zoomSnap: 0.01,
        zoomDelta: 0.5
    });
    window.map_ogasawara = L.map('map_ogasawara', {
        zoomControl: false,
        center: [26.91439669619432, 142.14703272013634],
        zoom: 7.57,
        attributionControl: false,
        maxZoom: 8,
        minZoom: 2,
        zoomSnap: 0.01,
        zoomDelta: 0.5
    });
    L.geoJson(_GEOJSON_TSUNAMI_JAPAN, {
        style: {
            weight: 0,
            fillColor: "#5e5e5e",
            fillOpacity: 1,
            fill: true
        },
        pane: "overlayPane"
    }).addTo(window.map_japan);
    L.geoJson(_GEOJSON_TSUNAMI_JAPAN, {
        style: {
            weight: 0,
            fillColor: "#5e5e5e",
            fillOpacity: 1,
            fill: true
        },
        pane: "overlayPane"
    }).addTo(window.map_okinawa);
    L.geoJson(_GEOJSON_TSUNAMI_JAPAN, {
        style: {
            weight: 0,
            fillColor: "#5e5e5e",
            fillOpacity: 1,
            fill: true
        },
        pane: "overlayPane"
    }).addTo(window.map_ogasawara);

    L.geoJson(_GEOJSON_JAPAN_AREA_LINE, {
        style: {
            weight: 1,
            fillOpacity: 0,
            color: "#000000"
        },
        pane: "overlayPane"
    }).addTo(window.map_japan);
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
    // Call now to avoid waiting for 5 seconds.
    getTsunamiForecastMapInfo();
    setInterval(function () {
        getTsunamiForecastMapInfo();
    }, 5000);
};