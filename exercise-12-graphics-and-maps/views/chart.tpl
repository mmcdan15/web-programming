<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/p5@1.4.0/lib/p5.js"></script>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script>
    function setup() {
      createCanvas(400, 400);
    }
    function draw() {
      background(220);
      ellipse(50,50,80,80);
    }
</script>
<script>
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Task', 'Hours per Day'],
          ['Work',     11],
          ['Eat',      2],
          ['Commute',  2],
          ['Watch TV', 2],
          ['Sleep',    7]
        ]);

        var options = {
          title: 'My Daily Activities'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
</script>
</head>
<body>
<h1>This is a drawing...</h1>
<main></main>
<hr/>
 <div id="piechart" style="width: 900px; height: 500px;"></div>
<hr/>
<p>So how was that?</p>
</body>
</html>