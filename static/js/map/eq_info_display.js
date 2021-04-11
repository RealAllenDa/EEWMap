var displayIntensityCode = function (intensity, is_eew) {
    var intensity_code_box = document.getElementById("intensity-icon");
    var intensity_code = document.getElementById("intensity");
    var intensity_code_add = document.getElementById("intensity-add");
    if (is_eew) {
        intensity_code_box = document.getElementById("eew-intensity-icon");
        intensity_code = document.getElementById("eew-intensity");
        intensity_code_add = document.getElementById("eew-intensity-add");
    }
    // 1=1, 2=2, 3=3, 4=4, 5=5-, 6=5+, 7=6-, 8=6+, 9=7, 0=Unknown
    /*
    * For intensity 1, 2, 3, 4, 7, Unknown: Add margin
    * For intensity 3, 4, 5-, 5+: Set text color to black, others to white
    * For intensity 5-, 5+, 6-, 6+: Set intensity add
    * */
    switch (intensity) {
        case "1":
        case "2":
        case "3":
        case "4":
            intensity_code_box.style.backgroundColor = "var(--intensity-" + intensity + ")";
            break;
        case "5-":
            intensity_code_box.style.backgroundColor = "var(--intensity-5)";
            break;
        case "5+":
            intensity_code_box.style.backgroundColor = "var(--intensity-6)";
            break;
        case "6-":
            intensity_code_box.style.backgroundColor = "var(--intensity-7)";
            break;
        case "6+":
            intensity_code_box.style.backgroundColor = "var(--intensity-8)";
            break;
        case "7":
            intensity_code_box.style.backgroundColor = "var(--intensity-9)";
            break;
        default:
            intensity_code_box.style.backgroundColor = "var(--info-background-color)";
    }
    // Set background color
    if ([0, "1", "2", "3", "4", "7"].indexOf(intensity) != -1) {
        // Add margin
        intensity_code.className = "intensity-display margin-add";
    } else {
        intensity_code.className = "intensity-display";
    }
    if (["3", "4", "5-", "5+"].indexOf(intensity) != -1) {
        // Text color to black
        intensity_code_box.style.color = "black";
    } else {
        // Text color to white
        intensity_code_box.style.color = "white";
    }
    if (["5-", "6-"].indexOf(intensity) != -1) {
        // Add intensity -
        intensity_code_add.innerText = "-";
    } else if (["5+", "6+"].indexOf(intensity) != -1) {
        // Add intensity +
        intensity_code_add.innerText = "+";
    } else {
        // Clear intensity +/-
        intensity_code_add.innerText = "";
    }
    if (["5-", "5+"].indexOf(intensity) != -1) {
        intensity_code.innerText = "5";
    } else if (["6-", "6+"].indexOf(intensity) != -1) {
        intensity_code.innerText = "6";
    } else if (intensity == "7") {
        intensity_code.innerText = "7";
    } else if (intensity == 0 || isNaN(intensity) || intensity == "NaN") {
        intensity_code.innerText = "--";
    } else {
        intensity_code.innerText = intensity;
    }
};
var setBannerContent = function (commentId, commentText) {
    var commentIds = commentId.split(" ");
    console.log(commentIds);
    // noinspection LoopStatementThatDoesntLoopJS,JSUnusedAssignment
    for (var i = 0; i < commentIds.length; i++) {
        commentId = parseInt(commentIds[i]);
        if (commentId == 211) {
            // Major tsunami warning / ... has been issued
            window.DOM.information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.information_banner.innerText = "Major Tsunami Warning / Tsunami Warning / Advisory In Effect";
            return;
        } else if (commentId == 215) {
            // No tsunami
            window.DOM.information_banner_div.style.backgroundColor = "#66cccc";
            window.DOM.information_banner.innerText = "No Tsunami Expected";
            return;
        } else if (commentId == 217) {
            // Evaluating
            window.DOM.information_banner_div.style.backgroundColor = "var(--intensity-6)";
            window.DOM.information_banner.innerText = "Tsunami Risk Evaluating - Stay away from coastal areas";
            return;
        } else if (commentId == 999) {
            // Train
            window.DOM.information_banner_div.style.backgroundColor = "var(--intensity-2)";
            window.DOM.information_banner.innerText = "Drill - Not Real Situation";
            return;
        } else if (commentId == 221 || commentId == 229) {
            // Evaluating (Overseas)
            window.DOM.information_banner_div.style.backgroundColor = "var(--intensity-6)";
            window.DOM.information_banner.innerText = "Overseas Earthquake - Japan tsunami risk evaluating";
            return;
        } else {
            // Unknown
            window.DOM.information_banner_div.style.backgroundColor = "var(--info-background-color)";
            window.DOM.information_banner.innerText = commentText;
            return;
        }
    }
};