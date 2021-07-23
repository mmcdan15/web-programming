import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

text = f"""\
This is a test e-mail message.

Check out http://mailtrap.io

-greg
"""

html = f"""\
<html>
<body>
<p>This is a test e-mail message.<br/></p>

<p>Check out <a href="http://mailtrap.io">http://mailtrap.io</a><br/></p>

<p>-greg<br/></p>
</body>
</html>
"""

message = MIMEMultipart("alternative")
message["Subject"] = "Test email from Python"
message["From"] = sender
message["To"] = receiver

message.attach(MIMEText(text,"plain"))
message.attach(MIMEText(html,"html"))

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login("eb60697f581e3e", "7777b332599f8c")
    server.sendmail(sender, receiver, message.as_string())