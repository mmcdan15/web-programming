<html>
Reset Password
<form action="/reset/{{username}}/{{reset_token}}" method="post">
    Username<br/>
    <p>{{ username }}</p><br/>
    Password<br/>
    <input type="password" name="password"/><br/>
    Password, Again<br/>
    <input type="password" name="password_again"/><br/>
    <hr/>
    <input type="submit" value="Reset Password"/>
</form>
</html>