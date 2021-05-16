var getEqInfo = function () {
    $.ajax({
        type: "GET",
        url: "/api/earthquake_info",
        cache: false,
        timeout: 3500,
        success: function (result) {
            eval("var result = " + result);
            parseEqInfo(result);
        },
        error: function () {
            console.warn("Failed to retrieve data.");
        }
    });
};
var last_message = {};
var parseEqInfo = function (result) {
    /*
    if ([0, 1, 2].indexOf(result["status"]) != -1) {
        // Hide EEW div, show Earthquake Report div
        window.DOM.eew_display_div.style.display = "none";
        window.DOM.intensity_display_div.style.display = "grid";
    } else if ([3, 4].indexOf(result["status"]) != -1) {
        // Hide Earthquake Report div, show EEW div
        window.DOM.eew_display_div.style.display = "grid";
        window.DOM.intensity_display_div.style.display = "none";
    }
    */
    console.debug(result);
    var result_for_compare = result;
    if (_.isEqual(last_message, result_for_compare)) {
        console.debug("Identical information. No need to update.");
        return;
    } else {
        last_message = result_for_compare;
        console.debug("Updated message. Parsing...");
    }
    // From the last one to the first one (sequence)
    result = result.reverse();
    for (var i = 0; i < result.length; i++) {
        var resp_content = result[i];
        if (resp_content["max_intensity"] == 99999) {
            resp_content["max_intensity"] = "--";
        }
        if (resp_content["type"] == "ScalePrompt") {
            window.DOM.intensity_report_div.style.display = "block";
            window.DOM.earthquake_report_div.style.display = "none";
            window.DOM.intensity_report_occur_time.innerText = resp_content["occur_time"];
            displayIntensityCode(resp_content["max_intensity"], false);
            deleteAllLayers();
            parseMapScale(resp_content["area_intensity"]["areas"], 0, 0);
            addMapIntensities(resp_content["area_intensity"]["areas"]);
            // Parse map coloring
            if (resp_content["area_intensity"]["geojson"] != "null") {
                addMapColoring(resp_content["area_intensity"]["geojson"]);
            }
            setBannerContent(resp_content["tsunami_comments"]);
        } else if (resp_content["type"] == "Destination") {
            displayEarthquakeInformation(resp_content, false);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            parseEpicenterMapScale(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
        } else if (resp_content["type"] == "ScaleAndDestination") {
            // Not enough examples, assumed process
            displayIntensityCode(resp_content["max_intensity"], false);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            displayEarthquakeInformation(resp_content, false);
            parseEpicenterMapScale(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
        } else if (resp_content["type"] == "DetailScale") {
            displayEarthquakeInformation(resp_content, false);
            deleteAllLayers();
            displayIntensityCode(resp_content["max_intensity"], false);
            parseMapScale(resp_content["area_intensity"]["areas"],
                resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            addMapIntensities(resp_content["area_intensity"]["areas"]);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
        }
    }
};
var parseEEWInfo = function (result) {
    if (result["is_cancel"]) {
        // Hide EEW div, show Earthquake Report div
        window.DOM.eew_display_div.style.display = "none";
        window.DOM.intensity_display_div.style.display = "grid";
        window.DOM.information_banner.innerText = "Previous Earthquake Early Warning had been cancelled";
        window.DOM.information_banner.style.color = "white";
        window.DOM.information_banner_div.style.background = "var(--intensity-3)";
        window.DOM.expected_flag.style.display = "none";
        window.DOM.drill_flag.style.display = "none";
        deleteAllLayers();
        return;
    }
    displayEarthquakeInformation(result, true);
    displayIntensityCode(result["max_intensity"], true);
    if (result["is_final"]) {
        window.DOM.eew_report_number.innerText = "#" + result["report_num"] + "-F";
    } else {
        window.DOM.eew_report_number.innerText = "#" + result["report_num"];
    }
    deleteAllLayers();
    addEpicenter(result["hypocenter"]["latitude"], result["hypocenter"]["longitude"]);
    parseMapScale([], result["hypocenter"]["latitude"], result["hypocenter"]["longitude"]);
    if (!(_.isEqual(result["area_intensity"]["geojson"], {}) && _.isEqual(result["area_intensity"]["intensity"], {}))) {
        addMapIntensities(result["area_intensity"]["intensity"]);
        addMapColoring(result["area_intensity"]["geojson"]);
        window.DOM.expected_flag.style.display = "block";
    } else {
        window.DOM.expected_flag.style.display = "none";
        console.warn("area_intensity equals {}. No map coloring.");
    }
    if (parseInt(result["report_flag"]) == 3) {
        // Earthquake Forecast
        window.DOM.eew_banner_div.style.background = "var(--info-background-color)";
        window.DOM.eew_banner.innerText = "Earthquake Early Warning (Forecast)";
        // Manually set the zoom since no earthquake point exists
        window.map.setZoom(7, {animate: false});
    } else if (parseInt(result["report_flag"]) == 4){
        // EEW
        window.DOM.eew_banner_div.style.background = "var(--intensity-8)";
        window.DOM.eew_banner.innerText = "Earthquake Early Warning (Warning) - Strong Shaking Expected";
    } else {
        // Unknown
        window.DOM.eew_banner_div.style.background = "var(--info-background-color)";
        window.DOM.eew_banner.innerText = "Unknown EEW (Probably PLUM, etc.)";
    }
    if (result["max_intensity"] == "0") {
        window.DOM.eew_advice.style.background = "var(--info-background-color)";
        window.DOM.eew_advice.innerText = "Wait for further information";
    } else if (["1", "2", "3", "4"].indexOf(result["max_intensity"]) != -1) {
        window.DOM.eew_advice.style.background = "var(--intensity-2)";
        window.DOM.eew_advice.innerText = "Pay attention to coastal areas";
    } else {
        window.DOM.eew_advice.style.background = "var(--intensity-7)";
        window.DOM.eew_advice.innerText = "Stay away from coastal areas";
    }
    if (result["is_test"]) {
        window.DOM.drill_flag.style.display = "block";
    } else {
        window.DOM.drill_flag.style.display = "none";
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
        setBannerContent(resp_content["tsunami_comments"]);
    }
    epicenter.innerText = resp_content["hypocenter"]["name"];
    depth.innerText = resp_content["hypocenter"]["depth"];
    magnitude.innerText = resp_content["magnitude"];
};