import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = "Dr. Person<person@gmail.com>"
receiver = "A Test User <gdelozie@kent.edu>"

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

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login("person@gmail.com", "immtjpsxyodyyqsk")
    server.sendmail(sender, receiver, message.as_string())