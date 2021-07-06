<html>
<body>
<form action="/edit" method="post">
Description <input type="text" name="task" value="{{item['task']}}"/><br>
<hr/>
<button onclick="window.location='/'; return false">Cancel</button>&nbsp
<a href='/'>Cancel</a>&nbsp
<input type="submit" value="Submit"/>

<input type="text" name="id" value="{{item['id']}}" readonly hidden/>
</form>
<hr/>
</body>
</html>