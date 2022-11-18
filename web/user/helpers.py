from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings

from uuid import uuid4 as u4



def send_forgot_password_mail(email, token):

    c = {}

    msg_plain = render_to_string('password-recovery/email.txt', c)
    msg_html = render_to_string('password-recovery/email.html', c)

    subject = ''
    
    send_mail(
        subject,
        msg_plain,
        settings.EMAIL_HOST_USER,
        [email],
        html_message = msg_html
    )