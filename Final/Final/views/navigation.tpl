<!DOCTYPE html>
<html>
<head></head>
<body>
<div>
%if username:  
<a href="/">My Lists</a></br>
<a href="/logout">Logout</a></br>
%else: 
<a href="/login">Login</a></br>
<a href="/signup">Sign Up</a></br>
%end  
<a href="/forgot">Reset password</a>
</div>
</body>

<style> 
  div {
  background-color: white;
  text-color: black;
  text-align: center;
}
</style>
