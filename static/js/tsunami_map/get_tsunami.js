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
        console.log(456);
        if (_.isEqual([], result["info"]["areas"])) {
            resetTsunami();
            return;
        }
        window.DOM.title.innerText = "TSUNAMI INFORMATION (DETAILED)";
        window.DOM.report_origin.innerText = result["info"]["origin"];
        setTsunamiInfo(result["info"]);
    } else if (parseInt(result["status"]) != 0 && !(_.isEqual({}, result["map"]))) {
        console.log(123);
        window.DOM.title.innerText = "TSUNAMI INFORMATION (PRELIMINARY)";
        window.DOM.report_origin.innerText = "P2P";
        var area_geojson = result["map"]["areas"]["features"];
        var receive_time = result["map"]["time"];
        var result_areas = [];
        for (var i = 0; i < area_geojson.length; i++) {
            if (area_geojson[i]["properties"]["name"] != "帰属未定1" &&
                area_geojson[i]["properties"]["name"] != "帰属未定2" &&
                area_geojson[i]["properties"]["name"] != "帰属未定3" &&
                area_geojson[i]["properties"]["name"] != "帰属未定4") {
                result_areas.push({
                    "name": area_geojson[i]["properties"]["name"],
                    "grade": area_geojson[i]["properties"]["grade"],
                    "height": "Unknown",
                    "time": {
                        "type": "no_time",
                        "time": ""
                    }
                });
            }
        }
        var result_combined = {
            "areas": customSort({
                data: result_areas,
                sortBy: sortByLevel,
                sortField: "grade"
            }),
            "receive_time": receive_time
        };
        console.log(result_combined);
        setTsunamiInfo(result_combined);
    } else {
        console.log(789);
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
    window.DOM.tsunami_overlay.innerText = "No tsunami warning in effect.";
    window.DOM.title.innerText = "TSUNAMI INFORMATION";
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