<!DOCTYPE html>
<html>
<head>
  %include banner
  %include header
</head>
<body>
%if message:
  %include('alert.tpl', message=message)
%end
%include('navigation.tpl', status=status)
<table class="table table-primary table-hover">
  <tr>
    <th>ID</th>
    <th>Item</th>
    <th>Price</th>
    <th>Purchased</th>
    <th>Edit</th>
    <th>Delete</th>
  </tr>
  %for item in items:
    <tr>
      <th>{{item['id']}}</th>
      <td>{{item['thing']}}</td>
      <td>{{item['price']}}$</td>
      <td>
      %if item['purchased']:
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
<div><a href="insert">Add a new item</a></div>
<hr/>
  %include drawing
</body>
</html>
