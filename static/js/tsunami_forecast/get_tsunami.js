// --- UTILITIES START
const customSort = ({data, sortBy, sortField}) => {
    const sortByObject = sortBy.reduce(
        (obj, item, index) => ({
            ...obj,
            [item]: index
        }),
        {}
    );
    return data.sort(
        (a, b) => sortByObject[a[sortField]] - sortByObject[b[sortField]]
    );
};

function isObj(obj) {
    return obj instanceof Object;
}

function deepCopyObj2NewObj(fromObj, toObj) {
    for (var key in fromObj) {
        if (fromObj.hasOwnProperty(key)) {
            var fromValue = fromObj[key];
            if (!isObj(fromValue)) {
                toObj[key] = fromValue;
            } else {
                var tmpObj = new fromValue.constructor;
                deepCopyObj2NewObj(fromValue, tmpObj);
                toObj[key] = tmpObj;
            }
        }
    }
}

var sortByArrivalTime = function (array_for_sort) {
    var area_entries = [];
    Object.entries(array_for_sort).forEach((content) => {
            // noinspection JSCheckFunctionSignatures
            area_entries.push(Object.entries(content[1]));
        }
    );
    area_entries.sort((f1, f2) => {
        var time_f1 = f1[3][1];
        var time_f2 = f2[3][1];
        if (time_f1["type"] == "no_time" && time_f2["type"] == "time") {
            return 99;
        } else if (time_f1["type"] == "time" && time_f2["type"] == "no_time") {
            return -99;
        } else if (time_f1["type"] == "no_time" && time_f2["type"] == "no_time") {
            return time_f1["status"] - time_f2["status"];
        } else {
            return time_f1["timestamp"] - time_f2["timestamp"];
        }
    });
    area_entries = area_entries.reverse();
    var area_sorted = [];
    area_entries.forEach((content) => {
        area_sorted.push(Object.fromEntries(content));
    });
    return area_sorted;
};
const sortByLevel = ["MajorWarning", "Warning", "Watch"];
// --- UTILITIES END

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
    if (_.isEqual(last_message, result)) {
        console.debug("Identical information. No need to update.");
    } else {
        last_message = result;
        console.debug("Updated message. Parsing...");
        parseTsunamiInfo(result);
    }
};
var parseTsunamiInfo = function (result) {
    if (parseInt(result["status_forecast"]) != 0
        && !_.isEqual({}, result["info"])) {
        console.log("Parsing detailed tsunami info...");
        if (_.isEqual([], result["info"]["forecast_areas"])) {
            resetTsunami();
            return;
        }
        window.DOM.report_origin.innerText = result["info"]["origin"];
        var sorted_result = {
            "areas": result["info"]["forecast_areas"],
            "origin": result["info"]["origin"],
            "receive_time": result["info"]["receive_time"]
        };
        setTsunamiInfo(sorted_result);
    } else {
        console.log("No tsunami messages.");
        resetTsunami();
    }
};
var setTsunamiInfo = function (result) {
    // Tsunami warning in effect
    if (window.tsunami_show != undefined) {
        clearInterval(window.tsunami_show);
        clearTsunamiInfo();
    }
    window.DOM.tsunami_overlay.style.display = "none";
    window.DOM.receive_time.innerText = result["receive_time"];
    var array_split = splitArray(result["areas"], 7);
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
    }, 10000);
};
var resetTsunami = function () {
    clearInterval(window.tsunami_show);
    window.DOM.tsunami_overlay.style.display = "block";
    clearTsunamiInfo();
    window.DOM.pages_now.innerText = "--";
    window.DOM.pages_total.innerText = "--";
    window.DOM.receive_time.innerText = "XXXX/XX/XX XX:XX";
    window.DOM.tsunami_overlay.innerText = "No tsunami forecast in effect.";
    window.DOM.report_origin.innerText = "--";
};
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
        var tsunami_height = document.createElement("div");
        tsunami_container.className = "tsunami-item";
        tsunami_container.id = "tsunami-" + i.toString();
        tsunami_grade.innerText = "FC";
        tsunami_grade.className = "forecast-tsunami";
        tsunami_height.className = "forecast-tsunami";
        tsunami_name.innerText = array[i]["name"];
        tsunami_height.innerText = "Less than 0.2m";
        tsunami_container.appendChild(tsunami_grade);
        tsunami_container.appendChild(tsunami_name);
        tsunami_container.appendChild(tsunami_height);
        window.DOM.tsunami_information.appendChild(tsunami_container);
        tsunami_messages_DOMs[i] = document.getElementById("tsunami-" + i.toString());
    }
};