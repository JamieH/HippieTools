function Detection() {
    this.GetFingerprint = function(callback) {
        new Fingerprint2().get(function(result, components){
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
}
