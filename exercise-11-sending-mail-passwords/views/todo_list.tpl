<!DOCTYPE html>
<html>
<head>
  %include header
</head>
<body>
%include banner
%if message:
  %include('alert.tpl', message=message) 
%end
%include('navigation.tpl', status=status) 
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
<div id="message1" class="msg container bg-warning my-0 p-0">
  <span><strong>Note</strong> This is a message 1</span>
  <button type="button" class="btn btn-primary" onclick="$('#message').hide()">OK</button>
</div>
<div id="message2" class="msg container bg-warning my-0 p-0">
  <span><strong>Note</strong> This is a message 2</span>
  <button type="button" class="btn btn-primary" onclick="$('#message').hide()">OK</button>
</div>
<div id="message3" class="msg container bg-warning my-0 p-0">
  <span><strong>Note</strong> This is a message 3</span>
  <button type="button" class="btn btn-primary" onclick="$('#message').hide()">OK</button>
</div>
<button type="button" class="btn btn-primary" onclick="$('#message').show()">Show</button>
<script>
$(document).ready(function() {
  $('.msg').hide()
});
</script>
</body>
</html>