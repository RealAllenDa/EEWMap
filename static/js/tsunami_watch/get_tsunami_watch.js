var getTsunamiWatch = function () {
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
var tsunami_watches_DOMs = [];
var last_message = {};
var splitTsunamiInfo = function (result) {
    console.debug(result);
    var result_for_compare = result;
    if (_.isEqual(last_message, result_for_compare)) {
        console.debug("Identical information. No need to update.");
        return;
    } else {
        last_message = result_for_compare;
        console.debug("Updated message. Parsing...");
    }
    if (!_.isEqual({}, result["watch"])) {
        setWatchInfo(result["watch"]);
    } else {
        resetTsunami();
    }
};
var setWatchInfo = function (result) {
    // Tsunami warning in effect
    if (window.watch_show != undefined) {
        clearInterval(window.watch_show);
        clearWatchInfo();
    }
    window.DOM.tsunami_overlay.style.display = "none";
    window.DOM.receive_time.innerText = result["receive_time"];
    var array_split = splitArray(result["areas"], 7);
    console.log(array_split);
    var pages_total = array_split.length;
    var pages_now = 1;
    window.DOM.pages_total.innerText = pages_total.toString();
    // Display first to prevent waiting
    window.DOM.pages_now.innerText = pages_now.toString();
    clearWatchInfo();
    displayWatchInfo(array_split[pages_now - 1]);
    pages_now++;
    if (pages_now > pages_total) {
        pages_now = 1;
    }
    window.watch_show = setInterval(function () {
        window.DOM.pages_now.innerText = pages_now.toString();
        clearWatchInfo();
        displayWatchInfo(array_split[pages_now - 1]);
        pages_now++;
        if (pages_now > pages_total) {
            pages_now = 1;
        }
    }, 15000);
};
var resetTsunami = function () {
    clearInterval(window.watch_show);
    window.DOM.tsunami_overlay.style.display = "block";
    clearWatchInfo();
    window.DOM.pages_now.innerText = "--";
    window.DOM.pages_total.innerText = "--";
    window.DOM.receive_time.innerText = "XXXX/XX/XX XX:XX";
};
var clearWatchInfo = function () {
    for (var i = 0; i < tsunami_watches_DOMs.length; i++) {
        tsunami_watches_DOMs[i].remove();
    }
};
var displayWatchInfo = function (array) {
    for (var i = 0; i < array.length; i++) {
        var tsunami_container = document.createElement("div");
        var tsunami_name = document.createElement("div");
        var tsunami_time = document.createElement("div");
        var tsunami_height = document.createElement("div");
        var tsunami_status = document.createElement("div");
        tsunami_container.className = "tsunami-item";
        tsunami_container.id = "tsunami-" + i.toString();
        tsunami_name.innerText = array[i]["name"];
        if (array[i]["condition"] == "Observing") {
            tsunami_height.innerText = "Observing";
        } else if (array[i]["condition"] == "Weak") {
            tsunami_height.innerText = "Weak";
            tsunami_time.innerText = array[i]["time"];
        }
        if (array[i]["condition"] == "None") {
            tsunami_time.innerText = array[i]["time"];
            if (array[i]["height_is_max"]) {
                tsunami_height.innerText = "Over ";
            }
            tsunami_height.innerText += array[i]["height"];
            if (array[i]["height_condition"] == "Rising") {
                tsunami_status.innerText = "RISING";
                tsunami_status.className = "rising-alert";
            }
            if (parseFloat(array[i]["height"]) >= 5) {
                tsunami_container.className += " major-warning";
            } else if (parseFloat(array[i]["height"]) >= 3) {
                tsunami_container.className += " warning";
            } else if (parseFloat(array[i]["height"]) >= 1) {
                tsunami_container.className += " advisory";
            }
            tsunami_height.innerText += "m";
        }
        tsunami_container.appendChild(tsunami_name);
        tsunami_container.appendChild(tsunami_time);
        tsunami_container.appendChild(tsunami_height);
        tsunami_container.appendChild(tsunami_status);
        window.DOM.tsunami_information.appendChild(tsunami_container);
        tsunami_watches_DOMs[i] = document.getElementById("tsunami-" + i.toString());
    }
};