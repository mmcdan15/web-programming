<html>
%include header
%include banner
<div style="text-align: center;">
Login
<form action="/login" method="post" style="text-align: center;">
    Username<br/>
    <input type="text" name="username"/><br/>
    Password<br/>
    <input type="password" name="password"/><br/>
    <hr/>
    <input type="submit" value="Login"/>
</form>
</div>
</html>
 <!--Includes header and banner
   gets post login 
   asks for username and password
   submits values-->