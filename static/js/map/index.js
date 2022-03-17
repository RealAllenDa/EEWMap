var initializeDOM = function () {
    window.DOM = {};
    window.DOM.intensity_display_div = document.getElementById("intensity-display");
    window.DOM.eew_display_div = document.getElementById("eew-display");
    window.DOM.intensity_report_div = document.getElementById("intensity-report");
    window.DOM.earthquake_report_div = document.getElementById("earthquake-report");
    window.DOM.drill_flag = document.getElementById("drill-flag");
    window.DOM.expected_flag = document.getElementById("expected-flag");
    // Earthquake Report
    window.DOM.domestic_information_banner_div = document.getElementById("banner-description-domestic");
    window.DOM.domestic_information_banner = document.getElementById("banner-text-domestic");
    window.DOM.foreign_information_banner_div = document.getElementById("banner-description-foreign");
    window.DOM.foreign_information_banner = document.getElementById("banner-text-foreign");
    window.DOM.occur_time = document.getElementById("occur-time");
    window.DOM.intensity_report_occur_time = document.getElementById("int-report-occur-time");
    window.DOM.depth_label = document.getElementById("depth-label");
    window.DOM.magnitude_label = document.getElementById("magnitude-label");

    // Earthquake Early Warning
    window.DOM.eew_banner_div = document.getElementById("eew-banner");
    window.DOM.eew_banner = document.getElementById("eew-level");
    window.DOM.eew_report_number = document.getElementById("report-number");
    window.DOM.eew_advice = document.getElementById("eew-advice");
    window.DOM.eew_receive_time = document.getElementById("eew-receive-time");
};
window.onload = function () {
    try {
        initializeLocale("map");
        initializeDOM();
        initializeMap();
        displayIntensityCode(0, false);
    } catch (e) {
        console.error("Failed to initialize the map." + e);
    }

    window.getEqInfoTimer = setInterval(function () {
        getEqInfo();
    }, 2000);
};