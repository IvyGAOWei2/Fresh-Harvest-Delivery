import traceback
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def sendEmail(data, receiver, subject, senderName, auth, HTML=False):
    port = 587
    sender = auth['email']['user']
    ## enforce receiver
    receiver = ['fateofheart@gmail.com']
    user = auth['email']['user']
    password = auth['email']['password']

    if HTML:
        msg = MIMEText(data,_subtype='html',_charset='utf-8')
    else:
        msg = MIMEText(data)

    msg['From'] = formataddr((Header(senderName, 'utf-8').encode(), sender))
    msg['To'] = ", ".join(receiver)
    msg['subject'] = Header(subject, 'utf-8')

    try:
        with smtplib.SMTP("smtp.office365.com", port) as server:
            # server.set_debuglevel(1)
            server.starttls()
            server.login(user, password)
            server.sendmail(sender, receiver, msg.as_string())
            print('Email: ' + subject + " successfully sent")
            return True
    except:
        print(traceback.format_exc())
        return False