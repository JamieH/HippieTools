doLog = false;

function BYONDDebug() {
    this.logWindow = window.open();
    if (this.logWindow == null || !doLog) {
        console.log("Error loading logger");
        this.Log = function(message) {console.log(message);}
        return
    }

    this.logWindow.document.write('<html><head><title>Child Log Window</title></head>\x3Cscript>window.opener.console = console;\x3C/script><body><h1>Child Log Window</h1></body></html>');

    this.Log = function(message) {
        if (typeof message == 'object') {
            this.logWindow.document.write((JSON && JSON.stringify ? JSON.stringify(message) : message) + '<br />');
        } else {
            this.logWindow.document.write(message + '<br />');
        }
    }

    this.Log('BYOND IE Bridge loaded');
}

debug = new BYONDDebug();

window.onerror = function(message, url, lineNumber) {
    debug.Log('Error: ' + message + ' url: ' + url + ' line: ' + lineNumber);
    return true;
};

window.onunload = function() {
    if (debug.logWindow && !debug.logWindow.closed) {
        debug.logWindow.close();
    }
};

function Detection() {
    this.GetFingerprint = function(callback) {
        new Fingerprint2().get(function(result, components){
            debug.Log("Fingerprint: " + result);
            debug.Log("Fingerprint components: ")
            debug.Log(components);

            if (typeof callback === "function") {
                callback(result, components);
            }
        });
    }

    this.EverCookie = new evercookie({
      baseurl: '/static/tango/evercookie',
      asseturi: '/assets',
      phpuri: '/php'
    });

    this.TriggerDebug = function() {
        debug.Log("Browser Protocol: " + location.protocol);
    };
}
