<html>
<body>
<table>
  <tr>
    <th>Task</th>
    <th>Done1</th>
    <th>Done2</th>
  </tr>
  %for item in items:
    <tr>
      <td>{{item['task']}}</td>
      <td>
      %if item['done']:
        yes
      %else:
        no
      %end
      </td>
      <td>{{'yes' if item['done'] else 'no'}}</td>
    </tr>
  %end
</table>
<hr/>
</body>
</html>