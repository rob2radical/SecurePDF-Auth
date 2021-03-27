import smtplib

def sendMail():
    server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
    server.login("testAccntPgrm2@yahoo.com", "lgeutogztgcpcydh")

    # message to be sent
    SUBJECT = "Hello Dummy"
    TEXT = "Hello world"

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)


    server.sendmail("testAccntPgrm2@yahoo.com",
                    "isaiasmtz12@yahoo.com",
                    message)
    server.quit()