import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend_roc.utils.const import AUTH_EMAIL, AUTH_DOMAIN, AUTH_EMAIL_PWD


def send_email(message, subject, to_email):
    try:
        from_addr = AUTH_EMAIL
        to_addr = to_email
        msg = MIMEMultipart()
        msg['From'] = f"ROC OTP <{AUTH_EMAIL}>"
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


