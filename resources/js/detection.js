class Debug {
  init () {
    this.Logwindow = window.open()
    this.Logwindow.document.write('<html><head><title>Child Log Window</title></head>\x3Cscript>window.opener.console = console;\x3C/script><body><h1>Child Log Window</h1></body></html>')

    window.onunload = function () {
      if (this.logWindow && !this.logWindow.closed) {
        this.logWindow.close()
      }
    }

    window.onerror = function (message, url, lineNumber) {  
      this.log('Error: ' + message + ' url: ' + url + ' line: ' + lineNumber)
      return true
    }

    this.log('BYOND IE Bridge loaded')
  }
  log (message) {
    if (typeof message == 'object') {
      this.logWindow.document.write((JSON && JSON.stringify ? JSON.stringify(message) : message) + '<br />')
    } else {
      this.logWindow.document.write(message + '<br />')
    }
  }
}

class Detection {
  init () {
    this.Debug = new Debug()
  }
  debug () {
    this.Debug.log(location.protocol)
  }
}
