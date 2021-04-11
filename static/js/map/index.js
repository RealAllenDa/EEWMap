var initializeDOM = function () {
    window.DOM = {};
    window.DOM.intensity_display_div = document.getElementById("intensity-display");
    window.DOM.eew_display_div = document.getElementById("eew-display");
    window.DOM.intensity_report_div = document.getElementById("intensity-report");
    window.DOM.earthquake_report_div = document.getElementById("earthquake-report");
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
    initializeDOM();
    initializeMap();
    displayIntensityCode(0, false);
    setInterval(function () {
        getJmaXML();
    }, 3000);
};
var compare = function (obj1, obj2) {
    if (obj1 === obj2) return true;
    if (typeof obj1 === "function" && typeof obj2 === "function") return obj1.toString() === obj2.toString();
    if (obj1 instanceof Date && obj2 instanceof Date) return obj1.getTime() === obj2.getTime();
    if ( Object.prototype.toString.call(obj1) !==Object.prototype.toString.call(obj2) || typeof obj1 !== "object") return false;
    const obj1Props = Object.getOwnPropertyNames(obj1);
    const obj2Props = Object.getOwnPropertyNames(obj2);
    if(obj1Props.length !== obj2Props.length) return false;
    return (obj1Props.every(prop => compare(obj1[prop], obj2[prop])));
};