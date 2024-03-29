const LOCALE = {
    "en": {
        "js": {
            "map": {
                "japan_tsunami": {
                    "tsunami_warning": "Japan: Major Tsunami Warning / Tsunami Warning / Advisory In Effect",
                    "no_tsunami": "Japan: No Tsunami Expected",
                    "non_effective": "Japan: Light Sea Level Changes Expected - No Tsunami Expected",
                    "risk_evaluating": "Japan: Tsunami Risk Evaluating - Stay away from coastal areas",
                    "unknown_message": "Japan: Unknown message: "
                },
                "foreign_tsunami": {
                    "risk_evaluating": "Foreign: Tsunami Risk Evaluating",
                    "non_effective_nearby": "Foreign: Small non-effective tsunami possible near the source",
                    "warning_nearby": "Foreign: Tsunami possible near the source",
                    "warning_pacific": "Foreign: Tsunami possible in the Pacific Ocean",
                    "warning_pacific_wide": "Foreign: Tsunami possible in wide area of Pacific Ocean",
                    "warning_indian": "Foreign: Tsunami possible in the Indian Ocean",
                    "warning_indian_wide": "Foreign: Tsunami possible in wide area of Indian Ocean",
                    "potential": "Foreign: In general, tsunami is possible on this scale",
                },
                "eew": {
                    "cancel": "Previous Earthquake Early Warning had been cancelled",
                    "forecast": "Earthquake Early Warning (Forecast)",
                    "warning": "Earthquake Early Warning (Warning) - Strong Shaking Expected",
                    "unknown": "Unknown EEW (Probably PLUM, etc.)",
                    "wait_further_information": "Wait for further information",
                    "deep_earthquake": "Deep earthquake - Information may not be accurate",
                    "pay_attention": "Pay attention to coastal areas",
                    "stay_away": "Stay away from coastal areas",
                },
                "attribution": {
                    "prefix": "QuakeMap by AllenDa",
                    "add": "Map: Natural Earth | Map Data: JMA",
                }
            },
            "tsunami_info": {
                "preliminary": "TSUNAMI INFORMATION (PRELIMINARY)",
                "detailed": "TSUNAMI INFORMATION (DETAILED)",
                "none": "No tsunami warning in effect.",
                "wait": "Waiting for messages...",
                "none_title": "TSUNAMI INFORMATION",
                "major_wrn_flag": "MAJOR",
                "wrn_flag": "WRN",
                "adv_flag": "ADV",
                "unk_flag": "UNK",
            }
        },
        "html": {
            "map": {
                "title": "Quake Map",
                "dom": {
                    "intensity-label,eew-intensity-label": "Maximum Int.",
                    "intensity-report-label": "Intensity Report",
                    "int-report-occur-label": "Occurred at <span\n id=\"int-report-occur-time\">XXXX-XX-XX XX:XX</span>",
                    "eq-report-occur-label": "Occurred at <span id=\"occur-time\">XXXX-XX-XX XX:XX</span>",
                    "epicenter-label,eew-epicenter-label": "Epicenter",
                    "depth-label,eew-depth-label": "Depth",
                    "magnitude-label,eew-magnitude-label": "M",
                    "banner-text-domestic,banner-text-foreign,eew-level,eew-advice": "Fetching information...",
                    "drill-label": "Drill - Not Real Situation",
                    "expected-label": "Expected Intensity",
                    "eew-receive-label": "Received at <span id=\"eew-receive-time\">XXXX/XX/XX XX:XX</span>"
                }
            },
            "tsunami_info": {
                "title": "Tsunami Info",
                "dom": {
                    "tsunami-title": "Tsunami Information",
                    "receive-label": "Received at",
                    "evacuate-sign": "EVACUATE!",
                    "grade-indicator": "Grade",
                    "region-indicator": "Tsunami Forecast Region",
                    "arr-time-indicator": "Initial tsunami arrival time",
                    "height-indicator": "Height",
                    "information-overlay": "Waiting for messages..."
                }
            }
        }
    },
    "zh": {
        "html": {
            "map": {
                "title": "地震地图",
                "dom": {
                    "intensity-label,eew-intensity-label": "最大震度",
                    "intensity-report-label": "震级速报",
                    "int-report-occur-label": "于 <span\n id=\"int-report-occur-time\">XXXX-XX-XX XX:XX</span> 发生",
                    "eq-report-occur-label": "于 <span id=\"occur-time\">XXXX-XX-XX XX:XX</span> 发生",
                    "epicenter-label,eew-epicenter-label": "震源",
                    "depth-label,eew-depth-label": "深度",
                    "magnitude-label,eew-magnitude-label": "震级",
                    "banner-text-domestic,banner-text-foreign,eew-level,eew-advice": "获取信息中……",
                    "drill-label": "训练 - 非真实情况",
                    "expected-label": "预计震度",
                    "eew-receive-label": "于 <span id=\"eew-receive-time\">XXXX/XX/XX XX:XX</span> 接收"
                }
            },
            "tsunami_info": {
                "title": "海啸预报信息",
                "dom": {
                    "tsunami-title": "海啸预报信息",
                    "receive-label": "接收于",
                    "evacuate-sign": "避难!",
                    "grade-indicator": "等级",
                    "region-indicator": "海啸预报区域",
                    "arr-time-indicator": "第一波海啸到达时间",
                    "height-indicator": "高度",
                    "information-overlay": "等待消息..."
                }
            }
        }
    }
};
let selectLocale = () => {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == "locale") {
            let content = pair[1];
            if (LOCALE[content] === undefined) {
                window.CURRENT_LOCALE = LOCALE["en"];
                return;
            } else {
                window.CURRENT_LOCALE = LOCALE[content];
                return;
            }
        }
    }
    window.CURRENT_LOCALE = LOCALE["en"];
};
let applyLocale = (module_name) => {
    // TODO: Apply on JS
    const currentModuleLocale = window.CURRENT_LOCALE.html[module_name];
    document.title = currentModuleLocale.title;
    for (var i in currentModuleLocale.dom) {
        console.log(i);
        const content = currentModuleLocale.dom[i];
        const toApplyIds = i.split(",");
        toApplyIds.forEach(id => {
            document.getElementById(id).innerHTML = content;
        });
    }
};
let initializeLocale = (module_name) => {
    selectLocale();
    applyLocale(module_name);
};
