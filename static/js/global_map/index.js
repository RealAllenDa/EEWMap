var initializeDOM = function () {
    window.DOM = {};
    window.DOM.list_container = document.getElementById("main-container");
    window.DOM.detail_map_container = document.getElementById("detail-map-container");
    if (window.__HN_SDK__.getUrlParams("show_map") == "false") {
        window.DOM.detail_map_container.style.display = "none";
    }
};
var getGlobalEarthquakeInfo = function () {
    $.ajax({
        type: "GET",
        url: "/api/global_earthquake_info",
        cache: false,
        dataType: "JSON",
        timeout: 3500,
        success: parseEqInfo,
        error: function () {
            console.warn("Failed to retrieve data.");
        }
    });
};
var last_message = {};
var parseEqInfo = function (result) {
    console.debug(result);
    if (result["status"] != 0) {
        console.warn("Incorrect response format. Breaking.");
        return;
    }
    if (_.isEqual(last_message, result)) {
        console.debug("Identical information. No need to update.");
    } else {
        last_message = result;
        console.debug("Updated information. Parsing...");
        parseEqList(result);
    }
};
var parseEqList = function (result) {
    window.DOM.list_container.innerHTML = "";
    result["data"].forEach((i) => {
        var infoItem = document.createElement("div");
        infoItem.classList.add("earthquake-item");
        var timeDepthContainer = document.createElement("div");
        timeDepthContainer.className = "sub-container";
        var epicenterMagnitudeContainer = document.createElement("div");
        epicenterMagnitudeContainer.className = "sub-container";

        var timeItem = document.createElement("span");
        timeItem.innerText = i["occur_time"];
        timeDepthContainer.appendChild(timeItem);

        var depthContainer = document.createElement("span");
        var depthItem = document.createElement("span");
        depthItem.className = "important highlighted";
        depthItem.innerText = i["epicenter"]["depth"];
        depthContainer.appendChild(depthItem);
        var depthIndicator = document.createElement("span");
        depthIndicator.innerText = "km";
        depthIndicator.className = "unimportant";
        depthContainer.appendChild(depthIndicator);
        timeDepthContainer.appendChild(depthContainer);

        var epicenterItem = document.createElement("span");
        epicenterItem.innerText = i["epicenter"]["name"];
        epicenterItem.className = "important";
        epicenterMagnitudeContainer.appendChild(epicenterItem);

        var magnitudeContainer = document.createElement("span");
        var magnitudeIndicator = document.createElement("span");
        magnitudeIndicator.innerText = "M";
        magnitudeIndicator.className = "unimportant";
        magnitudeContainer.appendChild(magnitudeIndicator);
        var magnitudeItem = document.createElement("span");
        magnitudeItem.innerText = i["magnitude"];
        magnitudeItem.className = "important highlighted";
        magnitudeContainer.appendChild(magnitudeItem);
        epicenterMagnitudeContainer.appendChild(magnitudeContainer);

        infoItem.appendChild(timeDepthContainer);
        infoItem.appendChild(epicenterMagnitudeContainer);
        infoItem.classList.add("intensity-" + i["mmi"]);

        infoItem.onclick = function () {
            showEqMap(i);
        };
        window.DOM.list_container.appendChild(infoItem);
    });
};
var showEqMap = function (content) {
    window.DOM.detail_map_container.contentWindow.parseEqInfo(
        {
            "info": [
                {
                    "area_intensity": {
                        "areas": {},
                        "station": {}
                    },
                    "hypocenter": {
                        "longitude": content["epicenter"]["longitude"],
                        "latitude": content["epicenter"]["latitude"],
                        "depth": content["epicenter"]["depth"] + "km",
                        "name": content["epicenter"]["name"]
                    },
                    "magnitude": content["magnitude"],
                    "max_intensity": transformIntensity(content["mmi"]),
                    "occur_time": content["occur_time"],
                    "receive_time": content["receive_time"],
                    "tsunami_comments": {
                        "domestic": "Unknown",
                        "foreign": "None"
                    },
                    "type": "Foreign"
                }
            ]
        }
    );
    window.DOM.detail_map_container.contentDocument.getElementById("banner-description-domestic").innerText = "Tsunami: Unknown";
    window.DOM.detail_map_container.contentWindow.map.setZoom(4);
};
var transformIntensity = function (mmi) {
    switch (mmi) {
        case 1:
        case 2:
            return "1";
        case 3:
            return "2";
        case 4:
            return "3";
        case 5:
            return "4";
        case 6:
            return "5-";
        case 7:
            return "5+";
        case 8:
            return "6-";
        case 9:
            return "6+";
        case 10:
            return "7";
        default:
            return "0";
    }
};
window.onload = function () {
    try {
        initializeDOM();
        window.DOM.detail_map_container.contentWindow.clearInterval(window.DOM.detail_map_container.contentWindow.getEqInfoTimer);
    } catch (e) {
        console.error("Failed to initialize: " + e);
    }
    setInterval(function () {
        getGlobalEarthquakeInfo();
    }, 3500);
};