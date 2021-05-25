var initializeDOM = function () {
    window.DOM = {};
    window.DOM.pages_now = document.getElementById("report-pages");
    window.DOM.pages_total = document.getElementById("report-final-pages");
    window.DOM.receive_time = document.getElementById("receive-time");
    window.DOM.tsunami_information = document.getElementById("tsunami-information");
    window.DOM.tsunami_overlay = document.getElementById("information-overlay");
};
window.onload = function () {
    try {
        initializeDOM();

    } catch (e) {
        console.error("Failed to initialize the information. ", e);
    }
    setInterval(function () {
        getTsunamiInfo();
    }, 3500);
};
function splitArray(arr, num) {
	var newArr = [];
	for (let i = 0; i < arr.length;) {
		newArr.push(arr.slice(i, i += num));
	}
	return newArr;
}