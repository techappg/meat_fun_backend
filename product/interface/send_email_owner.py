import smtplib
import traceback
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from backend_roc.utils.const import AUTH_EMAIL, AUTH_DOMAIN, AUTH_EMAIL_PWD


def owner_send_email(message, subject, to_email):
    try:
        from_addr = AUTH_EMAIL
        to_addr = to_email
        msg = MIMEMultipart()
        msg['From'] = f"<{AUTH_EMAIL}>"
        msg['To'] = to_addr
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(AUTH_DOMAIN, 587)
        server.starttls()
        server.login(from_addr, AUTH_EMAIL_PWD)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
        return "success"
    except:
        traceback.print_exc()
        return "failed"


def file_send_email( subject, to_email, files=None):
    try:
        from_addr = AUTH_EMAIL
        to_addr = to_email
        msg = MIMEMultipart()
        msg['From'] = f"<{AUTH_EMAIL}>"
        msg['To'] = to_addr
        msg['Subject'] = subject

        # body = message
        # msg.attach(MIMEText(body, 'html'))

        filename = "Cv.pdf"
        attachment = open(files.path, "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        server = smtplib.SMTP(AUTH_DOMAIN, 587)
        server.starttls()
        server.login(from_addr, AUTH_EMAIL_PWD)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
        return "success"
    except:
        traceback.print_exc()
        return "failed"

