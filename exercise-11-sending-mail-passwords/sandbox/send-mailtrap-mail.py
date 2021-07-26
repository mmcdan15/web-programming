import smtplib

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message.

Check out http://mailtrap.io

-greg
"""

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login("eb60697f581e3e", "7777b332599f8c")
    server.sendmail(sender, receiver, message)