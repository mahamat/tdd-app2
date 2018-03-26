from flask_mail import Message
from flask import current_app
from project import mail
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('project.api', 'templates'))


def send(username, recipient):
    if current_app.config['TESTING']:
        return

    msg = Message(
        "Successfull Registration",
        sender=current_app.config['DEFAULT_MAIL_SENDER'],
        recipients=[recipient])
    template = env.get_template('registration_mail.html')
    msg.html = template.render(username=username)
    mail.send(msg)
