from flask_mail import Message
from app import mail

# actually send the email
from flask import render_template
from app import app

# make email serivce asynchronous
from threading import Thread


def send_async_email(app:app, msg)->None:
    """creates an application context and make the app istance accessible to mail extension via current_app var from flask"""
    with app.app.context():
        mail.send(message=msg)


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
    # make the mail service an async task in background to improve efficency in real environment
    # the values sent to the method are the message to send and the application istance (context)
    Thread(target=send_async_email, args=(app, msg)).start() 

def send_password_reset_email(user):
    """send an email to the user when the password reset is requested, it uses a token to validate the request

    :param user: the user who requested the pw reset
    :type user: Users
    """
    token = user.get_reset_password_token() # 
    send_email(subject='reset password',
                sender=app.config['ADMINS'][0], # email addr defined in the config file
                recipients=[user.email], 
                text_body=render_template('email_templates/reset_password.txt', user = user, token = token),    # txt message TODO:both must still be created
                html_body=render_template('email_templates/reset_password.html', user = user, token = token))   # html template 
    