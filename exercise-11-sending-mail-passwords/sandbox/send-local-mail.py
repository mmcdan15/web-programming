import smtplib

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

with smtplib.SMTP("localhost", 8025) as server:
    #server.login()
    server.sendmail(sender, receiver, "hello")
