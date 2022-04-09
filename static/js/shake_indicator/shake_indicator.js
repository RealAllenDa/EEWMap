window.onload = function () {
    window.warning_indicator = document.getElementById("warning-indicator");
    window.caution_indicator = document.getElementById("caution-indicator");
    setInterval(function () {
        getShakeWarning();
    }, 2500);
};
var shakeWarningShow = function (result) {
    if (result["status"] == -1) {
        window.warning_indicator.className = "shake-indicator";
        window.caution_indicator.className = "shake-indicator";
    } else if (result["status"] == 0) {
        if (result["red"] >= 5) {
            window.warning_indicator.className = "shake-indicator indicator-active";
        } else {
            window.warning_indicator.className = "shake-indicator";
            if (result["yellow"] >= 30) {
                window.caution_indicator.className = "shake-indicator indicator-active";
            } else {
                window.caution_indicator.className = "shake-indicator";
            }
        }
    }
    console.log(result);
};
var getShakeWarning = function () {
    $.ajax({
        type: "GET",
        url: "/api/shake_level",
        dataType: "JSON",
        cache: false,
        timeout: 2500,
        success: shakeWarningShow
    });
};
