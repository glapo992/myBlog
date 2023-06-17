from flask_mail import Message
from app import mail



# actually send the email
from flask import render_template
from app import app

from threading import Thread


def send_async_email (app, msg):
    """make the email function to work in background in async
    send also app istance and create app context()
    allows the mail extension to find Falsl app istance 
    mail.send() has to access the config value that are related to the current app istace"""
    with app.app_context():
        print('email sent')
        mail.send(msg)

def send_email(subject, sender, recipients, text_body:str, html_body):
    """allows to send emails to a user

    :param subject: the subject of the email 
    :type subject: str
    :param sender: sender of the email
    :type sender: str
    :param recipients: destination mail addr  
    :type recipients: str
    :param text_body: text body of the email
    :type text_body: str
    :param html_body: html body of the email
    :type html_body: str html
    """
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # enable multithread to send email async
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    """send an email to the user when the password reset is requested, it uses a token to validate the request

    :param user: the user who requested the pw reset
    :type user: Users
    """
    token = user.get_reset_password_token() # 
    send_email('reset password',
                sender=app.config['ADMINS'][0], # email addr defined in the config file
                recipients=[user.email], 
                text_body=render_template('email_templates/reset_pwd.txt', user = user, token = token),    # txt message TODO:both must still be created
                html_body=render_template('email_templates/reset_pwd.html', user = user, token = token))   #html template 