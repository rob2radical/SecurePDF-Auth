import smtplib
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
server.login("testAccntPgrm2@yahoo.com", "lgeutogztgcpcydh")

msg = MIMEMultipart()

# message to be sent
SUBJECT = "Hello Dummy"
TEXT = "Hello world"

message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


server.sendmail("testAccntPgrm2@yahoo.com",
                "qrobert@rocketmail.com",
                message)
server.quit()