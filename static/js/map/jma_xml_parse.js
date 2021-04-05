var getJmaXML = function () {
    $.ajax({
        type: "GET",
        url: "/get_jma_xml",
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
    *  5 - Tsunami Warning (VTSE51/41)
    *  */
    // TODO: Tsunami Warning Check
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
    if (result["status"] == 0) {
        displayEarthquakeInformation(resp_content);
        deleteAllIcons();
        if (resp_content["is_overseas"] == false) {
            displayIntensityCode(resp_content["max_intensity"]);
            parseMapScale(resp_content["area_intensity"], resp_content["hypocenter"]["latitude"], resp_content["hypocenter"]["longitude"]);
            addMapIntensities(resp_content["area_intensity"]);
            addEpicenter(resp_content["hypocenter"]["latitude"],
                resp_content["hypocenter"]["longitude"]);
        } else {
            displayIntensityCode(0);
            addEpicenter(resp_content["hypocenter"]["latitude"], resp_content["hypocenter"]["longitude"]);
            window.map.setZoom(2);
            // TODO: Fix
            window.map.panTo([parseInt(resp_content["hypocenter"]["latitude"]), parseInt(resp_content["hypocenter"]["longitude"])]);
        }
    } else if (result["status"] == 1) {
        window.DOM.intensity_report_div.style.display = "block";
        window.DOM.earthquake_report_div.style.display = "none";
        window.DOM.intensity_report_occur_time.innerText = resp_content["occur_time"];
        displayIntensityCode(resp_content["max_intensity"]);
        parseMapScale(resp_content["area_intensity"], 0, 0);
        deleteAllIcons();
        addMapIntensities(resp_content["area_intensity"]);
        setBannerContent(resp_content["tsunami_comments"]["code"], resp_content["tsunami_comments"]["text"]);
    } else if (result["status"] == 2) {
        displayEarthquakeInformation(resp_content);
    }
    if (result["content"]["is_test"] == true) {
        setBannerContent(999);
    }
};
var displayEarthquakeInformation = function (resp_content) {
    window.DOM.intensity_report_div.style.display = "none";
    window.DOM.earthquake_report_div.style.display = "block";
    window.DOM.epicenter.innerText = resp_content["hypocenter"]["name"];
    window.DOM.depth.innerText = resp_content["hypocenter"]["depth"];
    window.DOM.magnitude.innerText = resp_content["magnitude"];
    window.DOM.occur_time.innerText = resp_content["occur_time"];
    setBannerContent(resp_content["tsunami_comments"]["code"], resp_content["tsunami_comments"]["text"]);
};