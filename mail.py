import smtplib

def sendMail():
    server = smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465)
    server.login("testAccntPgrm2@yahoo.com", "lgeutogztgcpcydh")

    # message to be sent
    SUBJECT = "Verification Code"
    TEXT = "67C6B5"

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    print("The hashed message is : " + str(hash(message)))


    server.sendmail("testAccntPgrm2@yahoo.com",
                    "qrobert@rocketmail.com",
                    message)
    server.quit()
sendMail()