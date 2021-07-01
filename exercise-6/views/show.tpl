<html>
<head>
</head>
<body>
<div>
<h2>Request demo</h2>
<button type="button" onclick="getData()">Get some data</button>
<div id="result">
  waiting...
</div>
</div>
<script>
function getData() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.getElementById("result").innerHTML = this.responseText
    }
    xhttp.open("GET","/data");
    xhttp.send();
}
</script>
</body>
</html>