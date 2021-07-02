var checkTime = function (i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
};
var Logger = function (default_level) {
    this.LEVELS = {
        "DEBUG": 0,
        "INFO": 1,
        "WARN": 2,
        "ERROR": 3,
        "FATAL": 4
    };
    try {
        this.level = this.LEVELS[default_level];
    } catch (e) {
        console.error("Failed to initialize logger: ", e);
    }
    // noinspection JSUnusedGlobalSymbols
    this.setLevel = function (new_level) {
        try {
            if (this.LEVELS[new_level] === undefined) {
                console.warn("Level equals undefined. Level left unchanged.");
                return;
            }
            this.level = this.LEVELS[new_level];
            console.log("Successfully changed to level: " + this.level + " => " + new_level);
        } catch (e) {
            console.warn("Failed to change log level: ", e);
        }
    };
    this.debug = function (str) {
        this._message(this.debug.caller.name, this.LEVELS["DEBUG"], str);
    };
    this.info = function (str) {
        this._message(this.info.caller.name, this.LEVELS["INFO"], str);
    };
    this.warn = function (str) {
        this._message(this.warn.caller.name, this.LEVELS["WARN"], str);
    };
    this.error = function (str) {
        this._message(this.error.caller.name, this.LEVELS["ERROR"], str);
    };
    // noinspection JSUnusedGlobalSymbols
    this.fatal = function (str) {
        this._message(this.fatal.caller.name, this.LEVELS["FATAL"], str);
    };
    this._message = function (module, level, str) {
        // Format: [DateTime] [CurrentProcessTime] [ Level ]: [Message]
        if (level >= this.level) {
            var dateTime = new Date();
            var dateString = dateTime.getFullYear() + "-" +
                checkTime(dateTime.getMonth() + 1) + "-" +
                checkTime(dateTime.getDay()) + " " +
                checkTime(dateTime.getHours()) + ":" +
                checkTime(dateTime.getMinutes()) + ":" +
                checkTime(dateTime.getSeconds()) + "." +
                dateTime.getMilliseconds();
            try {
                switch (level) {
                    case 0:
                        console.log("[" + dateString + "]", "[" + module + "]", "[ DEBUG ]:", str);
                        break;
                    case 1:
                        console.log("[" + dateString + "]", "[" + module + "]", "[ INFO ]:", str);
                        break;
                    case 2:
                        console.warn("[" + dateString + "]", "[" + module + "]", "[ WARNING ]:", str);
                        break;
                    case 3:
                        console.error("[" + dateString + "]", "[" + module + "]", "[ ERROR ]:", str);
                        break;
                    case 4:
                        console.error("[" + dateString + "]", "[" + module + "]", "[ FATAL ]:", str);
                        break;
                    default:
                        console.log("[" + dateString + "]", "[" + module + "]", "[ UNKNOWN ]:", str);
                }
            } catch (e) {
                console.error("Failed to print the log: ", e);
            }
        }
    }
};
window.logger = new Logger("DEBUG");