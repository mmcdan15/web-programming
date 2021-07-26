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
        data = JSON.parse(this.responseText)
        //document.getElemendocument.getElementById("result")tById("result").innerHTML = "<p><i>"+JSON.stringify(data.pets)+"</i></p>"
        result_element = document.getElementById("result");
        result_element.textContent = "";
        table_element = document.createElement("table");
        result_element.appendChild(table_element);
        data.pets.forEach(function(pet) {
            row_element = document.createElement("tr");
            table_element.appendChild(row_element);
            name_element = document.createElement("td");
            row_element.appendChild(name_element);
            name_element.textContent = pet.name;
            kind_element = document.createElement("td");
            row_element.appendChild(kind_element);
            kind_element.textContent = pet.kind;
        })
    }
    xhttp.open("GET","/data");
    xhttp.send();
}
</script>
</body>
</html>