var initializeDOM = function () {
    window.DOM = {};
    window.DOM.intensity_display_div = document.getElementById("intensity-display");
    window.DOM.eew_display_div = document.getElementById("eew-display");
    window.DOM.intensity_report_div = document.getElementById("intensity-report");
    window.DOM.earthquake_report_div = document.getElementById("earthquake-report");
    window.DOM.drill_flag = document.getElementById("drill-flag");
    window.DOM.expected_flag = document.getElementById("expected-flag");
    // Earthquake Report
    window.DOM.information_banner_div = document.getElementById("banner-description");
    window.DOM.information_banner = document.getElementById("banner-text");
    window.DOM.occur_time = document.getElementById("occur-time");
    window.DOM.intensity_report_occur_time = document.getElementById("int-report-occur-time");

    // Earthquake Early Warning
    window.DOM.eew_banner_div = document.getElementById("eew-banner");
    window.DOM.eew_banner = document.getElementById("eew-level");
    window.DOM.eew_report_number = document.getElementById("report-number");
    window.DOM.eew_advice = document.getElementById("eew-advice");
    window.DOM.eew_receive_time = document.getElementById("eew-receive-time");
};
window.onload = function () {
    try {
        initializeDOM();
        initializeMap();
        displayIntensityCode(0, false);
    } catch (e) {
        window.logger.fatal("Failed to initialize the map." + e);
    }

    setInterval(function () {
        getEqInfo();
    }, 2000);
};