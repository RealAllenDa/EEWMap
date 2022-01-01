var getEqInfo = function () {
    $.ajax({
        type: "GET",
        url: "/api/earthquake_info",
        cache: false,
        dataType: "JSON",
        timeout: 2500,
        success: splitEqInfo,
        error: function () {
            console.warn("Failed to retrieve data.");
        }
    });
};
var last_message = {};
var last_eew_report_num = -1;
var messages_before_eew = [];
var eew_in_effect = false;
var suspend_eew_until_number_change = false;
var splitEqInfo = function (result) {
    console.debug(result);
    var result_for_compare = result;
    // Pre-check info
    if (!result.hasOwnProperty("eew") || !result.hasOwnProperty("info")) {
        console.error("Message format incorrect. Breaking.");
        return;
    } else if (_.isEqual([], result["info"])) {
        console.warn("Info has no message inside.");
    }
    if (_.isEqual(last_message, result_for_compare)) {
        console.debug("Identical information. No need to update.");
        return;
    } else {
        last_message = result_for_compare;
        console.debug("Updated message. Parsing...");
    }
    if (result["eew"]["status"] == 0) {
        console.info("EEW received. Parsing...");
        if (!eew_in_effect) {
            // EEW first received
            console.info("EEW first received. Setting variables to default.");
            messages_before_eew = result["info"];
            eew_in_effect = true;
            last_eew_report_num = -1;
        }
        if (parseInt(result["eew"]["report_num"]) > parseInt(last_eew_report_num)) {
            // New EEW, display EEW
            console.info("EEW updated (num != last_num). Displaying EEW.");
            last_eew_report_num = result["eew"]["report_num"];
            suspend_eew_until_number_change = false;
            parseEEWInfo(result);
            if (window.swave_circle != undefined) {
                window.swave_circle.bringToFront();
            } else {
                console.warn("Failed to bring the S wave circle to front. " +
                    "Check backend code.");
            }
            if (window.pwave_circle != undefined) {
                window.pwave_circle.bringToFront();
            } else {
                console.warn("Failed to bring the P wave circle to front. " +
                    "Check backend code.");
            }
        } else if (!(_.isEqual(result["info"], messages_before_eew))) {
            console.info("Earthquake info updated. Displaying new earthquake info.");
            messages_before_eew = result["info"];
            suspend_eew_until_number_change = true;
            parseEqInfo(result);
        } else if (!suspend_eew_until_number_change) {
            console.info("Parameter updated. Displaying EEW.");
            // In this case, we only updates the map, not the information.
            parseEEWInfo(result, true);
            if (window.swave_circle != undefined) {
                window.swave_circle.bringToFront();
            } else {
                console.warn("Failed to bring the S wave circle to front. " +
                    "Check backend code.");
            }
            if (window.pwave_circle != undefined) {
                window.pwave_circle.bringToFront();
            } else {
                console.warn("Failed to bring the P wave circle to front. " +
                    "Check backend code.");
            }
        }
    } else {
        eew_in_effect = false;
        parseEqInfo(result);
    }
};
var parseEqInfo = function (result) {
    // Hide EEW div, show Earthquake Report div
    window.DOM.eew_display_div.style.display = "none";
    window.DOM.intensity_display_div.style.display = "grid";
    window.DOM.expected_flag.style.display = "none";
    window.DOM.drill_flag.style.display = "none";
    // When displaying EEW, this pane should cover the intensities. (S wave circle)
    // But when displaying earthquake information, this pane shouldn't.
    // So, we restore it to normal when displaying earthquake information
    $(".leaflet-overlay-pane")[0].className = "leaflet-pane leaflet-overlay-pane";
    result = result["info"];
    for (var i = 0; i < result.length; i++) {
        // In extreme conditions, there could be multiple reports.
        var resp_content = result[i];
        if (resp_content["max_intensity"] == 99999 || resp_content["max_intensity"] == "-1") {
            resp_content["max_intensity"] = "-1";
        }
        if (resp_content["type"] == "ScalePrompt") {
            /*
            * For scale prompt:
            *   1. Earthquake information div -> Intensity report div
            *       1.1 Change report time
            *   2. Display big intensity code
            *   3. Delete all layers on map
            *   4. Add area intensities on map
            *   5. Check if GeoJson for intensities are present
            *       True -> Add coloring (via GeoJson)
            *   6. Parse map scale
            *   7. Set status banner
            * */
            window.DOM.intensity_report_div.style.display = "block";
            window.DOM.earthquake_report_div.style.display = "none";
            window.DOM.intensity_report_occur_time.innerText = resp_content["occur_time"];
            displayIntensityCode(resp_content["max_intensity"], false);
            deleteAllLayers();
            if (resp_content["area_intensity"]["areas"] != null) {
                addMapIntensities(resp_content["area_intensity"]["areas"]);
                addMapColoring(resp_content["area_intensity"]["areas"]);
            }
            parseMapScale();
            setBannerContent(resp_content["tsunami_comments"]);
        } else if (resp_content["type"] == "Destination") {
            /*
            * For Destination (Hypocenter Report):
            *   1. Display earthquake information (Hypocenter)
            *   2. Add epicenter marker on map
            *   3. Parse map scale
            * */
            displayEarthquakeInformation(resp_content, false);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            parseMapScale();
        } else if (resp_content["type"] == "ScaleAndDestination") {
            /*
            * For ScaleAndDestination (Hypocenter and area intensity Report):
            *   1. Display big intensity code
            *   2. Delete all layers on map
            *   3. Add epicenter marker on map
            *   4. Add area intensities on map
            *   5. Check if GeoJson for intensities are present
            *       True -> Add coloring (via GeoJson)
            *   6. Parse map scale
            *   7. Set status banner
            *   8. Display earthquake information (Hypocenter)
            * */
            displayIntensityCode(resp_content["max_intensity"], false);
            deleteAllLayers();
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            if (resp_content["area_intensity"]["areas"] != null) {
                addMapIntensities(resp_content["area_intensity"]["areas"]);
                addMapColoring(resp_content["area_intensity"]["areas"]);
            }
            parseMapScale();
            setBannerContent(resp_content["tsunami_comments"]);
            displayEarthquakeInformation(resp_content, false);
        } else if (resp_content["type"] == "DetailScale") {
            /*
            * For DetailScale (Hypocenter and detailed intensity Report):
            *   1. Display earthquake information (Hypocenter)
            *   2. Delete all layers on map
            *   3. Display big intensity code
            *   4. Add station intensities on map
            *   5. Add epicenter marker on map
            *   6. Parse map scale
            * */
            displayEarthquakeInformation(resp_content, false);
            deleteAllLayers();
            displayIntensityCode(resp_content["max_intensity"], false);
            addMapIntensities(resp_content["area_intensity"]["station"]);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            //addMapColoring(resp_content["area_intensity"]["geojson"]);
            parseMapScale();
        } else if (resp_content["type"] == "Foreign") {
            /*
            * For Foreign (Foreign Earthquake Report):
            *   1. Display earthquake information (Hypocenter)
            *   2. Delete all layers on map
            *   3. Display big intensity code
            *       NOTE: For foreign, it'll always be -1.
            *   4. Add epicenter marker on map
            *   5. Set zoom & location for map
            * */
            displayEarthquakeInformation(resp_content, false);
            deleteAllLayers();
            displayIntensityCode(resp_content["max_intensity"], false);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
            // Manually set zoom
            window.map.setZoom(2, {animate: false});
            window.map.panTo([
                resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]
            ], {animate: false});
        }
    }
};
var parseEEWInfo = function (result, only_update_map = false) {
    // Hide Earthquake Report div, show EEW div
    window.DOM.eew_display_div.style.display = "grid";
    window.DOM.intensity_display_div.style.display = "none";
    result = result["eew"];
    if (result["is_cancel"]) {
        // Restore to normal display pane
        // Hide EEW div, show Earthquake Report div
        window.DOM.eew_display_div.style.display = "none";
        window.DOM.intensity_display_div.style.display = "grid";
        window.DOM.foreign_information_banner_div.style.display = "none";
        window.DOM.domestic_information_banner.innerText = "Previous Earthquake Early Warning had been cancelled";
        window.DOM.domestic_information_banner.style.color = "white";
        window.DOM.domestic_information_banner_div.style.background = "var(--intensity-3)";
        window.DOM.expected_flag.style.display = "none";
        window.DOM.drill_flag.style.display = "none";
        // Restore pane to normal (See parseEqInfo)
        $(".leaflet-overlay-pane")[0].className = "leaflet-pane leaflet-overlay-pane";
        // Delete overlay & intensities
        deleteAllLayers();
        return;
    }
    // For EEW, we need the S wave circle cover the intensities
    // So, we add the overlay pane's class name with "overlay-eew" (Set z-index to 99999)
    // noinspection JSJQueryEfficiency
    $(".leaflet-overlay-pane")[0].className = "leaflet-pane leaflet-overlay-pane overlay-eew";
    if (!only_update_map) {
        displayEarthquakeInformation(result, true);
        displayIntensityCode(result["max_intensity"], true);
        if (result["is_final"]) {
            window.DOM.eew_report_number.innerText = "#" + result["report_num"] + "-F";
        } else {
            window.DOM.eew_report_number.innerText = "#" + result["report_num"];
        }
        if (result["is_plum"]) {
            // PLUM
            window.DOM.eew_banner_div.style.background = "var(--info-background-color)";
            window.DOM.eew_banner.innerText = "PLUM determined epicenter - No detailed information available";
        } else {
            if (parseInt(result["report_flag"]) == 0) {
                // Earthquake Forecast
                window.DOM.eew_banner_div.style.background = "var(--info-background-color)";
                window.DOM.eew_banner.innerText = "Earthquake Early Warning (Forecast)";
            } else if (parseInt(result["report_flag"]) == 1) {
                // EEW
                window.DOM.eew_banner_div.style.background = "var(--intensity-8)";
                window.DOM.eew_banner.innerText = "Earthquake Early Warning (Warning) - Strong Shaking Expected";
            }
        }
        if (result["max_intensity"] == "0" || result["is_plum"]) {
            window.DOM.eew_advice.style.background = "var(--info-background-color)";
            window.DOM.eew_advice.innerText = "Wait for further information";
        } else if (parseInt(result["hypocenter"]["depth"].slice(0, -2)) >= 100) {
            window.DOM.eew_advice.style.background = "#C37807";
            window.DOM.eew_advice.innerText = "Deep earthquake - Information may not be accurate";
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
    }

    deleteAllLayers();
    addEpicenter(result["hypocenter"]["latitude"], result["hypocenter"]["longitude"]);

    if (result["area_coloring"]["recommended_areas"]) {
        if (!_.isEqual({}, result["area_coloring"]["areas"]) ) {
            addMapIntensities(result["area_coloring"]["areas"]);
            addMapColoring(result["area_coloring"]["areas"]);
        } else {
            console.warn("Areas equals null. Check server log.");
        }
    } else {
        if (result["area_intensity"] != {}) {
            addMapIntensities(result["area_intensity"]);
        } else {
            console.warn("No points exist. Check server log.");
        }
    }
    parseMapScale();
    window.DOM.expected_flag.style.display = "block";

    // S wave
    if (result["s_wave"] != null) {
        addSWaveCircle(result["hypocenter"], result["s_wave"]);
    } else {
        console.warn("S wave time equals null. Check server log.");
    }
    if (window.swave_circle != undefined) {
        window.swave_circle.bringToFront();
    } else {
        console.warn("Failed to bring the S wave circle to front. " +
            "Check backend code.");
    }


    // P wave
    if (result["p_wave"] != null) {
        addPWaveCircle(result["hypocenter"], result["p_wave"]);
    } else {
        console.warn("P wave time equals null. Check server log.");
    }
    if (window.pwave_circle != undefined) {
        window.pwave_circle.bringToFront();
    } else {
        console.warn("Failed to bring the P wave circle to front. " +
            "Check backend code.");
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
    magnitude.innerText = parseFloat(resp_content["magnitude"]).toFixed(1).toString();
};