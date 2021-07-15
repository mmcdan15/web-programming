<!DOCTYPE html>
<html>
<head>
  %include header
</head>
<body>
<table class="table table-hover">
  <tr>
    %for key in table[0].keys():
      <th>{{key}}</th>
    %end
  </tr>
  %for row in table:
    <tr>
    %for key in row.keys():
      <td>{{row[key]}}</td>
    %end
    </tr>
  %end
</table>
</body>
</html>