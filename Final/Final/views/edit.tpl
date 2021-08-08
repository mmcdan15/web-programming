<!DOCTYPE html>
<html>
<head>
%include header
</head>
<body>
%include banner
<form action="/edit" method="post">
Item <input type="text" name="thing" value="{{item['thing']}}"/><br>
Price <input type="number" step="0.01" name="price" value="{{item['price']}}"/><br>
Purchased<input type="checkbox" id="purchased" name="purchased">

<hr/>
<button onclick="window.location='/'; return false">Cancel</button>&nbsp
<a href='/'>Cancel</a>&nbsp
<input type="submit" value="Submit"/>




<input type="text" name="id" value="{{item['id']}}" readonly hidden/>
</form>
<hr/>
</body>
</html>
 <!--Includes header and banner to show up on edit page
   get item group for name and value
   Price goes up by 0.01
   If canceled returns to main page
   Or submit-->