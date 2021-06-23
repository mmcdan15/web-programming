<html>
<body>
<table>
  <tr>
    <th>ID</th>
    <th>Task</th>
    <th>Done1</th>
    <th>Done2</th>
    <th>Delete?</th>
  </tr>
  %for item in items:
    <tr>
      <th>{{item['id']}}</th>
      <td>{{item['task']}}</td>
      <td>
      %if item['done']:
        yes
      %else:
        no
      %end
      </td>
      <td>{{'yes' if item['done'] else 'no'}}</td>
      <td><a href="/delete/{{item['id']}}">Delete</a></td>
    </tr>
  %end
</table>
<hr/>
<a href="insert">Add a new task...</a>
<hr/>
</body>
</html>