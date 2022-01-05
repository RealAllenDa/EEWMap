class HNSdk {
    constructor() {
        this.urlParams = new URLSearchParams(window.location.search);
    }

    getUrlParams(param) {
        return this.urlParams.get(param);
    }
}

window.__HN_SDK__ = new HNSdk();