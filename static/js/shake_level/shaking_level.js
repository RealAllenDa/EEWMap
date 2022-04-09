window.onload = function () {
    window.level_display_div = document.getElementById("shaking-level");
    window.level_display_wrap = document.getElementById("shaking-level-wrap");
    window.green = document.getElementById("green-label");
    window.green_bg = document.getElementById("green");
    window.green_count = document.getElementById("green-count");
    window.yellow = document.getElementById("yellow-label");
    window.yellow_bg = document.getElementById("yellow");
    window.yellow_count = document.getElementById("yellow-count");
    window.red = document.getElementById("red-label");
    window.red_bg = document.getElementById("red");
    window.red_count = document.getElementById("red-count");
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
        window.green_bg.style.color = "white";
        window.green_count.style.background = "var(--info-background-color)";
        window.green.style.background = "var(--info-background-color)";
        window.yellow_bg.style.color = "white";
        window.yellow.style.background = "var(--info-background-color)";
        window.yellow_count.style.background = "var(--info-background-color)";
        window.red_bg.style.color = "white";
        window.red.style.background = "var(--info-background-color)";
        window.red_count.style.background = "var(--info-background-color)";
        window.green_count.innerText = "--";
        window.yellow_count.innerText = "--";
        window.red_count.innerText = "--";
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
        } else if (result["shake_level"] >= 3000 && result["shake_level"] < 4000) {
            window.level_display_wrap.style.backgroundColor = "var(--shake-3000)";
            window.level_display_wrap.style.color = "white";
        } else if (result["shake_level"] >= 4000) {
            window.level_display_wrap.style.backgroundColor = "black";
            window.level_display_wrap.style.color = "yellow";
        } else {
            window.level_display_wrap.style.backgroundColor = "var(--info-background-color)";
            window.level_display_wrap.style.color = "white";
        }

        window.green_count.innerText = result["green"];
        window.yellow_count.innerText = result["yellow"];
        window.red_count.innerText = result["red"];
        if (result["green"] >= 350) {
            window.green_count.style.background = "var(--green-warn)";
            window.green.style.background = "var(--green-warn-label)";
            window.green_bg.style.color = "black";
        } else {
            window.green_bg.style.color = "white";
            window.green_count.style.background = "var(--info-background-color)";
            window.green.style.background = "var(--info-background-color)";
        }
        if (result["yellow"] >= 30) {
            window.yellow_count.style.background = "var(--yellow-warn)";
            window.yellow.style.background = "var(--yellow-warn-label)";
            window.yellow_bg.style.color = "black";
        } else {
            window.yellow_bg.style.color = "white";
            window.yellow.style.background = "var(--info-background-color)";
            window.yellow_count.style.background = "var(--info-background-color)";
        }
        if (result["red"] >= 5) {
            window.red_count.style.background = "var(--red-warn)";
            window.red.style.background = "var(--red-warn-label)";
            window.red_bg.style.color = "black";
        } else {
            window.red_bg.style.color = "white";
            window.red.style.background = "var(--info-background-color)";
            window.red_count.style.background = "var(--info-background-color)";
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
