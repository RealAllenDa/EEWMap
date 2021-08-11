var initializeMap = function () {
    window.map_japan = L.map('map_main', {
        zoomControl: false,
        center: [38.06539235133249, 139.08691406250003],
        zoom: 5,
        attributionControl: false,
        maxZoom: 8,
        minZoom: 2,
        zoomSnap: 0.01,
        zoomDelta: 0.5
    });
    window.map_okinawa = L.map('map_okinawa', {
        zoomControl: false,
        center: [25.918526162075153, 127.17773437500001],
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
    var map_japan_url = "https://earthquake.daziannetwork.com/japan/{z}/{x}/{y}.pbf";
    var map_borders_url = "https://earthquake.daziannetwork.com/japan_area_line/{z}/{x}/{y}.pbf";
    var area_line_tile_option = {
        layerURL: map_borders_url,
        rendererFactory: L.canvas.tile,
        vectorTileLayerStyles: {
            "japan_area_line": {
                weight: 1,
                fillOpacity: 0,
                color: "#000000"
            }
        },
        bounds: [[-49.250870, -178.137086], [81.128531, 178.448622]]
    };
    var japan_tile_option = {
        layerURL: map_japan_url,
        rendererFactory: L.canvas.tile,
        vectorTileLayerStyles: {
            "japan": {
                weight: 0,
                fillColor: "#5e5e5e",
                fillOpacity: 1,
                fill: true
            }
        }
    };
    new L.vectorGrid.protobuf(map_japan_url, japan_tile_option).addTo(window.map_japan);
    new L.vectorGrid.protobuf(map_japan_url, japan_tile_option).addTo(window.map_okinawa);
    new L.vectorGrid.protobuf(map_japan_url, japan_tile_option).addTo(window.map_ogasawara);
    new L.vectorGrid.protobuf(map_borders_url, area_line_tile_option).addTo(window.map_japan);
    new L.vectorGrid.protobuf(map_borders_url, area_line_tile_option).addTo(window.map_okinawa);
    new L.vectorGrid.protobuf(map_borders_url, area_line_tile_option).addTo(window.map_ogasawara);
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
    getTsunamiMapInfo();
    setInterval(function () {
        getTsunamiMapInfo();
    }, 5000);
};