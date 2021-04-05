var initializeDOM = function () {
    window.DOM = {};
    window.DOM.intensity_code = document.getElementById("intensity");
    window.DOM.intensity_code_add = document.getElementById("intensity-add");
    window.DOM.intensity_code_box = document.getElementById("intensity-icon");
    window.DOM.information_banner = document.getElementById("banner-text");
    window.DOM.information_banner_div = document.getElementById("banner-description");
    window.DOM.occur_time = document.getElementById("occur-time");
    window.DOM.intensity_report_occur_time = document.getElementById("int-report-occur-time");
    window.DOM.epicenter = document.getElementById("epicenter");
    window.DOM.depth = document.getElementById("depth");
    window.DOM.magnitude = document.getElementById("magnitude");
    window.DOM.intensity_report_div = document.getElementById("intensity-report");
    window.DOM.earthquake_report_div = document.getElementById("earthquake-report");
};
window.onload = function () {
    initializeDOM();
    initializeMap();
    displayIntensityCode(0);
    setInterval(function () {
        getJmaXML();
    }, 3500);
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