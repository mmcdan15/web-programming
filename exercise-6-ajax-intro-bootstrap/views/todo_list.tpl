<!DOCTYPE html>
<html>
<head>
  %include header
</head>
<body>
%include banner
<table class="table table-dark table-hover">
  <tr>
    <th>ID</th>
    <th>Task</th>
    <th>Completed</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>
  %for item in items:
    <tr>
      <th>{{item['id']}}</th>
      <td>{{item['task']}}</td>
      <td>
      %if item['done']:
        <span class="material-icons-outlined">check_circle</span>
      %else:
        <span class="material-icons-outlined">unpublished</span>
      %end
      </td>
      <td><a href="/edit/{{item['id']}}"><span class="material-icons">
edit
</span></a></td>
      <td><a href="/delete/{{item['id']}}"><span class="material-icons">
delete
</span></a></td>
    </tr>
  %end
</table>
<hr/>
<a href="insert">Add a new task...</a>
<hr/>
</body>
</html>