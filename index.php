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
<script type="text/javascript" src="resources/js/fingerprint2.min.js"></script>
<script type="text/javascript" src="resources/evercookie/js/swfobject-2.2.min.js"></script>
<script type="text/javascript" src="resources/evercookie/js/evercookie.js"></script>
<script type="text/javascript" src="resources/evercookie/js/detection.js"></script>

<script>
$(function(){
    var detection = new Detection()
    detection.debug()
});
</script>

</html>
