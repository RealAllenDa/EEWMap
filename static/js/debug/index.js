String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{([0-9]+)}/g, function (match, index) {
        return typeof args[index] == 'undefined' ? match : args[index];
    });
};
var validation_date = /(\d{4})(0\d|1[0-2])([0-2]\d|3[0-1])([0-1]\d|2[0-3])([0-5]\d)([0-5]\d)/gm;


window.DEBUG_TOOLS = {};
window.DEBUG_TOOLS.urls = {
    "p2p": {
        "enable": "/debug/p2p/enable",
        "disable": "/debug/p2p/disable",
        "send_message": "/debug/p2p/send_message/{0}",

        "status": "/debug/p2p/status"
    },
    "eew": {
        "start": "/debug/eew/start",
        "end": "/debug/eew/end",
        "set_time": "/debug/eew/set_time/{0}",

        "status": "/debug/eew/status"
    }
};
window.DEBUG_TOOLS.events = {
    "p2p_debug_switch": p2p_debugSwitch_onclick,
    "eew_control_start": eew_controlStart_onclick,
    "eew_control_end": eew_controlEnd_onclick,
    "eew_test_date_set": eew_setTime_onclick,
    "p2p_info_send": p2p_messageSend_onclick
};
window.DEBUG_TOOLS.doms = {
    "p2p": {
        "switch": "p2p_debug_switch",
        "overlay": "p2p_debug_overlay"
    }
};


function initializeDOM() {
    window.DOM = {};
    window.DOM.eew_control_start = document.getElementById("eew-start-button");
    window.DOM.eew_control_end = document.getElementById("eew-end-button");
    window.DOM.eew_test_date = document.getElementById("eew-test-date");
    window.DOM.eew_test_date_set = document.getElementById("eew-set-test-date-button");

    window.DOM.p2p_debug_switch = document.getElementById("p2p-debug-on");
    window.DOM.p2p_debug_overlay = document.getElementById("p2p-debug-overlay");
    window.DOM.p2p_info_list = document.getElementById("p2p-info-type-select");
    window.DOM.p2p_info_send = document.getElementById("p2p-info-send");
}

function p2p_messageSend_onclick() {
    debuggingCommand("p2p", "send_message", window.DOM.p2p_info_list.value);
}

function p2p_debugSwitch_onclick() {
    var checked = window.DOM.p2p_debug_switch.checked;
    if (checked) {
        debuggingCommand("p2p", "enable");
        debuggingGetState("p2p", "status", statusCallback);
    } else {
        debuggingCommand("p2p", "disable");
        debuggingGetState("p2p", "status", statusCallback);
    }
    return false;
}

function eew_controlStart_onclick() {
    debuggingCommand("eew", "start");
}

function eew_controlEnd_onclick() {
    debuggingCommand("eew", "end");
}

function eew_setTime_onclick() {
    var date = window.DOM.eew_test_date.value;
    if (date.length == 14 && date.match(validation_date) != null) {
        debuggingCommand("eew", "set_time", date);
    } else {
        toastr.error("Date format doesn't match.");
    }
}

function initializeTriggers() {
    for (var i in window.DEBUG_TOOLS.events) {
        window.DOM[i].addEventListener("click", window.DEBUG_TOOLS.events[i]);
    }
}

function statusCallback(msg, module) {
    changeOverlayStatus(msg != "False", module);
}

function changeOverlayStatus(display, module) {
    var moduleSwitch = window.DOM[window.DEBUG_TOOLS.doms[module]["switch"]];
    var moduleOverlay = window.DOM[window.DEBUG_TOOLS.doms[module]["overlay"]];
    if (display) {
        moduleSwitch.checked = true;
        moduleOverlay.style.display = "block";
    } else {
        moduleSwitch.checked = false;
        moduleOverlay.style.display = "none";
    }
}

function initializeDefaults() {
    debuggingGetState("p2p", "status", statusCallback);
}

function debuggingCommand(module, api, ...arguments) {
    var url = window.DEBUG_TOOLS.urls[module][api].format(arguments);
    if (url === undefined) {
        toastr.error(`Failed to execute command ${module} - ${api}: Command not found`);
        return false;
    }
    $.ajax({
        type: "GET",
        url: url,
        timeout: 5000,
        success: function () {
            toastr.success(`Successfully executed ${url}`);
        },
        error: function (msg) {
            toastr.error(`Failed to execute ${url}: ${msg.status}: ${msg.statusText}`);
        }
    });
    return true;
}

function debuggingGetState(module, api, callback) {
    var url = window.DEBUG_TOOLS.urls[module][api].format(arguments);
    if (url === undefined) {
        toastr.error(`Failed to execute command ${module} - ${api}: Command not found`);
        return false;
    }
    $.ajax({
        type: "GET",
        url: url,
        timeout: 5000,
        success: function (msg) {
            callback(msg, module);
        },
        error: function (msg) {
            toastr.error(`Failed to execute ${url}: ${msg.status}-${msg.statusText}`);
        }
    });
}

window.onload = function () {
    initializeDOM();
    initializeTriggers();
    initializeDefaults();
};