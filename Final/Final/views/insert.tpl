<html>
%include header
%include banner
<body>
<form action="/insert" method="post">
<!-- Item name-->
Item <input type="text" name="thing"/><br>
<!-- Has a step of 0.01-->
Price <input type="number" step="0.01" name="price"/> $<br>
<hr/>
<!-- Cancel button -->	
<button onclick="window.location='/'; return false">Cancel</button>&nbsp
<a href='/'>Cancel</a>&nbsp
<input type="submit" value="Submit"/>
</form>
<hr/>
</body>
</html>