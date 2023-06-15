from flask_mail import Message
from app import mail

# actually send the email
from flask import render_template
from app import app

def send_email(subject, sender, recipients, text_body:str, html_body):
    """allows to send emails to a user

    :param subject: the subject of the email 
    :type subject: str
    :param sender: sender of the email
    :type sender: str
    :param recipients: _description_
    :type recipients: _type_
    :param text_body: text body of the email
    :type text_body: str
    :param html_body: html body of the email
    :type html_body: str html
    """
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token() # 
    send_email(subject='reset password',
                sender=app.config['ADMINS'][0] # email addr defined in the config file
                recipients=[user.email], 
                text_body=render_template('email/reset_password.txt', user = user, token = token),    # txt message TODO:both must still be created
                text_body=render_template('email/reset_password.html', user = user, token = token),   #html template 
    )