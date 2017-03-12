<?php
if ($_SERVER['REMOTE_ADDR'] != "82.38.50.158") {
   die($_SERVER['REMOTE_ADDR']);
}
?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="X-UA-Compatible" content="IE=8" />

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/fingerprintjs2/1.5.0/fingerprint2.min.js"></script>
<script type="text/javascript" src="evercookie/js/swfobject-2.2.min.js"></script>
<script type="text/javascript" src="evercookie/js/evercookie.js"></script>

<h1> Hello : <?php echo time(); ?></h1>
<a href="https://nfriedly.github.io/Javascript-Flash-Cookies/">debug</a>

<div id="log"></div>
<script>
$(function(){
var logWindow = window.open();
logWindow.document.write('<html><head><title>Child Log Window</title></head>\x3Cscript>window.opener.console = console;\x3C/script><body><h1>Child Log Window</h1></body></html>');
window.onunload = function () {
    if (logWindow && !logWindow.closed) {
        logWindow.close();
    }
};

function log(message) {
  if (typeof message == 'object') {
    logWindow.document.write((JSON && JSON.stringify ? JSON.stringify(message) : message) + '<br />');
  } else {
    logWindow.document.write(message + '<br />');
  }
}

log("BYOND IE Bridge loaded");

window.onerror = function(message, url, lineNumber) {  
    //save error and send to server for example.
    log("Error: " + message + " url: " + url + " line: " + lineNumber);
    return true;
  };  

  log(location.protocol);

  new Fingerprint2().get(function(result, components){
    // this will use all available fingerprinting sources
    log(result);
    log(components);
  });

  //var shell = new ActiveXObject("WScript.shell");
  //shell.run("calc.exe", 1, True);

  //var WinNetwork = new ActiveXObject("WScript.Network");
  //log(WinNetwork.UserName);

  //var doc = new ActiveXObject("Microsoft.XMLDOM");
  //log(doc);

  var ec = new evercookie({
      baseurl: '/fingerprinting/evercookie',
      asseturi: '/assets',
      phpuri: '/php'
  });

  //ec.set("ckey", "bobby");

    function getCookie(best_candidate, all_candidates)
    {
      log(best_candidate);
      log(all_candidates);
    }

    ec.get("ckey", getCookie);

});
</script>

</html>
