from flask import url_for, render_template
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

    #msg.add_alternative(render_template('password_reset.html', token=token), subtype='html')
    msg.add_alternative(f"""<h1>We heard that you lost your AlCen Helper password. Sorry about that!</h1>
    <p>But don’t worry! To initiate the password reset process for your account, click the link below.</p>
    {url_for('auth.reset_token', token=token, _external=True)}
    <p>If you did not make this request, you can simply ignore this email.</p>
    <br><br>
    Sincerely,
    AlCen Helper Team
    """, subtype='html')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def send_mail_confirmation(user):
    msg = EmailMessage()
    msg['Subject'] = 'AlCen Helper: Confirm your email'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user.email
    token = user.get_mail_confirm_token()
    #msg.html = render_template(render_template('confirm_email.html', token=token), subtype='html')
    msg.add_alternative(f"""<h1>Thank You for joining AlCen Helper!</h1>
    <p>Click the following link or button to verify your email</p>
    {url_for('auth.confirm_email', token=token, _external=True)}
    <p> If you didn't create an account with AlCen Helper, you can safely delete this email.</p>
    <br><br>
    Sincerely,
    AlCen Helper Team
    """, subtype='html')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
