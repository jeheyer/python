from smtplib import SMTP

class EMail():

    def __init__(self, sender, recipient, subject = "", body = ""):

        self.sender = sender
        self.recipient = recipient
        header = "From: <" + self.sender + ">\n"
        header += "To: <" + self.recipient + ">\n"
        if subject:
            self.subject = subject
        else:
            self.subject = ""
        header += "Subject: " + self.subject + "\n\n"
        if body:
            self.body = body
        else:
            self.body = ""
        contents = header + self.body

        try:
            smtpObj = SMTP('localhost')
            smtpObj.sendmail(self.sender, self.recipient, contents)
        except:
            print("Error: unable to send email")

