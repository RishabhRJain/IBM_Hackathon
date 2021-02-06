from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from os.path import basename
import netifaces as ni
import smtplib

fromEmail = 'foodexasu@gmail.com'
fromEmailPassword = 'foodex_asu'

toEmail = 'lkarupar@asu.edu'
# toEmail = 'suchit@asu.edu'

def send_email():
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Foodex Expiry Reminder'
    msgRoot['From'] = fromEmail
    msgRoot['To'] = toEmail
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('Click the following link to add to calender:')
    msgAlternative.attach(msgText)

    files = ['expiry_reminder.ics']
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msgRoot.attach(part)


    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(fromEmail, fromEmailPassword)
    smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
    smtp.quit()

if __name__ == '__main__':
    send_email()
