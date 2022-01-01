var displayIntensityCode = function (intensity, is_eew) {
    /*
    * For intensity 1, 2, 3, 4, 7, Unknown: Add margin
    * For intensity 3, 4, 5-, 5+: Set text color to black, others to white
    * For intensity 5-, 5+, 6-, 6+: Set intensity add
    * */
    var intensity_code_box = document.getElementById("intensity-icon");
    var intensity_code = document.getElementById("intensity");
    var intensity_code_add = document.getElementById("intensity-add");
    if (is_eew) {
        intensity_code_box = document.getElementById("eew-intensity-icon");
        intensity_code = document.getElementById("eew-intensity");
        intensity_code_add = document.getElementById("eew-intensity-add");
    }
    // 1=1, 2=2, 3=3, 4=4, 5=5-, 6=5+, 7=6-, 8=6+, 9=7, 0=Unknown
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
    if ([0, "-1", "1", "2", "3", "4", "7"].indexOf(intensity) != -1) {
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
    } else if (intensity == "-1" || intensity == 0 || isNaN(intensity) || intensity == "NaN") {
        intensity_code.innerText = "--";
    } else {
        intensity_code.innerText = intensity;
    }
};
var setBannerContent = function (commentId) {
    console.log("Comment ids: ", commentId);
    let domesticId = commentId["domestic"];
    let foreignId = commentId["foreign"];
    // noinspection LoopStatementThatDoesntLoopJS,JSUnusedAssignment
    if (domesticId == "Warning") {
        // Major tsunami warning / ... has been issued
        window.DOM.domestic_information_banner.style.color = "white";
        window.DOM.domestic_information_banner_div.style.backgroundColor = "var(--intensity-7)";
        window.DOM.domestic_information_banner.innerText = "Japan: Major Tsunami Warning / Tsunami Warning / Advisory In Effect";
    } else if (domesticId == "None") {
        // No tsunami
        window.DOM.domestic_information_banner.style.color = "white";
        window.DOM.domestic_information_banner_div.style.backgroundColor = "#66cccc";
        window.DOM.domestic_information_banner.innerText = "Japan: No Tsunami Expected";
    } else if (domesticId == "NonEffective") {
        // Light sea changes are expected
        window.DOM.domestic_information_banner.style.color = "black";
        window.DOM.domestic_information_banner_div.style.backgroundColor = "var(--intensity-4)";
        window.DOM.domestic_information_banner.innerText = "Japan: Light Sea Level Changes Expected - No Tsunami Expected";
    } else if (domesticId == "Checking") {
        // Evaluating
        window.DOM.domestic_information_banner.style.color = "white";
        window.DOM.domestic_information_banner_div.style.backgroundColor = "var(--intensity-6)";
        window.DOM.domestic_information_banner.innerText = "Japan: Tsunami Risk Evaluating - Stay away from coastal areas";
    } else {
        // Unknown
        window.DOM.domestic_information_banner.style.color = "white";
        window.DOM.domestic_information_banner_div.style.backgroundColor = "var(--info-background-color)";
        window.DOM.domestic_information_banner.innerText = "Japan: Unknown message: " + commentId;
    }

    if (foreignId == "None") {
        // No tsunami
        window.DOM.foreign_information_banner_div.style.display = "none";
    } else {
        window.DOM.foreign_information_banner_div.style.display = "block";
        if (foreignId == "Checking") {
            // Evaluating
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-6)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Tsunami Risk Evaluating";
        } else if (foreignId == "NonEffectiveNearby") {
            // Maybe tsunami waves near the earthquake, non effective
            window.DOM.foreign_information_banner.style.color = "black";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-4)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Small non-effective tsunami possible near the source";
        } else if (foreignId == "WarningNearby") {
            // Tsunami waves near the earthquake
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Tsunami possible near the source";
        } else if (foreignId == "WarningPacific") {
            // Tsunami waves near pacific ocean
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Tsunami possible in the Pacific Ocean";
        } else if (foreignId == "WarningPacificWide") {
            // Tsunami waves across pacific ocean
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Tsunami possible in wide area of Pacific Ocean";
        } else if (foreignId == "WarningIndian") {
            // Tsunami waves near indian ocean
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Tsunami possible in the Indian Ocean";
        } else if (foreignId == "WarningIndianWide") {
            // Tsunami waves across indian ocean
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.foreign_information_banner.innerText = "Foreign: Tsunami possible in wide area of Indian Ocean";
        } else if (foreignId == "Potential") {
            // Tsunami is possible
            window.DOM.foreign_information_banner.style.color = "white";
            window.DOM.foreign_information_banner_div.style.backgroundColor = "var(--intensity-7)";
            window.DOM.foreign_information_banner.innerText = "Foreign: In general, tsunami is possible on this scale";
        }
    }
};