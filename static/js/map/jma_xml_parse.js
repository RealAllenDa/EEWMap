var getJmaXML = function () {
    $.ajax({
        type: "GET",
        url: "/api/get_jma_xml",
        dataType: "JSON",
        cache: false,
        timeout: 3000,
        success: jmaXMLParse
    });
};
var lastMessage = {};
var jmaXMLParse = function (result) {
    /*
    * Status list:
    *  -1 - Retrieve failed
    *  0 - Earthquake Information (VXSE53)
    *  1 - Intensity Report (VXSE51)
    *  2 - Hypocenter Report (VXSE52)
    *  3 - Earthquake Early Warning (Forecast) (VXSE41)
    *  4 - Earthquake Early Warning (Warning) (VXSE40)
    *  5 - Tsunami Warning (VTSE51/41) TODO
    *  */
    console.debug(result);
    var resp_content = result["content"];
    if (result["status"] == -1) {
        console.warn("Can't retrieve data.");
        return;
    }
    if (compare(lastMessage, result)) {
        console.debug("Identical information. No need to update.");
        return;
    } else {
        lastMessage = result;
        console.debug("Updated message. Parsing...");
    }
    if ([0, 1, 2].indexOf(result["status"]) != -1) {
        // Hide EEW div, show Earthquake Report div
        window.DOM.eew_display_div.style.display = "none";
        window.DOM.intensity_display_div.style.display = "grid";
    } else if ([3, 4].indexOf(result["status"]) != -1) {
        // Hide Earthquake Report div, show EEW div
        window.DOM.eew_display_div.style.display = "grid";
        window.DOM.intensity_display_div.style.display = "none";
    }
    if (result["status"] == 0) {
        displayEarthquakeInformation(resp_content, false);
        deleteAllLayers();
        if (resp_content["is_overseas"] == false) {
            displayIntensityCode(resp_content["max_intensity"], false);
            parseMapScale(resp_content["area_intensity"], resp_content["hypocenter"]["latitude"], resp_content["hypocenter"]["longitude"]);
            addMapIntensities(resp_content["area_intensity"]);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
        } else {
            displayIntensityCode(0, false);
            addEpicenter(resp_content["hypocenter"]["latitude"], resp_content["hypocenter"]["longitude"]);
            window.map.setZoom(2);
            window.map.panTo([4, -5]);
        }
    } else if (result["status"] == 1) {
        window.DOM.intensity_report_div.style.display = "block";
        window.DOM.earthquake_report_div.style.display = "none";
        window.DOM.intensity_report_occur_time.innerText = resp_content["occur_time"];
        displayIntensityCode(resp_content["max_intensity"], false);
        deleteAllLayers();
        parseMapScale(resp_content["area_intensity"]["intensity"], 0, 0);
        addMapIntensities(resp_content["area_intensity"]["intensity"]);
        // Parse map coloring
        addMapColoring(resp_content["area_intensity"]["geojson"]);
        setBannerContent(resp_content["tsunami_comments"]["code"], resp_content["tsunami_comments"]["text"]);
    } else if (result["status"] == 2) {
        displayEarthquakeInformation(resp_content, false);
    } else if (result["status"] == 3 || result["status"] == 4) {
        parseEEWInfo(resp_content);
    }
    if (result["content"]["is_test"] == true && [0, 1, 2].indexOf(result["status"]) != -1) {
        // Not eew & training
        setBannerContent("999");
    }
};
var parseEEWInfo = function (result) {
    displayEarthquakeInformation(result, true);
    displayIntensityCode(result["max_intensity"], true);
    if (result["is_cancel"]) {
        // Hide EEW div, show Earthquake Report div
        window.DOM.eew_display_div.style.display = "none";
        window.DOM.intensity_display_div.style.display = "grid";
        window.DOM.information_banner.innerText = "Previous Earthquake Early Warning had been canceled";
        window.DOM.information_banner.style.color = "white";
        window.DOM.information_banner_div.style.background = "var(--info-background-color)";
    }
    if (result["is_final"]) {
        window.DOM.eew_report_number.innerText = "#" + result["report_num"] + "-F";
    } else {
        window.DOM.eew_report_number.innerText = "#" + result["report_num"];
    }
    deleteAllLayers();
    addEpicenter(result["hypocenter"]["latitude"], result["hypocenter"]["longitude"]);
    parseMapScale([], result["hypocenter"]["latitude"], result["hypocenter"]["longitude"]);
    if (!(compare(result["area_intensity"]["geojson"], {}) && compare(result["area_intensity"]["intensity"], {}))) {
        addMapIntensities(result["area_intensity"]["intensity"]);
        addMapColoring(result["area_intensity"]["geojson"]);
    } else {
        console.warn("area_intensity equals {}. No map coloring.");
    }
    if (result["report_flag"] == 3) {
        // Earthquake Forecast
        window.DOM.eew_banner_div.style.background = "var(--info-background-color)";
        window.DOM.eew_banner.innerText = "Earthquake Early Warning (Forecast)";
        // Manually set the zoom since no earthquake point exists
        window.map.setZoom(7);
    } else {
        // EEW
        window.DOM.eew_banner_div.style.background = "var(--intensity-8)";
        window.DOM.eew_banner.innerText = "Earthquake Early Warning (Warning) - Strong Shaking Expected";
    }
    if (["1", "2", "3", "4"].indexOf(result["max_intensity"]) != -1) {
        window.DOM.eew_advice.style.background = "var(--intensity-2)";
        window.DOM.eew_advice.innerText = "Pay attention to coastal areas";
    } else {
        window.DOM.eew_advice.style.background = "var(--intensity-7)";
        window.DOM.eew_advice.innerText = "Stay away from coastal areas";
    }
    if (result["is_test"]) {
        window.DOM.eew_banner_div.style.background = "var(--intensity-2)";
        window.DOM.eew_banner.innerText = "Drill - Not Real Situation";
        window.DOM.eew_advice.style.background = "var(--intensity-2)";
        window.DOM.eew_advice.innerText = "Drill - Not Real Situation";
    }
    if (result["is_degraded"]) {
        console.warn("Result degraded. Check server log.");
    }
};
var displayEarthquakeInformation = function (resp_content, is_eew) {
    var epicenter = document.getElementById("epicenter");
    var depth = document.getElementById("depth");
    var magnitude = document.getElementById("magnitude");
    if (is_eew) {
        epicenter = document.getElementById("eew-epicenter");
        depth = document.getElementById("eew-depth");
        magnitude = document.getElementById("eew-magnitude");
        window.DOM.eew_receive_time.innerText = resp_content["report_time"];
    } else {
        window.DOM.intensity_report_div.style.display = "none";
        window.DOM.earthquake_report_div.style.display = "block";
        window.DOM.occur_time.innerText = resp_content["occur_time"];
        setBannerContent(resp_content["tsunami_comments"]["code"], resp_content["tsunami_comments"]["text"]);
    }
    epicenter.innerText = resp_content["hypocenter"]["name"];
    depth.innerText = resp_content["hypocenter"]["depth"];
    magnitude.innerText = resp_content["magnitude"];
};