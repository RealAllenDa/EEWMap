var getTsunamiInfo = function () {
    $.ajax({
        type: "GET",
        url: "/api/tsunami_info",
        cache: false,
        dataType: "JSON",
        timeout: 3500,
        success: splitTsunamiInfo,
        error: function () {
            console.warn("Failed to retrieve data.");
        }
    });
};
var last_message = {};
var tsunami_messages_DOMs = [];
var splitTsunamiInfo = function (result) {
    console.debug(result);
    var result_for_compare = result;
    if (_.isEqual(last_message, result_for_compare)) {
        console.debug("Identical information. No need to update.");
    } else {
        last_message = result_for_compare;
        console.debug("Updated message. Parsing...");
        parseTsunamiInfo(result);
    }
};
var parseTsunamiInfo = function (result) {
    if (parseInt(result["status"]) != 0
        && !_.isEqual({}, result["info"])) {
        if (_.isEqual([], result["info"]["areas"])) {
            resetTsunami();
            return;
        }
        // Tsunami warning in effect
        if (window.tsunami_show != undefined) {
            clearInterval(window.tsunami_show);
            clearTsunamiInfo();
        }
        window.DOM.tsunami_overlay.style.display = "none";
        window.DOM.receive_time.innerText = result["info"]["receive_time"];
        var array_split = splitArray(result["info"]["areas"], 7);
        var pages_total = array_split.length;
        var pages_now = 1;
        window.DOM.pages_total.innerText = pages_total.toString();
        // Display first to prevent waiting
        window.DOM.pages_now.innerText = pages_now.toString();
        clearTsunamiInfo();
        displayTsunamiInfo(array_split[pages_now - 1]);
        pages_now++;
        if (pages_now > pages_total) {
            pages_now = 1;
        }
        window.tsunami_show = setInterval(function () {
            window.DOM.pages_now.innerText = pages_now.toString();
            clearTsunamiInfo();
            displayTsunamiInfo(array_split[pages_now - 1]);
            pages_now++;
            if (pages_now > pages_total) {
                pages_now = 1;
            }
        }, 15000);
    } else {
        resetTsunami();
    }
};
var resetTsunami = function () {
    clearInterval(window.tsunami_show);
    window.DOM.tsunami_overlay.style.display = "block";
    clearTsunamiInfo();
    window.DOM.pages_now.innerText = "--";
    window.DOM.pages_total.innerText = "--";
    window.DOM.receive_time.innerText = "XXXX-XX-XX XX:XX";
    window.DOM.tsunami_overlay.innerText = "No tsunami warning in effect.";
}
var clearTsunamiInfo = function () {
    for (var i = 0; i < tsunami_messages_DOMs.length; i++) {
        tsunami_messages_DOMs[i].remove();
    }
};
var displayTsunamiInfo = function (array) {
    for (var i = 0; i < array.length; i++) {
        var tsunami_container = document.createElement("div");
        var tsunami_grade = document.createElement("div");
        var tsunami_name = document.createElement("div");
        var tsunami_time = document.createElement("div");
        var tsunami_height = document.createElement("div");
        tsunami_container.className = "tsunami-item";
        tsunami_container.id = "tsunami-" + i.toString();
        if (array[i]["grade"] == "MajorWarning") {
            tsunami_grade.innerText = "MAJOR";
            tsunami_grade.className = "major-tsunami-warn";
            tsunami_height.className = "major-tsunami-warn";
        } else if (array[i]["grade"] == "Warning") {
            tsunami_grade.innerText = "WRN";
            tsunami_grade.className = "tsunami-warn";
            tsunami_height.className = "tsunami-warn";
        } else if (array[i]["grade"] == "Watch") {
            tsunami_grade.innerText = "ADV";
            tsunami_grade.className = "tsunami-advisory";
            tsunami_height.className = "tsunami-advisory";
        } else {
            tsunami_grade.innerText = "UNK";
        }
        tsunami_name.innerText = array[i]["name"];
        tsunami_time.innerText = array[i]["time"]["time"];
        if (array[i]["height"] == "Unknown") {
            tsunami_height.className = "";
        } else {
            tsunami_height.innerText = array[i]["height"];
        }
        tsunami_container.appendChild(tsunami_grade);
        tsunami_container.appendChild(tsunami_name);
        tsunami_container.appendChild(tsunami_time);
        tsunami_container.appendChild(tsunami_height);
        window.DOM.tsunami_information.appendChild(tsunami_container);
        tsunami_messages_DOMs[i] = document.getElementById("tsunami-" + i.toString());
    }
};