window.onload = function () {
    window.level_display_div = document.getElementById("shaking-level");
    window.level_display_wrap = document.getElementById("shaking-level-wrap");
    window.last_time_fetch_success = 0;
    setInterval(function () {
        getShakeLevel();
    }, 2500);
};
var shakeLevelShow = function (result) {
    if (result["status"] == -1) {
        window.level_display_div.innerText = "---";
        window.level_display_wrap.style.backgroundColor = "var(--info-background-color)";
        window.level_display_wrap.style.color = "white";
    } else if (result["status"] == 0) {
        window.level_display_div.innerText = result["shake_level"];
        if (result["shake_level"] >= 50 && result["shake_level"] < 100) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-50)";
            window.level_display_wrap.style.color = "white";
        } else if (result["shake_level"] >= 100 && result["shake_level"] < 500) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-100)";
            window.level_display_wrap.style.color = "black";
        } else if (result["shake_level"] >= 500 && result["shake_level"] < 1000) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-500)";
            window.level_display_wrap.style.color = "white";
        } else if (result["shake_level"] >= 1000 && result["shake_level"] < 2000) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-1000)";
            window.level_display_wrap.style.color = "white";
        } else if (result["shake_level"] >= 2000 && result["shake_level"] < 3000) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-2000)";
            window.level_display_wrap.style.color = "white";
        } else if (result["shake_level"] >= 3000) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-3000)";
            window.level_display_wrap.style.color = "white";
        } else {
            window.level_display_wrap.style.backgroundColor = "var(--info-background-color)";
            window.level_display_wrap.style.color = "white";
        }

    }
    console.log(result);
};
var getShakeLevel = function () {
    $.ajax({
        type: "GET",
        url: "/api/shake_level",
        dataType: "JSON",
        cache: false,
        timeout: 2500,
        success: shakeLevelShow
    });
};
