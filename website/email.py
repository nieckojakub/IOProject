from flask import url_for
import smtplib, ssl
import config
from email.message import EmailMessage

EMAIL_ADDRESS = config.Config.MAIL_DEFAULT_SENDER
EMAIL_PASSWORD = config.Config.MAIL_PASSWORD
def send_reset_email(user):
    msg = EmailMessage()
    msg['Subject'] = 'AlCen Helpe: Password Reset Request'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user.email
    token = user.get_reset_token()

    msg.add_alternative(f"""<h1>We heard that you lost your AlCen Helper password. Sorry about that!</h1>
<p>But don’t worry! To initiate the password reset process for your account, click the link below.</p>
{ url_for('auth.reset_token', token=token, _external=True) }

If you did not make this request, you can simply ignore this email.
<br><br>
Sincerely,
AlCen Helper Team
""",subtype = 'html')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)